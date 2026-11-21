"""Pruebas de integración de clientes, servicios y reservas."""
import unittest  # unittest: marco de pruebas incluido en Python

from cliente import Cliente  # clase Cliente a probar
from excepciones import (  # excepciones propias que se esperan en las pruebas
    ClienteInvalidoError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,  # (importación repetida de ReservaInvalidaError; no afecta el funcionamiento)
)
from reserva import Reserva  # clase Reserva a probar
from servicios import AsesoriaEspecializada, ReservaSala, Servicio  # servicios a probar


# Cada método test_* es una prueba independiente
class PruebasIntegracion(unittest.TestCase):
    def setUp(self):  # setUp se ejecuta antes de cada prueba y prepara los datos
        self.cliente = Cliente(  # crea un cliente válido para las pruebas
            "CC-2001", "María López", "maria@example.com", "3001234567"
        )
        self.sala = ReservaSala("Sala de pruebas", 40000, 8)  # crea una sala válida para las pruebas

    # Prueba: un cliente con datos válidos se guarda correctamente
    def test_cliente_valido(self):
        self.assertEqual(self.cliente.nombre, "María López")  # el nombre debe ser el esperado
        self.assertEqual(self.cliente.correo, "maria@example.com")  # el correo debe ser el esperado

    # Prueba: un correo inválido debe lanzar ClienteInvalidoError
    def test_cliente_correo_invalido(self):
        with self.assertRaises(ClienteInvalidoError):  # se espera que el bloque lance esa excepción
            Cliente("CC-2002", "Juan Pérez", "correo-invalido", "3001234567")  # correo sin formato válido

    # Prueba: la clase Servicio es abstracta y no se puede instanciar
    def test_servicio_es_abstracto(self):
        with self.assertRaises(TypeError):  # Python lanza TypeError al instanciar una clase abstracta
            Servicio("Base", 100)  # intenta crear la clase abstracta

    # Prueba: flujo completo de una reserva (crear, confirmar y procesar)
    def test_reserva_y_procesamiento(self):
        reserva = Reserva("RES-2001", self.cliente, self.sala, 2)  # crea una reserva de 2 horas
        self.assertEqual(reserva.estado, "Pendiente")  # toda reserva inicia Pendiente
        reserva.confirmar()  # pasa a Confirmada
        costo = reserva.procesar()  # procesa y devuelve el costo
        self.assertEqual(costo, 80000)  # 40000 x 2 horas = 80000
        self.assertEqual(reserva.estado, "Procesada")  # el estado final es Procesada

    # Prueba: no se puede confirmar una reserva cancelada
    def test_no_confirmar_reserva_cancelada(self):
        reserva = Reserva("RES-2002", self.cliente, self.sala, 1)  # crea la reserva
        reserva.cancelar()  # la cancela
        with self.assertRaises(OperacionNoPermitidaError):  # confirmar ahora debe lanzar OperacionNoPermitidaError
            reserva.confirmar()  # intento no permitido

    # Prueba: no se puede reservar un servicio no disponible
    def test_no_reservar_servicio_no_disponible(self):
        servicio = ReservaSala(  # crea una sala con disponible=False
            "Sala cerrada", 40000, 8, disponible=False
        )
        with self.assertRaises(ServicioNoDisponibleError):  # la reserva debe lanzar ServicioNoDisponibleError
            Reserva("RES-2003", self.cliente, servicio, 1)  # intento de reservar el servicio cerrado

    # Prueba: la reserva rechaza un cliente que no sea objeto Cliente
    def test_reserva_rechaza_objeto_cliente_invalido(self):
        with self.assertRaises(ReservaInvalidaError):  # debe lanzar ReservaInvalidaError
            Reserva("RES-2004", "No es un cliente", self.sala, 1)  # pasa un texto en lugar de un cliente

    # Prueba: la asesoría senior aplica el recargo del 25 %
    def test_asesoria_calcula_recargo_senior(self):
        asesoria = AsesoriaEspecializada(  # crea una asesoría senior
            "Asesoría", 80000, "senior"
        )
        self.assertEqual(asesoria.calcular_costo(2), 200000)  # 80000 x 2 horas x 1,25 = 200000

    # Prueba: un error al procesar conserva su causa original (encadenamiento)
    def test_error_de_procesamiento_conserva_causa(self):
        reserva = Reserva("RES-2005", self.cliente, self.sala, 1)  # crea la reserva
        reserva.confirmar()  # la confirma
        self.sala.disponible = False  # desactiva el servicio después de confirmar
        with self.assertRaises(ReservaInvalidaError) as contexto:  # procesar debe lanzar ReservaInvalidaError
            reserva.procesar()  # intenta procesar con el servicio no disponible
        self.assertIsInstance(  # la causa original debe ser ServicioNoDisponibleError
            contexto.exception.__cause__, ServicioNoDisponibleError
        )

    # Prueba: no se puede cancelar una reserva dos veces
    def test_no_cancelar_reserva_dos_veces(self):
        reserva = Reserva("RES-2006", self.cliente, self.sala, 1)  # crea la reserva
        reserva.cancelar()  # primera cancelación: correcta
        with self.assertRaises(OperacionNoPermitidaError):  # la segunda debe lanzar OperacionNoPermitidaError
            reserva.cancelar()  # segunda cancelación: no permitida

    # Prueba: una duración de cero horas es inválida
    def test_duracion_invalida(self):
        with self.assertRaises(ReservaInvalidaError):  # debe lanzar ReservaInvalidaError
            Reserva("RES-2007", self.cliente, self.sala, 0)  # duración 0


# Ejecuta todas las pruebas si el archivo se corre directamente
if __name__ == "__main__":
    unittest.main(verbosity=2)  # verbosity=2 muestra el detalle de cada prueba

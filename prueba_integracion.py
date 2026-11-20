"""Pruebas de integración de clientes, servicios y reservas."""
import unittest

from cliente import Cliente
from excepciones import (
    ClienteInvalidoError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
)
from reserva import Reserva
from servicios import AsesoriaEspecializada, ReservaSala, Servicio


class PruebasIntegracion(unittest.TestCase):
    def setUp(self):
        self.cliente = Cliente(
            "CC-2001", "María López", "maria@example.com", "3001234567"
        )
        self.sala = ReservaSala("Sala de pruebas", 40000, 8)

    def test_cliente_valido(self):
        self.assertEqual(self.cliente.nombre, "María López")
        self.assertEqual(self.cliente.correo, "maria@example.com")

    def test_cliente_correo_invalido(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("CC-2002", "Juan Pérez", "correo-invalido", "3001234567")

    def test_servicio_es_abstracto(self):
        with self.assertRaises(TypeError):
            Servicio("Base", 100)

    def test_reserva_y_procesamiento(self):
        reserva = Reserva("RES-2001", self.cliente, self.sala, 2)
        self.assertEqual(reserva.estado, "Pendiente")
        reserva.confirmar()
        costo = reserva.procesar()
        self.assertEqual(costo, 80000)
        self.assertEqual(reserva.estado, "Procesada")

    def test_no_confirmar_reserva_cancelada(self):
        reserva = Reserva("RES-2002", self.cliente, self.sala, 1)
        reserva.cancelar()
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.confirmar()

    def test_no_reservar_servicio_no_disponible(self):
        servicio = ReservaSala(
            "Sala cerrada", 40000, 8, disponible=False
        )
        with self.assertRaises(ServicioNoDisponibleError):
            Reserva("RES-2003", self.cliente, servicio, 1)

    def test_reserva_rechaza_objeto_cliente_invalido(self):
        with self.assertRaises(ReservaInvalidaError):
            Reserva("RES-2004", "No es un cliente", self.sala, 1)

    def test_asesoria_calcula_recargo_senior(self):
        asesoria = AsesoriaEspecializada(
            "Asesoría", 80000, "senior"
        )
        self.assertEqual(asesoria.calcular_costo(2), 200000)

    def test_error_de_procesamiento_conserva_causa(self):
        reserva = Reserva("RES-2005", self.cliente, self.sala, 1)
        reserva.confirmar()
        self.sala.disponible = False
        with self.assertRaises(ReservaInvalidaError) as contexto:
            reserva.procesar()
        self.assertIsInstance(
            contexto.exception.__cause__, ServicioNoDisponibleError
        )

    def test_no_cancelar_reserva_dos_veces(self):
        reserva = Reserva("RES-2006", self.cliente, self.sala, 1)
        reserva.cancelar()
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.cancelar()

    def test_duracion_invalida(self):
        with self.assertRaises(ReservaInvalidaError):
            Reserva("RES-2007", self.cliente, self.sala, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

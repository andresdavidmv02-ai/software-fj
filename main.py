"""Programa principal de demostración del sistema Software FJ."""
from cliente import Cliente
from excepciones import (
    ClienteInvalidoError,
    ErrorSistemaFJ,
    ParametroInvalidoError,
    ReservaInvalidaError,
)
from logs import registrar_error, registrar_evento
from reserva import Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala, Servicio


clientes = []
servicios = []
reservas = []
estadisticas = {"total": 0, "exitosas": 0, "errores_controlados": 0, "errores_inesperados": 0}


def ejecutar(numero, descripcion, operacion):
    """Ejecuta una operación, informa el resultado y registra su resultado."""
    print(f"\n[{numero}] {descripcion}")
    estadisticas["total"] += 1

    try:
        resultado = operacion()
    except ErrorSistemaFJ as error:
        estadisticas["errores_controlados"] += 1
        registrar_error(descripcion, error)
        print(f"ERROR CONTROLADO: {type(error).__name__}: {error}")
        return None
    except Exception as error:
        estadisticas["errores_inesperados"] += 1
        registrar_error(f"Error inesperado en: {descripcion}", error)
        print(
            f"ERROR INESPERADO REGISTRADO: {type(error).__name__}: {error}"
        )
        return None
    else:
        estadisticas["exitosas"] += 1
        registrar_evento(f"Operación {numero} completada: {descripcion}")
        if hasattr(resultado, "mostrar_informacion"):
            detalle = resultado.mostrar_informacion()
        else:
            detalle = resultado
        print(f"CORRECTO: {detalle}")
        return resultado
    finally:
        print(f"Fin de operación {numero}.")


def registrar_cliente(identificacion, nombre, correo, telefono):
    identificacion_normalizada = str(identificacion).strip()
    if any(c.identificador == identificacion_normalizada for c in clientes):
        raise ClienteInvalidoError(
            "Ya existe un cliente con esa identificación"
        )
    cliente = Cliente(identificacion, nombre, correo, telefono)
    clientes.append(cliente)
    return cliente


def registrar_servicio(servicio):
    if not isinstance(servicio, Servicio):
        raise ParametroInvalidoError(
            "Solo se pueden registrar objetos de tipo Servicio"
        )
    servicios.append(servicio)
    return servicio


def crear_reserva(identificador, cliente, servicio, duracion):
    identificador_normalizado = str(identificador).strip()
    if any(r.identificador == identificador_normalizado for r in reservas):
        raise ReservaInvalidaError(
            "Ya existe una reserva con ese identificador"
        )
    reserva = Reserva(identificador, cliente, servicio, duracion)
    reservas.append(reserva)
    return reserva


def main():
    """Ejecuta 17 operaciones de demostración, válidas y no válidas."""
    clientes.clear()
    servicios.clear()
    reservas.clear()
    for clave in estadisticas:
        estadisticas[clave] = 0

    print("=" * 58)
    print("       SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("=" * 58)

    # 1. Registro válido de cliente.
    cliente_obj = ejecutar(
        1,
        "Registrar cliente válido",
        lambda: registrar_cliente(
            "CC-1001", "Laura Gómez", "laura@email.com", "3001234567"
        ),
    )

    # 2. Registro inválido de cliente.
    ejecutar(
        2,
        "Registrar cliente con correo inválido",
        lambda: registrar_cliente(
            "CC-1002", "Carlos Pérez", "correo-invalido", "3011234567"
        ),
    )

    # 3. Intento de identificación duplicada.
    ejecutar(
        3,
        "Registrar cliente con identificación duplicada",
        lambda: registrar_cliente(
            "CC-1001", "Otra Persona", "otra@email.com", "3021234567"
        ),
    )

    # 4. Creación de servicio de sala.
    sala_obj = ejecutar(
        4,
        "Crear servicio de reserva de sala",
        lambda: registrar_servicio(ReservaSala("Sala Norte", 50000, 12)),
    )

    # 5. Creación de servicio de alquiler de equipo.
    ejecutar(
        5,
        "Crear servicio de alquiler de equipo",
        lambda: registrar_servicio(
            AlquilerEquipo("Portátil", 15000, seguro=5000)
        ),
    )

    # 6. Creación incorrecta de servicio.
    ejecutar(
        6,
        "Crear servicio con tarifa negativa",
        lambda: registrar_servicio(AlquilerEquipo("Proyector", -100)),
    )

    # 7. Creación de asesoría especializada.
    ejecutar(
        7,
        "Crear servicio de asesoría especializada",
        lambda: registrar_servicio(
            AsesoriaEspecializada("Consultoría Python", 80000, "senior")
        ),
    )

    # 8. Registro de un servicio temporal no disponible.
    ejecutar(
        8,
        "Crear servicio temporal no disponible",
        lambda: registrar_servicio(
            ReservaSala(
                "Sala en mantenimiento", 40000, 8, disponible=False
            )
        ),
    )
    no_disponible_obj = next(
        (s for s in servicios if s.nombre == "Sala en mantenimiento"), None
    )

    # 9. Intento de reserva con servicio no disponible.
    if cliente_obj and no_disponible_obj:
        ejecutar(
            9,
            "Intentar reservar un servicio no disponible",
            lambda: crear_reserva(
                "RES-009", cliente_obj, no_disponible_obj, 2
            ),
        )

    # 10. Crear reserva válida.
    reserva_obj = None
    if cliente_obj and sala_obj:
        reserva_obj = ejecutar(
            10,
            "Crear reserva válida",
            lambda: crear_reserva("RES-010", cliente_obj, sala_obj, 3),
        )

    # 11. Confirmar reserva.
    if reserva_obj:
        ejecutar(11, "Confirmar reserva", reserva_obj.confirmar)

    # 12. Procesar reserva confirmada.
    if reserva_obj:
        ejecutar(12, "Procesar reserva confirmada", reserva_obj.procesar)

    # 13. Intentar cancelar una reserva ya procesada.
    if reserva_obj:
        ejecutar(13, "Cancelar reserva ya procesada", reserva_obj.cancelar)

    # 14. Intentar crear una reserva sin cliente.
    if sala_obj:
        ejecutar(
            14,
            "Crear reserva sin cliente",
            lambda: crear_reserva("RES-014", None, sala_obj, 1),
        )

    # 15, 16 y 17. Crear, cancelar y volver a confirmar una reserva.
    if cliente_obj and sala_obj:
        reserva_pendiente = ejecutar(
            15,
            "Crear segunda reserva pendiente",
            lambda: crear_reserva("RES-015", cliente_obj, sala_obj, 1),
        )
        if reserva_pendiente:
            ejecutar(
                16, "Cancelar reserva pendiente", reserva_pendiente.cancelar
            )
            ejecutar(
                17,
                "Intentar confirmar reserva cancelada",
                reserva_pendiente.confirmar,
            )

    print("\n" + "=" * 58)
    print("RESUMEN DEL SISTEMA")
    print(f"Clientes registrados: {len(clientes)}")
    print(f"Servicios registrados: {len(servicios)}")
    print(f"Reservas registradas: {len(reservas)}")
    print(f"Operaciones ejecutadas: {estadisticas['total']}")
    print(f"Operaciones exitosas: {estadisticas['exitosas']}")
    print(f"Errores controlados: {estadisticas['errores_controlados']}")
    print(f"Errores inesperados: {estadisticas['errores_inesperados']}")
    print("Los eventos y errores se guardaron en software_fj.log")
    print("=" * 58)
    registrar_evento("Ejecución de demostración finalizada")


if __name__ == "__main__":
    main()

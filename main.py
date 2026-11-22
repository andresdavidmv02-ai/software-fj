"""Programa principal de demostración del sistema Software FJ."""
from cliente import Cliente  # clase Cliente
from excepciones import (  # excepciones propias usadas en el programa
    ClienteInvalidoError,
    ErrorSistemaFJ,
    ParametroInvalidoError,
    ReservaInvalidaError,
)
from logs import registrar_error, registrar_evento  # funciones para escribir eventos y errores en el archivo de log
from reserva import Reserva  # clase Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala, Servicio  # servicios (clase abstracta y tres especializados)


# Listas internas: reemplazan a una base de datos (todo se guarda en memoria)
clientes = []  # clientes registrados
servicios = []  # servicios registrados
reservas = []  # reservas creadas
# Contadores para el resumen final
estadisticas = {"total": 0, "exitosas": 0, "errores_controlados": 0, "errores_inesperados": 0}


# Ejecuta una operación y controla sus errores con try/except/else/finally
def ejecutar(numero, descripcion, operacion):
    """Ejecuta una operación, informa el resultado y registra su resultado."""
    print(f"\n[{numero}] {descripcion}")  # muestra el número y la descripción de la operación
    estadisticas["total"] += 1  # suma una operación al total

    try:  # try: intenta ejecutar la operación recibida
        resultado = operacion()  # ejecuta la función y guarda su resultado
    except ErrorSistemaFJ as error:  # except 1: errores propios del sistema (controlados)
        estadisticas["errores_controlados"] += 1  # cuenta el error controlado
        registrar_error(descripcion, error)  # lo registra en el archivo de log
        print(f"ERROR CONTROLADO: {type(error).__name__}: {error}")  # informa el error en pantalla
        return None  # devuelve None para que el programa continúe
    except Exception as error:  # except 2: cualquier otro error imprevisto
        estadisticas["errores_inesperados"] += 1  # cuenta el error inesperado
        registrar_error(f"Error inesperado en: {descripcion}", error)  # lo registra en el log
        print(  # informa el error inesperado en pantalla
            f"ERROR INESPERADO REGISTRADO: {type(error).__name__}: {error}"
        )
        return None  # devuelve None y el programa sigue funcionando
    else:  # else: se ejecuta solo si NO hubo error
        estadisticas["exitosas"] += 1  # cuenta la operación exitosa
        registrar_evento(f"Operación {numero} completada: {descripcion}")  # registra el evento en el log
        if hasattr(resultado, "mostrar_informacion"):  # si el resultado es una entidad...
            detalle = resultado.mostrar_informacion()  # ...usa su descripción
        else:  # si no...
            detalle = resultado  # ...usa el resultado tal cual
        print(f"CORRECTO: {detalle}")  # muestra el resultado en pantalla
        return resultado  # devuelve el resultado de la operación
    finally:  # finally: se ejecuta siempre
        print(f"Fin de operación {numero}.")  # marca el fin de la operación


# Registra un cliente nuevo validando que no exista otro con la misma identificación
def registrar_cliente(identificacion, nombre, correo, telefono):
    identificacion_normalizada = str(identificacion).strip()  # normaliza la identificación (texto sin espacios)
    if any(c.identificador == identificacion_normalizada for c in clientes):  # busca si algún cliente ya tiene esa identificación
        raise ClienteInvalidoError(  # identificación duplicada
            "Ya existe un cliente con esa identificación"
        )
    cliente = Cliente(identificacion, nombre, correo, telefono)  # crea el cliente (valida sus datos en la clase Cliente)
    clientes.append(cliente)  # lo agrega a la lista interna
    return cliente  # devuelve el cliente creado


# Registra un servicio en la lista, verificando que sea del tipo correcto
def registrar_servicio(servicio):
    if not isinstance(servicio, Servicio):  # debe ser un objeto de tipo Servicio
        raise ParametroInvalidoError(  # parámetro inválido
            "Solo se pueden registrar objetos de tipo Servicio"
        )
    servicios.append(servicio)  # agrega el servicio a la lista interna
    return servicio  # devuelve el servicio registrado


# Crea una reserva nueva validando que el identificador no esté repetido
def crear_reserva(identificador, cliente, servicio, duracion):
    identificador_normalizado = str(identificador).strip()  # normaliza el identificador
    if any(r.identificador == identificador_normalizado for r in reservas):  # busca si ya existe una reserva con ese id
        raise ReservaInvalidaError(  # reserva duplicada
            "Ya existe una reserva con ese identificador"
        )
    reserva = Reserva(identificador, cliente, servicio, duracion)  # crea la reserva (valida cliente, servicio y duración)
    reservas.append(reserva)  # la agrega a la lista interna
    return reserva  # devuelve la reserva creada


# Función principal: ejecuta 17 operaciones de demostración, válidas e inválidas
def main():
    """Ejecuta 17 operaciones de demostración, válidas y no válidas."""
    clientes.clear()  # limpia la lista de clientes
    servicios.clear()  # limpia la lista de servicios
    reservas.clear()  # limpia la lista de reservas
    for clave in estadisticas:  # reinicia los contadores...
        estadisticas[clave] = 0  # ...poniendo cada uno en 0

    print("=" * 58)  # línea decorativa del encabezado
    print("       SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")  # título del programa
    print("=" * 58)

    # 1. Registro válido de cliente.
    cliente_obj = ejecutar(  # ejecuta la operación 1 y guarda el cliente creado
        1,
        "Registrar cliente válido",
        lambda: registrar_cliente(  # registra al cliente con datos válidos
            "CC-1001", "Laura Gómez", "laura@email.com", "3001234567"
        ),
    )

    # 2. Registro inválido de cliente.
    ejecutar(  # se espera un error controlado
        2,
        "Registrar cliente con correo inválido",
        lambda: registrar_cliente(  # registra un cliente...
            "CC-1002", "Carlos Pérez", "correo-invalido", "3011234567"  # ...cuyo correo no tiene formato válido
        ),
    )

    # 3. Intento de identificación duplicada.
    ejecutar(  # se espera error por duplicado
        3,
        "Registrar cliente con identificación duplicada",
        lambda: registrar_cliente(  # misma identificación que el cliente 1
            "CC-1001", "Otra Persona", "otra@email.com", "3021234567"
        ),
    )

    # 4. Creación de servicio de sala.
    sala_obj = ejecutar(  # crea una sala válida y la guarda en la lista
        4,
        "Crear servicio de reserva de sala",
        lambda: registrar_servicio(ReservaSala("Sala Norte", 50000, 12)),  # nombre, tarifa por hora y capacidad
    )

    # 5. Creación de servicio de alquiler de equipo.
    ejecutar(  # crea un equipo válido
        5,
        "Crear servicio de alquiler de equipo",
        lambda: registrar_servicio(
            AlquilerEquipo("Portátil", 15000, seguro=5000)  # nombre, tarifa por hora y seguro fijo
        ),
    )

    # 6. Creación incorrecta de servicio.
    ejecutar(  # se espera error controlado
        6,
        "Crear servicio con tarifa negativa",
        lambda: registrar_servicio(AlquilerEquipo("Proyector", -100)),  # la tarifa negativa es inválida
    )

    # 7. Creación de asesoría especializada.
    ejecutar(  # crea una asesoría válida
        7,
        "Crear servicio de asesoría especializada",
        lambda: registrar_servicio(
            AsesoriaEspecializada("Consultoría Python", 80000, "senior")  # nombre, tarifa por hora y nivel senior
        ),
    )

    # 8. Registro de un servicio temporal no disponible.
    ejecutar(  # crea una sala marcada como no disponible
        8,
        "Crear servicio temporal no disponible",
        lambda: registrar_servicio(
            ReservaSala(
                "Sala en mantenimiento", 40000, 8, disponible=False  # servicio con disponible=False
            )
        ),
    )
    no_disponible_obj = next(  # busca en la lista la sala que está en mantenimiento
        (s for s in servicios if s.nombre == "Sala en mantenimiento"), None  # devuelve el primer servicio con ese nombre, o None si no está
    )

    # 9. Intento de reserva con servicio no disponible.
    if cliente_obj and no_disponible_obj:  # solo se ejecuta si el cliente y la sala existen
        ejecutar(  # se espera error por servicio no disponible
            9,
            "Intentar reservar un servicio no disponible",
            lambda: crear_reserva(  # intenta crear la reserva RES-009 de 2 horas
                "RES-009", cliente_obj, no_disponible_obj, 2
            ),
        )

    # 10. Crear reserva válida.
    reserva_obj = None  # guardará la reserva si se crea bien
    if cliente_obj and sala_obj:  # solo si existen el cliente y la sala
        reserva_obj = ejecutar(  # crea la reserva válida
            10,
            "Crear reserva válida",
            lambda: crear_reserva("RES-010", cliente_obj, sala_obj, 3),  # reserva RES-010 de 3 horas
        )

    # 11. Confirmar reserva.
    if reserva_obj:  # solo si la reserva se creó
        ejecutar(11, "Confirmar reserva", reserva_obj.confirmar)  # pasa la reserva de Pendiente a Confirmada

    # 12. Procesar reserva confirmada.
    if reserva_obj:  # solo si la reserva existe
        ejecutar(12, "Procesar reserva confirmada", reserva_obj.procesar)  # calcula el costo y deja la reserva Procesada

    # 13. Intentar cancelar una reserva ya procesada.
    if reserva_obj:  # solo si la reserva existe
        ejecutar(13, "Cancelar reserva ya procesada", reserva_obj.cancelar)  # se espera error: no se puede cancelar una reserva procesada

    # 14. Intentar crear una reserva sin cliente.
    if sala_obj:  # solo si la sala existe
        ejecutar(  # se espera error por cliente inexistente
            14,
            "Crear reserva sin cliente",
            lambda: crear_reserva("RES-014", None, sala_obj, 1),  # cliente = None
        )

    # 15, 16 y 17. Crear, cancelar y volver a confirmar una reserva.
    if cliente_obj and sala_obj:  # solo si existen el cliente y la sala
        reserva_pendiente = ejecutar(  # crea la segunda reserva
            15,
            "Crear segunda reserva pendiente",
            lambda: crear_reserva("RES-015", cliente_obj, sala_obj, 1),  # reserva RES-015 de 1 hora
        )
        if reserva_pendiente:  # solo si se creó la reserva
            ejecutar(  # cancela la reserva pendiente
                16, "Cancelar reserva pendiente", reserva_pendiente.cancelar
            )
            ejecutar(  # se espera error: no se puede confirmar una reserva cancelada
                17,
                "Intentar confirmar reserva cancelada",
                reserva_pendiente.confirmar,
            )

    print("\n" + "=" * 58)  # línea de separación
    print("RESUMEN DEL SISTEMA")  # resumen final del sistema
    print(f"Clientes registrados: {len(clientes)}")  # cantidad de clientes
    print(f"Servicios registrados: {len(servicios)}")  # cantidad de servicios
    print(f"Reservas registradas: {len(reservas)}")  # cantidad de reservas
    print(f"Operaciones ejecutadas: {estadisticas['total']}")  # total de operaciones ejecutadas
    print(f"Operaciones exitosas: {estadisticas['exitosas']}")  # operaciones correctas
    print(f"Errores controlados: {estadisticas['errores_controlados']}")  # errores propios del sistema, controlados
    print(f"Errores inesperados: {estadisticas['errores_inesperados']}")  # errores imprevistos (deben ser 0)
    print("Los eventos y errores se guardaron en software_fj.log")  # indica dónde quedó el log
    print("=" * 58)
    registrar_evento("Ejecución de demostración finalizada")  # deja constancia en el log del fin de la ejecución


# Ejecuta main() solo si el archivo se corre directamente
if __name__ == "__main__":
    main()  # arranca la demostración

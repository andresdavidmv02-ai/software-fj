"""Pruebas de validación y cálculo de los servicios especializados."""

from excepciones import ErrorSistemaFJ
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala, Servicio


resultados = []


def probar(titulo, funcion, excepciones_esperadas=()):
    """Ejecuta una prueba y comprueba el resultado o la excepción esperada."""
    try:
        resultado = funcion()
    except Exception as error:
        correcto = isinstance(error, excepciones_esperadas)
        if correcto:
            print(
                f"OK   - {titulo}: rechazo controlado "
                f"({type(error).__name__})"
            )
        else:
            print(f"FALLO - {titulo}: {type(error).__name__}: {error}")
    else:
        correcto = not excepciones_esperadas
        if correcto:
            print(f"OK   - {titulo}: {resultado}")
        else:
            print(f"FALLO - {titulo}: se esperaba una excepción")

    resultados.append(correcto)
    return correcto


def main():
    # La clase abstracta no debe poder instanciarse directamente.
    probar(
        "Instanciar Servicio abstracta",
        lambda: Servicio("Servicio de prueba", 100),
        (TypeError,),
    )

    sala = ReservaSala("Sala Norte", 50000, 10)
    equipo = AlquilerEquipo("Portátil", 15000, seguro=5000)
    asesoria = AsesoriaEspecializada("Consultoría Python", 80000, "senior")

    print("\nServicios creados:")
    for servicio in (sala, equipo, asesoria):
        print("-", servicio.mostrar_informacion())

    # Cálculos con distintas combinaciones de argumentos opcionales.
    probar("Sala 3h sin impuesto", lambda: sala.calcular_costo(3))
    probar(
        "Sala 3h con IVA 19%",
        lambda: sala.calcular_costo(3, impuesto=0.19),
    )
    probar(
        "Equipo 2h con IVA y 10% de descuento",
        lambda: equipo.calcular_costo(2, 0.19, 0.10),
    )
    probar("Asesoría senior 2h", lambda: asesoria.calcular_costo(2))

    # Parámetros inválidos y cálculos que deben rechazarse.
    probar(
        "Sala con capacidad 0",
        lambda: ReservaSala("Sala X", 50000, 0),
        (ErrorSistemaFJ,),
    )
    probar(
        "Equipo con tarifa negativa",
        lambda: AlquilerEquipo("Proyector", -100),
        (ErrorSistemaFJ,),
    )
    probar(
        "Asesoría con nivel inventado",
        lambda: AsesoriaEspecializada("Asesoría", 80000, "experto"),
        (ErrorSistemaFJ,),
    )
    probar(
        "Asesoría sin parámetros",
        lambda: AsesoriaEspecializada(),
        (ErrorSistemaFJ,),
    )
    probar(
        "Impuesto fuera de rango",
        lambda: sala.calcular_costo(2, impuesto=5),
        (ErrorSistemaFJ,),
    )
    probar(
        "Descuento del 100% (costo cero)",
        lambda: sala.calcular_costo(2, descuento=1),
        (ErrorSistemaFJ,),
    )
    probar(
        "Duración no finita",
        lambda: sala.calcular_costo(float("inf")),
        (ErrorSistemaFJ,),
    )

    aprobadas = sum(resultados)
    fallidas = len(resultados) - aprobadas
    print(f"\nResultado de pruebas: {aprobadas} aprobadas, {fallidas} fallidas.")
    if fallidas:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

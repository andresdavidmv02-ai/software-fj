"""Pruebas de validación y cálculo de los servicios especializados."""

from excepciones import ErrorSistemaFJ  # excepción base: agrupa todos los errores propios del sistema
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala, Servicio  # clases a probar


resultados = []  # guarda True/False de cada prueba para contar aprobadas y fallidas al final


def probar(titulo, funcion, excepciones_esperadas=()):
    """Ejecuta una prueba y comprueba el resultado o la excepción esperada."""
    # Si excepciones_esperadas está vacío, la prueba debe terminar SIN error;
    # si trae tipos de excepción, la prueba debe terminar lanzando alguno de ellos.
    try:
        resultado = funcion()  # ejecuta el código que se está probando
    except Exception as error:  # se produjo un error durante la prueba
        # La prueba es correcta solo si el error es de un tipo esperado
        correcto = isinstance(error, excepciones_esperadas)
        if correcto:
            print(  # el error era el esperado: el sistema rechazó el dato de forma controlada
                f"OK   - {titulo}: rechazo controlado "
                f"({type(error).__name__})"
            )
        else:
            # el error NO era el esperado: la prueba falla
            print(f"FALLO - {titulo}: {type(error).__name__}: {error}")
    else:  # no hubo ningún error
        # Es correcto solo si no se esperaba ninguna excepción
        correcto = not excepciones_esperadas
        if correcto:
            print(f"OK   - {titulo}: {resultado}")  # muestra el resultado calculado
        else:
            # se esperaba un error pero no ocurrió: la prueba falla
            print(f"FALLO - {titulo}: se esperaba una excepción")

    resultados.append(correcto)  # guarda el resultado de esta prueba
    return correcto  # devuelve True si la prueba fue aprobada


def main():
    # La clase abstracta no debe poder instanciarse directamente.
    probar(
        "Instanciar Servicio abstracta",  # nombre de la prueba
        lambda: Servicio("Servicio de prueba", 100),  # intenta crear la clase abstracta
        (TypeError,),  # Python lanza TypeError al instanciar una clase abstracta
    )

    # Servicios válidos, uno de cada tipo
    sala = ReservaSala("Sala Norte", 50000, 10)  # nombre, tarifa por hora, capacidad
    equipo = AlquilerEquipo("Portátil", 15000, seguro=5000)  # nombre, tarifa por hora, seguro fijo
    asesoria = AsesoriaEspecializada("Consultoría Python", 80000, "senior")  # nombre, tarifa, nivel

    print("\nServicios creados:")
    for servicio in (sala, equipo, asesoria):  # recorre los tres servicios (polimorfismo)
        print("-", servicio.mostrar_informacion())  # cada clase se describe a su manera

    # Cálculos con distintas combinaciones de argumentos opcionales.
    probar("Sala 3h sin impuesto", lambda: sala.calcular_costo(3))  # solo horas
    probar(
        "Sala 3h con IVA 19%",
        lambda: sala.calcular_costo(3, impuesto=0.19),  # horas + impuesto
    )
    probar(
        "Equipo 2h con IVA y 10% de descuento",
        lambda: equipo.calcular_costo(2, 0.19, 0.10),  # horas + impuesto + descuento
    )
    probar("Asesoría senior 2h", lambda: asesoria.calcular_costo(2))  # incluye el recargo senior

    # Parámetros inválidos y cálculos que deben rechazarse.
    probar(
        "Sala con capacidad 0",
        lambda: ReservaSala("Sala X", 50000, 0),  # la capacidad debe ser positiva
        (ErrorSistemaFJ,),  # se espera una excepción propia del sistema
    )
    probar(
        "Equipo con tarifa negativa",
        lambda: AlquilerEquipo("Proyector", -100),  # la tarifa debe ser mayor que cero
        (ErrorSistemaFJ,),
    )
    probar(
        "Asesoría con nivel inventado",
        lambda: AsesoriaEspecializada("Asesoría", 80000, "experto"),  # solo existen junior y senior
        (ErrorSistemaFJ,),
    )
    probar(
        "Asesoría sin parámetros",
        lambda: AsesoriaEspecializada(),  # faltan nombre y tarifa
        (ErrorSistemaFJ,),
    )
    probar(
        "Impuesto fuera de rango",
        lambda: sala.calcular_costo(2, impuesto=5),  # el impuesto debe estar entre 0 y 1
        (ErrorSistemaFJ,),
    )
    probar(
        "Descuento del 100% (costo cero)",
        lambda: sala.calcular_costo(2, descuento=1),  # un costo de cero es inconsistente
        (ErrorSistemaFJ,),
    )
    probar(
        "Duración no finita",
        lambda: sala.calcular_costo(float("inf")),  # infinito no es una duración válida
        (ErrorSistemaFJ,),
    )

    aprobadas = sum(resultados)  # True cuenta como 1, así que la suma da las pruebas aprobadas
    fallidas = len(resultados) - aprobadas  # el resto son las fallidas
    print(f"\nResultado de pruebas: {aprobadas} aprobadas, {fallidas} fallidas.")
    if fallidas:
        raise SystemExit(1)  # termina con código de error si alguna prueba falló


if __name__ == "__main__":  # solo se ejecuta si se corre este archivo directamente
    main()

# Juego de cartas "Caida"
import time
import os
import errores_personalizados as e_p
import random

Dificultad = tuple(["facil", "normal", "dificil"])
orden_valido = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]
Puntos_para_ganar = 24
puntos_j1 = 0
puntos_j2 = 0
cartas_recogidas_j1 = 0
cartas_recogidas_j2 = 0
ultima_carta = 0


# verificamos dificultad
def Verificar_dif():
    print(f"dificultades disponibles: {Dificultad}")
    dif_select = str(input("Escriba la dificultad deseada:")).strip().lower()
    if dif_select not in Dificultad:
        raise ValueError(
            "Dificultad invalida, por favor seleccione las opciones disponibles"
        )

    return dif_select


# verificamos el puntaje #pendiente
def Verficar_punt():
    """nueva_puntuacion = int(
        input(
            "Coloque los puntos necesarios para ganar (de manera predeterminada son 20 puntos): "
        )
    )

    if nueva_puntuacion <= 0 or nueva_puntuacion is None:
        raise e_p.Error_puntuacion(
            "Hubo un error al elegir la puntuacion para ganar. Elija un numero valido"
        )
    else:
        Puntos_para_ganar = nueva_puntuacion
    """
    return 20


# verificar opciones generales
def Verificar_opciones():

    try:
        print()
        dificultad = Verificar_dif()
        puntuacion = Verficar_punt()
        return dificultad, puntuacion
    except ValueError as x:
        print(f"{x}.Saliendo....")
        time.sleep(3)
        exit()
    except e_p.Error_puntuacion as z:
        print(f"{z}.Saliendo....")
        time.sleep(3)
        exit()


# desarrollo del juego
def juego():
    global puntos_j1, puntos_j2
    global cartas_recogidas_j1, cartas_recogidas_j2
    cartas_jugador1 = list()
    cartas_jugador2 = list()
    turno_jugador = False
    ultimo_en_tomar = ""

    baraja = crear_baraja()
    mesa, baraja, turno_jugador = poner_mesa(baraja, turno_jugador)

    cartas_jugador1, cartas_jugador2 = distribuir_cartas(
        cartas_jugador1, cartas_jugador2, baraja
    )

    puntos_j1 = verificar_cantos(cartas_jugador1)
    puntos_j2 = verificar_cantos(cartas_jugador2)
    time.sleep(3)
    os.system("cls")
    while puntos_j1 <= Puntos_para_ganar and puntos_j2 <= Puntos_para_ganar:

        for ronda in range(0, 6):
            print("♦" * 60)
            print(f"                     RONDA {ronda+1}/6")
            print("♦" * 60 + "\n")
            print("╔════════════════════════════════════════════════════╗")
            print("║                    PUNTUACIONES                    ║")
            print("╠════════════════════════════════════════════════════╣")
            print(
                f"║   Jugador 1: {puntos_j1} puntos"
                + " " * (29 - len(str(puntos_j1)))
                + "  ║"
            )
            print(
                f"║   Jugador 2: {puntos_j2} puntos"
                + " " * (29 - len(str(puntos_j2)))
                + "  ║"
            )
            print("╚════════════════════════════════════════════════════╝\n")

            if mesa:
                print(f"│  {mesa}                                     │")
            else:
                print("│               🃏  Mesa vacía  🃏              │")

            print("└────────────────────────────────────────────────────┘\n")
            print("─" * 60)

            if turno_jugador:
                turno_jugador, ultimo_en_tomar = soltar_carta(
                    cartas_jugador1, mesa, turno_jugador, ultimo_en_tomar
                )
                # verificar si el jugador limpio la mesa, si es asi gana 4 puntos
                if len(mesa) == 0:
                    print("\n" + "!" * 60)
                    print("   ¡¡¡ EL JUGADOR 1 SE HA LLEVADO LA MESA !!!")
                    print("   ¡¡¡ +4 PUNTOS !!!")
                    print("!" * 60)
                    time.sleep(3)
                    puntos_j1 += 4

            else:
                turno_jugador, ultimo_en_tomar = soltar_carta(
                    cartas_jugador2, mesa, turno_jugador, ultimo_en_tomar
                )

                if len(mesa) == 0:
                    print("\n" + "!" * 60)
                    print("   ¡¡¡ EL JUGADOR 2 SE HA LLEVADO LA MESA !!!")
                    print("   ¡¡¡ +4 PUNTOS !!!")
                    print("!" * 60)
                    time.sleep(3)
                    puntos_j2 += 4
                if puntos_j1 >= Puntos_para_ganar or puntos_j2 >= Puntos_para_ganar:
                    break
            os.system("cls")

        if len(baraja) == 0:
            if len(mesa) != 0:
                if ultimo_en_tomar == "j1":
                    cartas_recogidas_j1 += len(mesa)

                else:
                    cartas_recogidas_j2 += len(mesa)

            print("Barajando cartas....")
            conteo_cartas()
            baraja = crear_baraja()
            mesa, baraja, turno_jugador = poner_mesa(baraja, turno_jugador)

        print("Distribuyendo cartas....")
        time.sleep(3)

        cartas_jugador1, cartas_jugador2 = distribuir_cartas(
            cartas_jugador1, cartas_jugador2, baraja
        )

        puntos_j1 += verificar_cantos(cartas_jugador1)
        puntos_j2 += verificar_cantos(cartas_jugador2)
        time.sleep(3)

    else:

        if puntos_j1 >= Puntos_para_ganar and puntos_j1 > puntos_j2:
            print(f"Ha ganado el jugador 1 con:{puntos_j1} puntos.")
            time.sleep(3)

        else:
            print(f"Ha ganado el jugador 2 con:{puntos_j2} puntos.")
            time.sleep(3)


def poner_mesa(baraja: list, turno_jugador):
    global puntos_j1, puntos_j2
    mesa = list()
    puntos_ganados = 0
    mesa_valida = [4, 3, 2, 1]
    mesa_valida2 = [1, 2, 3, 4]
    if turno_jugador:
        inicio_elegido = int(input("Escribe con que carta empezar la mesa 4 o 1:"))

        while not (inicio_elegido == 4 or inicio_elegido == 1):
            inicio_elegido = int(input("Por favor elegir entre 4 o 1:"))

        turno_jugador = False
    else:
        inicio_elegido = random.choice([4, 1])
        turno_jugador = True

    i = 0
    while len(mesa) < 4:
        if baraja[0] not in mesa:
            mesa.append(baraja[0])
            del baraja[0]

            if mesa[i] == mesa_valida[i] or mesa[i] == mesa_valida2[i]:
                puntos_ganados += mesa[i]
            i += 1
        else:
            baraja.append(baraja[0])
            del baraja[0]

    if turno_jugador:
        puntos_j2 += puntos_ganados

    else:
        puntos_j1 += puntos_ganados

    return mesa, baraja, turno_jugador


# creacion de baraja
def crear_baraja():
    baraja_cartas = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12] * 4
    random.shuffle(baraja_cartas)
    return baraja_cartas


# verificar la existencia de cantos
def verificar_cantos(mazo_jugador: list):

    mazo_ordenado = mazo_jugador.copy()
    mazo_ordenado.sort()
    idx0 = orden_valido.index(mazo_ordenado[0])
    idx1 = orden_valido.index(mazo_ordenado[1])
    idx2 = orden_valido.index(mazo_ordenado[2])
    indices = sorted([idx0, idx1, idx2])

    if mazo_ordenado == [1, 11, 12]:
        print("Registro !")
        return 8

    elif len(set(mazo_ordenado)) == 1:
        print("Trivilin !")
        return Puntos_para_ganar

    elif (
        (mazo_ordenado[0] == mazo_ordenado[1] and abs(idx0 - idx2) == 1)
        or (mazo_ordenado[0] == mazo_ordenado[2] and abs(idx0 - idx1) == 1)
        or (mazo_ordenado[1] == mazo_ordenado[2] and abs(idx1 - idx0) == 1)
    ):
        print("Vigia !")
        return 7

    elif (
        mazo_ordenado[0]
        and (mazo_ordenado[1] == mazo_ordenado[2])
        or mazo_ordenado[2]
        and (mazo_ordenado[1] == mazo_ordenado[0])
    ):
        print("Ronda !")
        if (
            mazo_ordenado[0] == 12
            and mazo_ordenado[1] == 12
            or mazo_ordenado[1] == 12
            and mazo_ordenado[2] == 12
        ):
            return 4
        elif (
            mazo_ordenado[0] == 11
            and mazo_ordenado[1] == 11
            or mazo_ordenado[1] == 11
            and mazo_ordenado[2] == 11
        ):
            return 3

        elif (
            mazo_ordenado[0] == 10
            and mazo_ordenado[1] == 10
            or mazo_ordenado[1] == 10
            and mazo_ordenado[2] == 10
        ):
            return 2

        else:
            return 1

    elif indices[1] == indices[0] + 1 and indices[2] == indices[1] + 1:
        print("Patrulla !")
        return 6
    else:
        return 0


# sistema de distribucion de puntos
def sistema_de_puntos(puntosj1, puntosj2):
    pass


# distribucion de cartas
def distribuir_cartas(p1, p2, baraja):
    p1 = baraja[0:3]

    del baraja[0:3]
    p2 = baraja[0:3]

    del baraja[0:3]
    return p1, p2


# verificacion de la "caida"
def verificar_caida(ultima_carta, carta_actual):

    if ultima_carta == carta_actual:
        print(f"Hubo una caida de: {carta_actual} !!!")
        time.sleep(3)
        if carta_actual in orden_valido[0:7]:
            return 1
        elif carta_actual == 10:
            return 2
        elif carta_actual == 11:
            return 3
        elif carta_actual == 12:
            return 4
    else:
        return 0


def soltar_carta(cartas: list, mesa: list, turno_jugador, ultimo):
    global ultima_carta
    global puntos_j1, puntos_j2
    global cartas_recogidas_j1

    if cartas and turno_jugador:
        eleccion = int(input((f"Elija la posicion de la carta a soltar{cartas}: ")))
        while eleccion > len(cartas):
            eleccion = int(
                input(
                    "Las posiciones de las cartas son 1,2,3. Elegir el numero correcto:"
                )
            )
        # condicional para saber si la carta no está en la mesa
        if not (cartas[eleccion - 1] in mesa):

            ultima_carta = cartas[eleccion - 1]
            mesa.append(cartas[eleccion - 1])

            cartas.pop(eleccion - 1)
        # lo opuesto al condicional
        else:
            puntos_j1 += verificar_caida(ultima_carta, cartas[eleccion - 1])
            ultima_carta = cartas[eleccion - 1]
            cartas_recogidas_j1 = recoger_cartas(mesa, cartas[eleccion - 1])
            cartas.pop(eleccion - 1)
            ultimo = "j1"
        turno_jugador = False

    elif cartas:

        eleccion = random.choice(cartas)
        print(f"El jugador 2 soltó la carta:{eleccion}")
        time.sleep(3)

        if not (eleccion in mesa):

            ultima_carta = eleccion
            mesa.append(eleccion)
            cartas.remove(eleccion)
        # lo opuesto al condicional
        else:
            puntos_j2 += verificar_caida(ultima_carta, eleccion)
            ultima_carta = eleccion
            cartas.remove(eleccion)
            recoger_cartas(mesa, eleccion)
            ultimo = "j2"

        turno_jugador = True

    return turno_jugador, ultimo


# observar reglas de juego
def ver_reglas():
    print("En el siguiente enlace podrá consultar las reglas del juego:\n")
    print(
        "https://steemit.com/spanish/@joriangel/juego-de-cartas-caida-explicado-venezuela"
    )

    input("Presione enter para continuar.")
    os.system("cls")


def recoger_cartas(mesa: list, eleccion):
    se_puede_recoger = True
    cartas_tomadas = 0

    while se_puede_recoger:

        if eleccion == 8:
            eleccion = 10

        elif eleccion in mesa:
            cartas_tomadas += 1
            mesa.remove(eleccion)
            eleccion += 1
        else:
            cartas_tomadas += 1
            se_puede_recoger = False

    return cartas_tomadas


def conteo_cartas():
    global puntos_j1, puntos_j2
    global cartas_recogidas_j2, cartas_recogidas_j1

    cartas_recogiasj2 = 40 - cartas_recogidas_j1

    if cartas_recogidas_j1 > 20:
        puntos_j1 += cartas_recogidas_j1 - 20
        print(
            f"El jugador 1 se ha llevado {cartas_recogidas_j1 - 20} puntos por su pila de descarte"
        )

    else:
        puntos_j2 += cartas_recogiasj2 - 20
        print(
            f"El jugador 2 se ha llevado { cartas_recogiasj2 - 20} puntos por su pila de descarte"
        )
    time.sleep(3)
    cartas_recogidas_j1 = 0
    cartas_recogiasj2 = 0


def mostrar_menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print("╔════════════════════════════════════════════════════╗")
        print("║                                                    ║")
        print("║              🃏   C A Í D A   🃏                   ║")
        print("║           Juego de cartas estratégico              ║")
        print("║                                                    ║")
        print("╠════════════════════════════════════════════════════╣")
        print("║                                                    ║")
        print("║        [1]  🎴  Empezar partida                    ║")
        print("║        [2]  📜  Ver reglas                         ║")
        print("║        [3]  🚪  Salir                              ║")
        print("║                                                    ║")
        print("╠════════════════════════════════════════════════════╣")
        print("║                                                    ║")

        eleccion = input("║    ► Elija una opción (1-3): ").strip()

        match eleccion:
            case "1":
                os.system("cls")
                print("║                                                    ║")
                print("║    🎯 Iniciando partida...                         ║")
                print("╚════════════════════════════════════════════════════╝")
                time.sleep(1)
                juego()
            case "2":
                ver_reglas()
            case "3":
                print("║                                                    ║")
                print("║    👋 Gracias por jugar a Caída!                   ║")
                print("║                                                    ║")
                print("╚════════════════════════════════════════════════════╝")
                time.sleep(2)
                exit()
            case _:
                print("║                                                    ║")
                print("║    ❌ Opción no válida. Intente de nuevo.          ║")
                print("╚════════════════════════════════════════════════════╝")
                time.sleep(1.5)


mostrar_menu()

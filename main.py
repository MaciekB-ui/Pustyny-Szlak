from character import Rover
import random
from world import EasyWorld, World, create_world
import turtle
from utils import get_not_empty_input
from constants import TURTLE_MOVE_SCALE


def start_game(ready: str) -> None:
    choice = input(ready).strip().lower()
    if choice == "tak":
        return
    else:
        print("\n=== KONIEC SYMULACJI ===")
        quit()


def staring_angle() -> int:
    possible_angle: set[str] = {"0", "45", "90", "135", "180", "225", "270", "315"}

    while True:
        angle = input("Podaj kierunek (0, 45, 90, 135, 180, 225, 270, 315): ").strip()
        if angle in possible_angle:
            return int(angle)
        else:
            print(
                "Niepoprawny kąt. Wprowadź jeden z: 0, 45, 90, 135, 180, 225, 270, 315."
            )


def dig(rover: Rover, world: World) -> None:
    
    pos = (rover.x, rover.y)

    dig_count = world.dug_positions[pos]

    max_digs = rover.max_dig_level

    if dig_count >= max_digs:
        print("To miejsce zostało już całkowicie przekopane.")
        return

    rover.fuel -= 1
    print("Kopanie... (-1 paliwa)")

    world.dug_positions[pos] += 1

    if random.random() < world.fuel_chance:
        fuel_found = random.randint(10, 30)
        rover.fuel += fuel_found
        print(f"Znalazłeś paliwo! (+{fuel_found} paliwa)")
        return

    if random.random() < world.engine_part_chance:
        print("Znalazłeś część silnika!")
        if rover.upgrade_engine():
            print("\n SILNIK ULEPSZONY!")
            print(f"Poziom silnika: {rover.engine_level}")
            print(f"Aktualne spalanie: {rover.fuel_consumption} paliwa/ruch")
        return

    if random.random() < world.armor_part_chance:
        rover.armor_durability += 20
        print("Znalazłeś część pancerza!")
        print("Trwałość pancerza pojazdu zwiększona o 20.")
        print(f"Trwałość pancerza pojazdu: {rover.armor_durability}")
        return

    if random.random() < world.map_fragment_chance:
        print("Znaleziono fragment mapy!")
        print("Przybliżona lokalizacja artefaktu:")
        print(f"X: około {world.artifact_x + random.randint(-5, 5)}")
        print(f"Y: około {world.artifact_y + random.randint(-5, 5)}")
        return

    print(" Nic nie znaleziono.")


def simulation(rover: Rover, world: World, step: int, score: int) -> tuple[int, int]:

    turtle.setup(width=world.width, height=world.height, startx=rover.x, starty=rover.y)
    root = turtle.getscreen().getcanvas().winfo_toplevel()
    root.resizable(False, False)
    start = turtle.Turtle()
    start.hideturtle()
    start.penup()
    start.goto(0, 0)
    start.dot(3, "green")
    start.goto(0, -20)
    start.write("START", align="center")

    score = 0

    artifact_found = False
    artifact_collected = False

    print("\n=== START SYMULACJI ===")

    while True:
        if not rover.has_fuel:
            print("\nBrak paliwa. Koniec wyprawy.")
            print("\n=== KONIEC SYMULACJI ===")
            break

        if not rover.has_armor:
            print("\nPojazd został zniszczony. Koniec wyprawy.")
            print("\n=== KONIEC SYMULACJI ===")
            break

        if world.is_out_of_bounds(rover.x, rover.y):
            print("\n WYJŚCIE POZA MAPĘ!")
            print("Misja zakończona niepowodzeniem.")
            break

        print("\nAkcje:")
        print("1 - Ruch do przodu")
        print("2 - Obrót w lewo")
        print("3 - Obrót w prawo")
        print("4 - Kopanie")
        print("9 - Zakończ wyprawę")

        action = input("Wybierz akcję: ")

        print(f"Pozycja przed ruchem: ({rover.x}, {rover.y})")
        print(f"Paliwo przed ruchem: {rover.fuel}")
        print(f"Kąt przed ruchem: {rover.angle}°")
        print(f"\n=== KROK {step} ===")

        if action == "1":
            new_x, new_y = rover.move_forward(1)
            turtle.goto(rover.x * TURTLE_MOVE_SCALE, rover.y * TURTLE_MOVE_SCALE)

            print("\nRuch wykonany o 1 jednostkę.")

        elif action == "2":
            rover.rotate(45)
            turtle.right(45)

            print("\nObrót w lewo o 45°")

        elif action == "3":
            rover.rotate(-45)
            turtle.left(-45)

            print("\nObrót w prawo o 45°")

        elif action == "4":
            dig(rover, world)
            print("\nKopanie w poszukiwaniu zasobów...")

        elif action == "9":
            print("\nZakończono wyprawę.")
            print("\n=== KONIEC SYMULACJI ===")
            quit()

        elif action == "0":
            print("\nMusisz cos zrobić, nie możesz tak tu czekać!")

        else:
            print("\nNiepoprawna akcja.")
            continue

        print(f"Pozycja po ruchu: ({rover.x}, {rover.y})")
        print(f"Paliwo po ruchu: {rover.fuel}")
        print(f"Kąt po ruchu: {rover.angle}°")
        print(f"Trwałość pancerza pojazdu: {rover.armor_durability}")

        is_storm_step = step % world.storm_interval == 0
        if is_storm_step and random.random() < world.storm_chance:
            damage = random.randint(10, 30)
            rover.armor_durability -= damage

            print("\n=== BURZA PIASKOWA! ===")
            print(f"Pancerz uszkodzony: -{damage}")
            print(f"Aktualna wytrzymałość pancerza: {rover.armor_durability}")

        has_moved = action == "1"
        if has_moved and random.random() < world.oasis_chance:
            miracle = random.randint(50, 80)
            rover.armor_durability += miracle

            print("\n=== Znaleziono OAZĘ! ===")
            print(f"+{miracle} punktów wytrzymałości pancerza")

        if (
            not artifact_found
            and rover.x == world.artifact_x
            and rover.y == world.artifact_y
        ):
            artifact_found = True
            score += 100
            print("\n=== ODNALEZIONO STAROŻYTNY ARTEFAKT! ===")
            print(" +100 punktów do wyniku!")
            print("Musisz wrócić do punktu startowego (0,0).")
            start.goto(world.artifact_x * TURTLE_MOVE_SCALE, world.artifact_y * TURTLE_MOVE_SCALE)
            start.dot(5, "gold")
            start.goto(world.artifact_x * TURTLE_MOVE_SCALE, world.artifact_y * TURTLE_MOVE_SCALE - 20)
            start.write("ARTEFAKT", align="center")

        if artifact_found and not artifact_collected and rover.x == 0 and rover.y == 0:
            artifact_collected = True
            score += 100
            print("\n=== MISJA UKOŃCZONA! ===")
            print("Artefakt został bezpiecznie dostarczony.")
            print(" +100 punktów do wyniku!")
            break

        print(f"Trwałość pancerza pojazdu: {rover.armor_durability}")

        step += 1
    return score, step


def main():
    x = 0
    y = 0
    angle = 0
    fuel = 200
    armor_durability = 100
    score = 0
    step = 0

    turtle.clearscreen()

    print("=== Pustynny Szlak ===")
    print("Wprowadź parametry startowe wyprawy.\n")
    name = get_not_empty_input("Nazwa użytkownika: ")
    codename = get_not_empty_input("Kryptonim wyprawy: ")

    difficulty = (
        input("Wybierz trudność: easy / medium / hard / extreme\n").strip().lower()
    )
    try:
        world = create_world(difficulty)
    except ValueError:
        print("Nieznany poziom trudności. Ustawiono na 'easy' domyślnie.")
        world = EasyWorld()

    angle = staring_angle()
    turtle.setheading(angle)

    rover = Rover(name, x, y, angle, fuel, armor_durability)

    print("\n=== PODSUMOWANIE STARTU ===")
    print(f"||Nazwa użytkownika: {name}")
    print(f"||Kryptonim wyprawy: {codename}")
    print(f"||Poziom trudności: {difficulty}")
    print(f"||Trwałość pancerza pojazdu: {rover.armor_durability}")
    print(f"||Start: ({x}, {y})")
    print(f"||Kąt: {angle}°")
    print(f"||Startowa ilość paliwa: {fuel}")
    print(f"||Wielkość mapy: {world.width // 4}x{world.height // 4}")
    print("||Cel wyprawy: odnaleźć starożytny artefakt i wrócić do punktu startowego.")
    print("\n=== INSTRUKCJA I ZASADY GRY ===")
    print("CEL GRY:")
    print(
        "Twoim zadaniem jest odnaleźć starożytny artefakt i wrócić z nim do punktu startowego (0,0)."
    )

    print("\nSTEROWANIE:")
    print("1 - ruch do przodu")
    print("2 - obrót w prawo (45°)")
    print("3 - obrót w lewo (45°)")
    print("4 - kopanie w miejscu")
    print("9 - zakończenie wyprawy")

    print("\nZASOBY:")
    print("- Paliwo: potrzebne do ruchu, zużywa się przy każdym kroku")
    print("- Pancerz: chroni przed burzami i uszkodzeniami pojazdu")

    print("\nSILNIK I ULEPSZENIA:")
    print("- Na początku każdy ruch zużywa 4 jednostki paliwa")
    print("- Podczas kopania możesz znaleźć części silnika")
    print("- Każda część silnika ulepsza pojazd")
    print("- Ulepszony silnik zmniejsza zużycie paliwa na ruch")
    print("- Dzięki temu możesz eksplorować dłużej i dalej")

    print("\nEKSPLOATACJA:")
    print("- Kopanie może dać paliwo, części, fragmenty mapy lub nic")
    print("- Fragmenty mapy pokazują przybliżoną lokalizację artefaktu")
    print("- Dzięki nim możesz zawęzić obszar poszukiwań")

    print("\nZDARZENIA LOSOWE:")
    print("- Burze piaskowe: uszkadzają pancerz")
    print("- Oazy: regenerują pancerz")

    print("\nZASADY GRY:")
    print("- Utrata paliwa = koniec gry")
    print("- Zniszczenie pancerza = koniec gry")
    print("- Wyjście poza mapę = koniec gry")
    print("- Artefakt można zdobyć tylko raz")
    print("- Punkty naliczają się tylko za znalezienie i zwrot artefaktu")

    print("\nPUNKTACJA:")
    print("+100 pkt za znalezienie artefaktu")
    print("+100 pkt za powrót do bazy z artefaktem")
    print("Maksymalny wynik: 200 punktów")

    print("\nPowodzenia w misji!")
    print("Czy jesteś gotowy na wyprawę? (tak/nie)")
    start_game("Wprowadź swoją odpowiedź: ")

    score, step = simulation(rover, world, step=step, score=score)
    max_score = 200
    percent = int((score / max_score) * 100)

    if percent >= 200:
        print("\n=== RAPORT ===")
        print("Gratulacje! Osiągnąłeś wysoki wynik.")
    elif percent >= 100:
        print("\n=== RAPORT ===")
        print("Dobrze wykonana praca. Możesz poprawić wynik w kolejnych próbach.")
    else:
        print("\n=== RAPORT ===")
        print("Konieczna praca nad poprawą wyniku.")
    print(f"||Nazwa wyprawy: {rover.name}")
    print(f"||Końcowa pozycja: ({rover.x}, {rover.y})")
    print(f"||Poziom trudności: {difficulty}")
    print(f"||Pozostałe paliwo: {rover.fuel}")
    print(f"||Spalanie na ruch: {rover.fuel_consumption}")
    print(f"||Poziom silnika: {rover.engine_level}")
    print(f"||Trwałość pancerza pojazdu: {rover.armor_durability}")
    print(f"||Liczba kroków: {step}")
    print(f"||Końcowy wynik: {score}")
    print("\n=== KONIEC SYMULACJI ===")


if __name__ == "__main__":
    while True:
        main()
        again = input("\nCzy chcesz opuścić grę? (tak/nie): ").strip().lower()

        if again == "nie":
            print("Restart gry.")
        elif again == "tak":
            print("\nKoniec programu.")
            break
        else:
            print("Niepoprawna odpowiedź. Wpisz 'tak' albo 'nie'.")

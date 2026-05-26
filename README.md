# Pustynny Szlak

## Opis projektu
Pustynny Szlak to gra eksploracyjna, w której sterujesz łazikiem poruszającym się po pustynnej mapie. Świat jest losowo generowany, a Twoim celem jest odnalezienie starożytnego artefaktu i powrót z nim do bazy (0,0).

W trakcie gry musisz zarządzać paliwem, stanem pancerza oraz reagować na losowe zdarzenia takie jak burze piaskowe i oazy.

---

## Jak uruchomić grę
1. Otwórz projekt w Visual Studio Code  
2. Upewnij się, że masz zainstalowanego Pythona (3.11+)  
3. Otwórz terminal w miejscu gdzie są pliki projektowe
4. Uruchom grę używając komendy "python main.py"  
5. Gra uruchomi oraz wyświetli okno Turtle  

Nie są wymagane żadne dodatkowe biblioteki.

---

## Struktura projektu

- `main.py` – główny plik gry, obsługa rozgrywki i interakcji z graczem  
- `character.py` – klasa Rover (ruch, paliwo, ulepszenia, stan pojazdu)  
- `world.py` – definicje świata, poziomy trudności i generowanie artefaktu  
- `constants.py` – stałe używane w grze (skale mapy, ruch Turtle)  
- `utils.py` – funkcje pomocnicze (np. pobieranie danych od użytkownika)  

---

## O co chodzi w grze
Gracz steruje łazikiem poruszającym się po pustyni. Każdy ruch zużywa paliwo, a mapa jest pełna losowych zdarzeń i zasobów.

Celem jest:
- odnalezienie ukrytego artefaktu  
- powrót z nim do punktu startowego (0,0)

---

## Sterowanie

- `1` – ruch do przodu  
- `2` – obrót w lewo (45°)  
- `3` – obrót w prawo (45°)  
- `4` – kopanie  
- `9` – zakończenie wyprawy  

Każda akcja wymaga potwierdzenia Enterem w terminalu.

---

## Mechaniki gry

### Eksploracja
Łazik porusza się po mapie krok po kroku. Każdy ruch zużywa paliwo zależne od poziomu silnika.

---

### Kopanie
Podczas kopania można znaleźć:
- paliwo  
- części silnika  
- części pancerza  
- fragmenty mapy  
- nic  

Każde pole ma ograniczoną liczbę możliwych wykopów.

---

### Ulepszenia
- Części silnika pozwalają ulepszać pojazd  
- Każdy poziom silnika zmniejsza zużycie paliwa na ruch  
- Ulepszenia pozwalają dłużej eksplorować mapę  

---

### Fragmenty mapy
Fragmenty mapy pokazują przybliżone położenie artefaktu, co ułatwia jego odnalezienie.

---

### Zdarzenia losowe
- Burze piaskowe – zmniejszają pancerz  
- Oazy – regenerują pancerz  

---

## Świat gry
Gra posiada kilka poziomów trudności:

- easy  
- medium  
- hard  
- extreme  

Różnią się one:
- wielkością mapy  
- szansami na zasoby  
- częstotliwością zdarzeń losowych  

---

## Zasady gry
Gra kończy się, gdy:
- skończy się paliwo  
- pancerz spadnie do 0  
- wyjdziesz poza mapę  
- zakończysz grę ręcznie  

Artefakt można zdobyć tylko raz, a punkty naliczane są za jego znalezienie i powrót do bazy.

---

## Punktacja
- +100 punktów – znalezienie artefaktu  
- +100 punktów – powrót z artefaktem do bazy  

Maksymalny wynik: 200 punktów
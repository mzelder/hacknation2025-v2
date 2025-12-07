# Anonimizator
Narzędzie do anonimizowania danych wrażliwych takich jak imie, nazwisko, pesel, data urodzin itd.

Wykorzystaliśmy podejście typu: Hybryda Herbert + RegEx

## Struktura projektu
- `anonimizer.py` – komponent orkiestrujący wykrywanie i zamianę.
- `regex_handler.py` – wzorce regex, etykiety oraz mechanizm automatycznego uruchamiania/zamiany.
- `main.py` – prosty punkt startowy (demo).
- `anonymized.txt` / `orig.txt` – przykładowe pliki wejściowe.

## Użycie komponentu
Zapis do zmiennej jako string
```python
from anonimizer import Anonimizer

anon = Anonimizer(text="Nazywam się Jan Kowalski, mój PESEL to 90010112345. Mieszkam w Warszawie przy ulicy Długiej 5.") 

result = anon.anonymize_to_string()
print(result)   
```
```
Output: Nazywam się [name] [surname], mój PESEL to [pesel].
Mieszkam w [address].
```

Zapis do pliku
```python
from anonimizer import Anonimizer

anon = Anonimizer(file_name="test.txt")
anon.anonymize_to_string("output.txt")
```
```
output.txt

„Hej, piszę bo nie mam już do kogo. Jestem [name] [age] lat, [sex] Mieszkam w [city] blisko centrum [address] jakbyś potrzebował/a szczegółów. Mój PESEL to [pesel], a numer dowodu [document-number] – ostatnio przy rejestracji do lekarza kazali mi podawać, więc pewnie i tu się przyda. Problem w tym, że mój chłopak (a właściwie już ex) zaczął mnie stalkować. Wysyła wiadomości typu 'Wiem, że jesteś w domu, [name] widziałem światło'. Zmieniłem numer (nowy to [phone]), ale on i tak znajduje sposoby. Boję się wychodzić sam, a w pracy dzwonił podając się za kuriera. Czy mogę gdzieś to zgłosić, żeby nie było śladu, że to ja? Boję się, że jak pójdę na policję, to on się wkurzy jeszcze bardziej. Jak ty byś to ogarnął/a?”
```

## Jak to działa?
- Wstępna detekcja wzorców: moduł `regex_handler.py` zawiera stałe `REGEX_*` oraz mapę `LABELS`. Funkcja `RegexSet.replace_all` automatycznie znajduje zdefiniowane wzorce i zamienia dopasowania na etykiety (np. `[phone]`, `[email]`, `[pesel]`).
- Anonimizacja kontekstowa modelem: po wstępnej zamianie regexów `Anonimizer` przekazuje tekst do modelu NER (`models_func/model.py`), który wczytywany jest z checkpointu `models_func/checkpoint_epoch_11`. Model przewiduje etykiety tokenów (np. `B-NAME`, `0`), a logika wynikowa zachowuje słowa z `0` i podstawia nazwy kategorii dla `B-`.
- Dwa tryby pracy:
	- `anonymize_to_string()` – zwraca pojedynczy, zanonimizowany ciąg znaków.
	- `anonymize_to_file(file_name)` – przetwarza tekst linia po linii i zapisuje wynik, zachowując strukturę końców linii.
- Założenia: najpierw szybkie, deterministyczne wykrycia (regex) dla ustrukturyzowanych danych, następnie model NER dla kontekstowo trudniejszych fragmentów. Pipeline łączy wydajność i elastyczność.

## Wymagania i zależności
Zainstaluj zależności w wirtualnym środowisku:

```powershell
pip install -r requirements.txt
```

W `requirements.txt` znajdują się m.in.:
- transformers
- torch
- python-dotenv
- langchain-openai

## Jak sklonować i uruchomić
```powershell
# Sklonuj repozytorium
git clone https://github.com/mzelder/hacknation2025-v2.git
cd hacknation2025-v2

# Utwórz i aktywuj wirtualne środowisko (PowerShell)
python -m venv .venv
. .\.venv\Scripts\Activate.ps1

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom przykład
python .\main.py
```

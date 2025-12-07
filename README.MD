# Anonimizator
Narzędzie do anonimizowania danych wrażliwych takich jak imie, nazwisko, pesel, data urodzin itd.

Wykorzystaliśmy podejście typu: Hybryda Herbert + RegEx

## Struktura projektu
- `anonimizer.py` – komponent orkiestrujący wykrywanie i zamianę.
- `regex_handler.py` – wzorce regex, etykiety oraz mechanizm automatycznego uruchamiania/zamiany.
- `main.py` – prosty punkt startowy (demo).
- `anonymized.txt` / `orig.txt` – przykładowe pliki wejściowe.

## Użycie komponentu
```python
from anonimizer import Anonimizer

anon = Anonimizer(text="Nazywam się Jan Kowalski, mój PESEL to 90010112345.
Mieszkam w Warszawie przy ulicy Długiej 5.") 

result = anon.anonymize()
print(result)   
```
```
Output: Nazywam się {name} {surname}, mój PESEL to {pesel}.
Mieszkam w {address}.
```
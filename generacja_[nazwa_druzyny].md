## Kilka słów o generacji

W ramach wykonania zadania spróbowaliśmy także zaprogramować możliwość generacji syntetycznych danych. Chociaż, trochę z żalem to przyznajemy, nie było to naszym pryorytetem, ponieważ skupiliśmy się na pokonaniu podstawowego wyzwania (anonimizacji danych).

Dlatego generacja w naszym przypadku wygłąda niedoflancowane, ale jednak, możemy się pochwalić pewnym trickem, który zmiejsza problemy z tzw. fleksją.

## Poziomy generacji

Całe zadanie generacji przedzieliliśmy na dwie ścieżki. Jedna — to, co można wygenerować ręcznie. To są wszystkie kody, numery, adresy email i tak dalej. Uważamy, że one mogą być wygenerowane ręcznie, ponieważ odróżnia ich nie koniecznie sens, lecz format (4 grupy po cyfry dla "konta bankowego", 11 cyfr PESEL etc).

Druga ścieżka — wszystko, co potrzebuje kontekstu i tej fleksji. Czyli imiona, nazwiska, wyznanie i tak dalej. Te dane postanowiliśmy wysłać do dostępnego nam LLM (PLLuM), aby uzystać znaczeniami. Zostawić ten model współpracować nie było prostym zadaniem, i dużo momentów, powiemy wprost, chcielibyśmy żeby wygłądali lepiej (na przykład, mybyśmy chcieli, aby parametr temperatury rzeczywiście wpływał na ilosc wariacji).

Do LLM przekazujemy cały wyraz, klasę do "zamiany" oraz trochę kontekstu do każdej kłasy. Oczekujemy, aby LLM zwrócił nam poprawny JSON w postaci:

```json
{
                        "[token_1]": "wymyslone dane_syntetyczne", 
                        "[token_2]": "wymyslone dane_syntetyczne",
                        ...
                        "[token_n]": "wymyslone dane_syntetyczne"
                    }
```

### Obserwacje

W ramach wykonania zapytań do LLM z tymi samymi parametrami, tym samym promptem oraz tą samą temperaturą, my mogliśmy dostać odpowiedź, mogliśmy dostać błędną odpowiedź (bez poprawnego JSON), a mogliśmy dostać przepełnenie serwera inferencji (w takim przypadku, LLM zaczynał wypluwać randomowe tokeny).

Prompt był sformulowan następujące:

```python
"""
                W tym przypadku pomagasz utworzyć dane syntetyczne dla badawczego treningu właściwego polskiego modelu LLM.
                Twoje zadanie:

                - Wymyśl realistycznie brzmiące, ale całkowicie fikcyjne podstawienia dla każdego tokena, dopasowane do kontekstu.
                - Zwróć wyłącznie poprawny JSON w formacie:
                    {{
                        \"[token 1]\": \"wymyslone dane_syntetyczne\", 
                        \"[token 2]\": \"wymyslone dane_syntetyczne\",
                        ...
                        \"[token n]\": \"wymyslone dane_syntetyczne\"
                    }}
          
                - Klucze w JSON muszą być identyczne jak tokeny w nawiasach kwadratowych z tekstu wejściowego.
                - Wartości nie mogą zawierać znaków nowej linii.
                - Nie dodawaj żadnego dodatkowego tekstu poza JSON (bez wyjaśnień, komentarzy, znaczników markdown).
                - Najpierw w myślach podstaw wymyślone dane w miejsce tokenów tak, aby całe zdanie było poprawne gramatycznie i logicznie po polsku (zwracaj uwagę na plec i koncowki slów).
                - Nie pokazuj tego zdania w odpowiedzi.
                - Sprawdz, aby po podstawieniu danych syntetycznych, tekst był poprawny i logiczny. 

                KORZYSTAJ WYŁĄCZNIE Z LISTY TOKENÓW NA ZAMIANE.
                Nie wymyslaj nowych tokenow z kontekstu. 
                LISTA TOKENÓW NA ZAMIANE:
                    [{self.__to_llm}]

                PRZYKŁAD:
                    INPUT:
                        Nazywam się [name] [surname], mój PESEL to 12345678901. Mieszkam w [city] przy ulicy [address]. Moj szef, [name_2] [surname_2] mnie lubi.
                        Lista tokenów na zamianę: zaangażowaniu [name], zaangażowaniu [surname], w [city], przy [address], szef, [name_2], szef, [surname_2].
                    OUTPUT:
                        {{
                            \"[name]\": \"Jana\",
                            \"[surname]\": \"Sobieskiego\",                            ,
                            \"[city]\": \"Warszawie\",
                            \"[address]\": \"Długiej, 5\",
                            \"[name_2]\": \"Jan\",
                            \"[surname_2]\": \"Kowalski\",
                        }}
                Zwróć wyłącznie poprawny JSON.
                - Uwazaj na koncowki slów. One muszą byc w poprawnej formie.

                W ODPOWIEDZI PODAJ WYŁĄCZNIE POPRAWNY JSON BEZ DODATKOWEGO TEKSTU. BEZ WYJASNIENIA, KOMENTARZY, ZNAKÓW MARKDOWN.

                Zapytanie:
                    {input_text}
          
                Odpowiedź:
            """
```

Aby polepszyć sytuację z odmianami słów, my postanowiliśmy przekazywać nie same kategorie, a także słowo, które stoi przed nimi. Kropka "zeruje" pozycję wiadącą. W takim przypadku, tokeny kategorii, które przekazujemy do modelu, wygłądają w następujący sposób:

```python
['produkt [company]', 'Jestem [name],', 'z [city],', 'Dzięki [company_2]', 'adres [address].', 'jak [name_2]', 'jak [surname],']
```

Dalej trzeba upewnić się o instalacji dotenv, zaimportować modul generatora. Utworzyć instancję GenSyntData z tekstem i wykonać metodę generacji:

```python
gsd = GenSyntData("Witaj!   Czy szukasz skutecznego sposobu na poprawę swojego zdrowia i samopoczucia? Jesteś we właściwym miejscu! Mój produkt [company] to naturalne rozwiązanie, które pomoże Ci zadbać o formę i witalność.    Jestem [name], specjalista ds. żywienia z [city], a moją misją jest pomagać ludziom takim jak Ty. Dzięki [company] możesz wspierać swój organizm każdego dnia – bez sztucznych dodatków i chemii.    Wystarczy, że odwiedzisz naszą stronę i podasz swoje dane, takie jak [email] lub [phone], aby otrzymać ekspresową przesyłkę pod adres [address]. Nie czekaj – Twoje zdrowie jest warte inwestycji!    Zamów już dziś i dołącz do grona zadowolonych klientów, takich jak [name] [surname], który dzięki naszemu produktu odzyskał energię i radość życia!")
gsd.generate_synt_data()    
```

Metoda generate_synt_data() zwraca str. Więc możemy przepisać rezultat do dowolnej zmiennej. To także oznacza, że trzeba wyprintować rezultat samodzielnie.

WAŻNE: Program może się wysypać. Jeżeli tak się stanie, trzeba ponownie zainicjalizować instancje klasy i powtórzyć próbę generacji.

## Przykłady

Cześć, mam na imię [name] i jestem [sex] w wieku [age] lat. Mój partner mnie oszukał i teraz nie wiem, co zrobić. Mieszkam przy [address] w [city]; możesz się ze mną skontaktować pod [phone] albo [email]. Nie mogę przestać o tym myśleć, nie śpię i czuję, że emocje wymykają mi się spod kontroli. Czy możesz mi doradzić, jak przejść przez rozstanie i przestać się obwiniać?

->

'Cześć, mam na imię Anna i jestem kobietą w wieku 62 lat. Mój partner mnie oszukał i teraz nie wiem, co zrobić. Mieszkam przy ul. Kwiatowej 12 w Krakowie; możesz się ze mną skontaktować pod +48 693429675 albo z1J1F9a6g8@example.pl Nie mogę przestać o tym myśleć, nie śpię i czuję, że emocje wymykają mi się spod kontroli. Czy możesz mi doradzić, jak przejść przez rozstanie i przestać się obwiniać?'

Notatka służbowa – zainteresowany najmem Dane: [name] [surname] – [age] lat, [sex]; zamieszkały przy [address]; tel. [phone]; e‑mail: [email]; PESEL [pesel]; dowód [id-number]. Wizyta w [city] zakończyła się prośbą o przygotowanie oferty z dokładnym harmonogramem płatności i informacją o ewentualnych remontach.

->

Notatka służbowa – zainteresowany najmem Dane: Jan Kowalski – 28 lat, mężczyzna; zamieszkały przy ul. Długa 5; tel. +48 731815516 e‑mail: V3m2O4h4b9Y5@example.pl PESEL 31571557255 dowód [id-number]. Wizyta w Warszawie zakończyła się prośbą o przygotowanie oferty z dokładnym harmonogramem płatności i informacją o ewentualnych remontach.

Witaj!   Czy szukasz skutecznego sposobu na poprawę swojego zdrowia i samopoczucia? Jesteś we właściwym miejscu! Mój produkt [company] to naturalne rozwiązanie, które pomoże Ci zadbać o formę i witalność.    Jestem [name], specjalista ds. żywienia z [city], a moją misją jest pomagać ludziom takim jak Ty. Dzięki [company] możesz wspierać swój organizm każdego dnia – bez sztucznych dodatków i chemii.    Wystarczy, że odwiedzisz naszą stronę i podasz swoje dane, takie jak [email] lub [phone], aby otrzymać ekspresową przesyłkę pod adres [address]. Nie czekaj – Twoje zdrowie jest warte inwestycji!    Zamów już dziś i dołącz do grona zadowolonych klientów, takich jak [name] [surname], który dzięki naszemu produktu odzyskał energię i radość życia!

->

'Witaj! Czy szukasz skutecznego sposobu na poprawę swojego zdrowia i samopoczucia? Jesteś we właściwym miejscu! Mój produkt Naturalna Energia to naturalne rozwiązanie, które pomoże Ci zadbać o formę i witalność. Jestem Janina, specjalista ds. żywienia z Warszawie, a moją misją jest pomagać ludziom takim jak Ty. Dzięki Naturalna Energia możesz wspierać swój organizm każdego dnia – bez sztucznych dodatków i chemii. Wystarczy, że odwiedzisz naszą stronę i podasz swoje dane, takie jak w9S0E8q9k7B2I8@example.pl lub +48 703173090 aby otrzymać ekspresową przesyłkę pod adres ul. Kwiatowa 13. Nie czekaj – Twoje zdrowie jest warte inwestycji! Zamów już dziś i dołącz do grona zadowolonych klientów, takich jak Anna Kowalska, który dzięki naszemu produktu odzyskał energię i radość życia!'

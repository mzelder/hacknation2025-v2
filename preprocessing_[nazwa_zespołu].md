## Opis przetwarzania, pozyskiwania danych

W ramach wykonania zadania postanowiliśmy zrobić fine-tune modelu [Herbert](https://huggingface.co/allegro/herbert-base-cased) (Mroczkowski, Robert  and Rybak, Piotr and Wróblewska, Alina  and Gawlik, Ireneusz, CC BY 4.0). Dla realizacji tego celu potrzebowaliśmy dane. 

Za dane treningowe wzieliśmy dane z plików tekstowych, dostarczonych przez organizatorów zadania. 

Ogólnie nasze podejście można opisać następująco:

1. **Znalezienie par [label] — text**. Czyli, co zostało zmienione na labely.
2. **Analiza par**. Co jest podstawą dla zmiany tekstu w label — format (dotyczy, na przykład, liczb) czy sens (imię, wyznanie etc).
3. **Przygotowanie** labelów, które są zmieniane na podstawie sensu, do dotrenowania modelu.

Przygotowanie danych do trenowania jest opisane w Readme. 

Dane nie zostały przez nas ani zmienione, ani wzbogacone syntetyczne, ponieważ na to nie starczyło czasu naszemu 3-osobowemu zespółowi.

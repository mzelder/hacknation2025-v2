from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


api_key = os.getenv('API_KEY')
base_url = "https://apim-pllum-tst-pcn.azure-api.net/vllm/v1"
model_name = "CYFRAGOVPL/pllum-12b-nc-chat-250715"


llm = ChatOpenAI(
    model=model_name,
    openai_api_key="EMPTY",
    openai_api_base=base_url,
    temperature=0.23,
    max_tokens=300,
    default_headers={
    'Ocp-Apim-Subscription-Key': api_key
     }
)

response = llm.invoke("""
Jesteś systemem do anonimizacji danych wrażliwych w tekstach konwersacyjnych po polsku.
Twoim zadaniem jest wspomóc tej anonymizacji, wskazując, które słowa trzeba zamienić na tokeny.


TOKENY: 
    [name] – imiona.
    [surname] – nazwiska.
    [age] – wiek.
    [date-of-birth] – data urodzenia.
    [date] – inne daty wydarzen pozwalające identyfikować osobę (np. w rozmowie medycznej „przyjęto 23.09.2023 r.”)
    [sex] – płeć (jeśli wyrażona explicite w formie danej wrażliwej, np. w formularzu/deklaracji).
    [religion] – wyznanie.
    [political-view] – poglądy polityczne.
    [ethnicity] – pochodzenie etniczne/narodowe.
    [sexual-orientation] – orientacja seksualna.
    [health] – dane o stanie zdrowia
    [relative] – relacje rodzinne, które ujawniają tożsamość danej osoby (np.„mój brat Jan”, „syn Kowalskiego”, „córka pana Nowaka”
REGUŁY: 
    - Słowo albo numer trzeba zamienić na token, jeżeli ono jest związane z danymi osobowymi. 
    - Każde słowo/liczba musi odpowiadać jednemu tokenowi
    - OBOWIĄZKOWE używać tylko tokenów które są ci dane
    - Dla każdego słowa w zdaniu pomyśl, czy to słowo jest związane z danymi personalnymi, a znacy, go trzeba go zamenić na token.
    - W odpowiedzi wyślij tylko poprawny JSON.
OUTPUT: 
    - Poprawny JSON w postaci:
        {
            "dane_wrazliwe": "token" 
        }
PRZYKŁADY:
    INPUT: Nazywam się Jan Kowalski, mój PESEL to 90010112345. Mieszkam w Warszawie przy ulicy Długiej 5
    OUTPUT:
    {
        "Jan": "[name]",
        "Kowalski": "[surname]",
        "90010112345": "[pesel]",
        "Warszawie przy ulicy Długiej 5": "[address]",
        "Krakowie": "[miasto]"
    }

ZAPYTANIE:
Nie wyklucza się istnienia w terenie innych nie wykazanych na niniejszej mapie urządzeń podziemnych, które nie były zgłoszone do inwentaryzacji lub o których brak jest informacji w instytucjach branżowych. mgr inż. Jerzy P@wlos UPR NR EWID 249 02 MOR, mgr inż. clominik Kołak, mgr inż. Tadeusz Buśko, inż. Ada Fedak.
ROZPORZĄDZENIE MINISTRA INFRASTRUKTURY I ROZWOJU z dnia 20 maja 2014 r. w sprawie sposobu udostępniania map zasadniczych oraz mapy ewidencyjnej w postaci elektronicznej Na podstawie art. 24a ust. 2 ustawy z dnia 17 maja 1989 r. Prawo geodezyjne i kartograficzne (Dz. U. z 2010 r. Nr 193, poz. 1287, z późn. zm.) zarządza się, co następuje:  § 1. Rozporządzenie określa sposób udostępniania map zasadniczych oraz mapy ewidencyjnej w postaci elektronicznej.  § 2. Udostępnianie map zasadniczych oraz mapy ewidencyjnej w postaci elektronicznej odbywa się poprzez:  1) sieć teleinformatyczną; 2) nośniki danych.  § 3. Udostępnianie map zasadniczych oraz mapy ewidencyjnej w postaci elektronicznej przez sieć teleinformatyczną odbywa się za pośrednictwem geoportalu, o którym mowa w art. 24b ustawy, z zachowaniem wymogów bezpieczeństwa określonych w przepisach o ochronie informacji niejawnych.
""")
print(response.model_dump()['content'])
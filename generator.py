# Ivan Maslov, 07.12.2025, hacknation 2025
# 
# Ten plik zawiera funkcjonalność generatora — 
# zbioru skryptów, które będą podstawiały dane syntetyczne 
# do zanonimizowanych danych osobowych.
# 

import random
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json
from datetime import datetime
import os

load_dotenv()

TOKEN_LIST = {
    "[name]": "llm",
    "[surname]": "llm",
    "[age]": "rand-age",
    "[date-of-birth]": "rand-DOB",
    "[date]": "rand-date",
    "[sex]": "llm",
    "[religion]": "llm",
    "[political-view]": "llm",
    "[ethnicity]": "llm",
    "[sexual-orientation]": "llm",
    "[health]": "rand-health-data",
    "[relative]": "llm",
    "[city]": "llm",
    "[address]": "llm",
    "[email]": "rand-email",
    "[phone]": "rand-phone",
    "[pesel]": "rand-pesel",
    "[bank-account]": "rand-bank-account",
    "[username]": "rand-username",
    "[secret]": "rand-secret",
    "[document-number]": "rand-document-number",
    "[company]": "llm",
    "[school-name]": "llm",
    "[job-title]": "llm",
    "[credit-card-number]": "rand-credit-card-number",
}

class GenSyntData:
    """
        Klasa generatora danych syntetycznych.

        Zadaniem tej kłasy jest przyjęcie napisu, zawierającego 
        dane osobowe w postaci tokenów formatu [token].
        
        Lista tokenów jest wskazana TOKEN_LIST. To takze przedziela, która metoda
        powinna być uzyta do generowania tych danych.

        Args:
            text: str - napis do uzupelnienia danymi syntetycznymi.
        
        Methods:
            generate_synt_data(self) -> str:
                Generuje dane syntetyczne do napisu, zawierającego dane osobowe w postaci tokenów formatu [token].
            regenerate_for_token(self, token: str) -> str:
                Generuje dane syntetyczne dla konkretnego tokenu.

        
    """
    def __init__(self, text):
        if not isinstance(text, str):
            raise ValueError("Generator powinien być zainicjowany napisem.")
        
        self._text = text
        self._tokens = [ token for token in text.split() if token in TOKEN_LIST.keys() ]
        self._generated_text = ""

        if not self._tokens:
            raise ValueError("Napis nie zawiera żadnych tokenów do uzupelnienia.")
        
        self._register_methods()


        self.__generated_rand_age = None
        self.__dict_letters = [ chr(i) for i in range(97, 123) ] + [ chr(i) for i in range(65, 91) ] 
        self.__dict_numbers = [ str(i) for i in range(0, 10) ]
        self.__dict_special = [ ".", "-", "_", "$", "#"]

        self.__to_llm = []


        self.LLM_API_KEY = os.getenv('API_KEY', "b87673ce906449ddb18d5a26a078a9dc")
        self.LLM_API_URL = os.getenv('LLM_API_URL', "https://apim-pllum-tst-pcn.azure-api.net/vllm/v1")
        self.LLM_MODEL_NAME = os.getenv('LLM_MODEL_NAME', "CYFRAGOVPL/pllum-12b-nc-chat-250715")

    def _register_methods(self):
        """
            Rejestruje metody generowania danych syntetycznych dla każdego tokenu.
        """
        self.__methods = {
            "llm": self.__append_to_llm,
            "rand-age": self._rand_age,
            "rand-DOB": self._rand_DOB,
            "rand-date": self._rand_date,
            "rand-health-data": self._rand_health_data,
            "rand-email": self._rand_email,
            "rand-phone": self._rand_phone,
            "rand-pesel": self._rand_pesel,
            "rand-bank-account": self._rand_bank_account,
            "rand-username": self._rand_username,
            "rand-secret": self._rand_secret,
            "rand-credit-card-number": self._rand_credit_card_number,
            "rand-document-number": self._rand_document_number,
        }

    def _rand_age(self) -> str:
        """
            Generuje losowy wiek.
        """

        if self.__generated_rand_age is not None:
            return f"{self.__generated_rand_age}"
        else: 
            self.__generated_rand_age = random.randint(16, 85)
            return f"{self.__generated_rand_age}"
    
    def _rand_DOB(self) -> str:
        """
            Generuje losową datę urodzenia (z uwagi na wygenerowany wiek).
        """        

        if self.__generated_rand_age is None:
            self.__generated_rand_age = random.randint(16, 85)
            return f"{datetime.now().year - self.__generated_rand_age}-{random.randint(1, 12)}-{random.randint(1, 28)}"
        else:
            return f"{datetime.now().year - self.__generated_rand_age}-{random.randint(1, 12)}-{random.randint(1, 28)}"

    def _rand_date(self) -> str:
        """
            Generuje losową datę.
        """
        return f"{datetime.now().year - random.randint(1, 58)}-{random.randint(1, 12)}-{random.randint(1, 28)}"
    
    def _rand_health_data(self) -> str:
        """
            Generuje losowe dane o stanie zdrowia.
        """
        return "(zostało wykryte: " + random.choice(['cukrzyca', 'nowotwór', 'depresja', 'zawał serca', 'udar mózgu', 'zapalenie płuc', 'grypa', 'nadciśnienie', 'złamanie POChP', 'astma']) + ")"

    
    def _rand_email(self) -> str:
        """
            Generuje losowy email.
        """
        
        email = ""
        for i in range(random.randint(3, 10)):
            email += random.choice(self.__dict_letters)
            email += random.choice(self.__dict_numbers)
        email += "@example.pl"

        return  f"{email}"
    
    def _rand_phone(self) -> str:
        """
            Generuje losowy numer telefonu.
        """
        return f"+48 {random.randint(600000000, 999999999)}"
    
    def _rand_pesel(self) -> str:
        """
            Generuje losowy numer, który, co prawda nie jest PESELem, 
            ale uwazamy, ze moze go zastąpić, bo model i tak nie potrzebuje sprawdzac
            wszystkich zasad PESELu.
        """

        return f"{random.randint(10000000000, 99999999999)}"
    
    def _rand_bank_account(self) -> str:
        """
            Generuje losowy numer konta bankowego.
        """
        return f"{random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}"

    def _rand_username(self) -> str:
        """
            Generuje losowy login.
        """
        return f"{random.choice(self.__dict_letters)}{random.choice(self.__dict_numbers)}{random.choice(self.__dict_numbers)}{random.choice(self.__dict_numbers)}{random.choice(self.__dict_numbers)}{random.choice(self.__dict_numbers)}"
    
    def _rand_secret(self) -> str:
        """
            Generuje losowe hasło lub klucz API.
        """
        return f"{random.choice(self.__dict_letters)}{random.choice(self.__dict_special)}{random.choice(self.__dict_numbers)}{random.choice(self.__dict_numbers)}{random.choice(self.__dict_special)}{random.choice(self.__dict_numbers)}{random.choice(self.__dict_numbers)}{random.choice(self.__dict_numbers)}{random.choice(self.__dict_special)}"
    
    def _rand_credit_card_number(self) -> str:
        """
            Generuje losowy numer karty kredytowej.
        """
        return self.__rand_bank_account().replace(" ", "")

    def _rand_document_number(self) -> str:
        """
            Generuje losowy numer dowodu osobistego.
        """
        return f"{random.randint(10000000000, 99999999999)}"

    def __append_to_llm(self, token: str) -> None:
        """
            Dodaje dane syntetyczne do napisu, zawierającego dane osobowe w postaci tokenów formatu [token].
        """
        self.__to_llm.append(token)
        return None

    
    def __send_request_to_llm(self, input_text: str) -> dict:
        """
            Wysyła zapytanie do LLM i otrzymuje odpowiedź w postaci JSON.

            Ta wewnętrzna metoda jest uzywana do wyslania napisu, ktory chcemy uzupelnic danymi syntetycznymi.
            do LLM. W odpowiedzi oczekujemy JSON, ktory zawiera: 
            {
                "token": "dane_syntetyczne"
            }

            W przypadku błędu LLM, powiadamia o nim i wywoluje błąd ValueError.
        """

        try:
            llm = ChatOpenAI(
                model=self.LLM_MODEL_NAME,
                openai_api_key="EMPTY",
                openai_api_base=self.LLM_API_URL,
                temperature=0.23,
                max_tokens=300,
                default_headers={
                'Ocp-Apim-Subscription-Key': self.LLM_API_KEY
                }
            )

            PROMPT = f"""
                W tym przypadku pomagasz utworzyć dane syntetyczne dla badawczego treningu właściwego polskiego modelu LLM.
                Twoje zadanie:

                - Wymyśl realistycznie brzmiące, ale całkowicie fikcyjne podstawienia dla każdego tokena.
                - Zwróć wyłącznie poprawny JSON w formacie:
                    {{
                        \"[token 1]\": \"dane_syntetyczne\", 
                        \"[token 2]\": \"dane_syntetyczne\",
                        \"[token 3]\": \"dane_syntetyczne\",
                        ...
                        \"[token n]\": \"dane_syntetyczne\"
                    }}
                
                - Klucze w JSON muszą być identyczne jak tokeny w nawiasach kwadratowych z tekstu wejściowego.
                - Wartości nie mogą zawierać znaków nowej linii.
                - Nie dodawaj żadnego dodatkowego tekstu poza JSON (bez wyjaśnień, komentarzy, znaczników markdown).
                - Najpierw w myślach podstaw wymyślone dane w miejsce tokenów tak, aby całe zdanie było poprawne gramatycznie i logicznie po polsku.
                - Nie pokazuj tego zdania w odpowiedzi.
                - Sprawdz, aby po podstawieniu danych syntetycznych, tekst był poprawny i logiczny. 
                

                LISTA TOKENÓW NA ZAMIANE:
                    [{self.__to_llm}]

                KORZYSTAJ WYŁĄCZNIE Z LISTY TOKENÓW NA ZAMIANE.
                Nie wymyslaj nowych tokenow z kontekstu. 

                PRZYKŁAD:
                    INPUT:
                        Nazywam się [name] [surname], mój PESEL to 12345678901. Mieszkam w [city] przy ulicy [address].
                    OUTPUT:
                        {{
                            \"[name]\": \"Jan\",
                            \"[surname]\": \"Kowalski\",
                            \"[city]\": \"Warszawie\",
                            \"[address]\": \"Długiej, 5\"
                        }}
                Zwróć wyłącznie poprawny JSON.
                - Uwazaj na koncowki slów. One muszą byc w poprawnej formie.

                Niepoprawnie:
                    [address], [city].
                    - 'na', '[address]', 'w', '[city].'
                    
                OUTPUT:
                 {{
                    \"[address]\": \"Długa, 5\",
                    \"[city]\": \"Warszawa\"
                 }}

                Poprawnie:
                    [address], [city].
                    - 'na', '[address]', 'w', '[city].'
                    

                OUTPUT:
                 {{
                    \"[address]\": \"Długiej, 5\",
                    \"[city]\": \"Warszawie\"
                 }}

                W ODPOWIEDZI PODAJ WYŁĄCZNIE POPRAWNY JSON BEZ DODATKOWEGO TEKSTU.
                
                Tylko jeden JSON powinien byc generowany.

                JSON ma zawierać słowa w poprawnej formie gramatycznej. Pamiętaj ze pozniej te slowa beda podstawiane do napisu zamiast tokenow.

                Twoja odpowiedź OBOWIĄZKOWO musi zaczynać się znakiem {{ i kończyć }}. 
                
                Jezeli odstapisz od regul, wyłączymy twoje servere za tydzień z powodu nieuzyteczności.

                INPUT:
                    {input_text}
                
                
            """

            response = llm.invoke(PROMPT)
            if not "{" in response.content or not "}" in response.content:
                raise ValueError("Odpowiedź nie zawiera poprawnego JSON.")
            else:
                resp = response.content.split("{")[1].split("}")[0]
                resp = "{" + resp + "}"    
            print(response.content)
            return json.loads(resp)

        except Exception as e:
            raise ValueError(f"Błąd podczas wysyłania zapytania do LLM: {e}")
    
    def generate_synt_data(self) -> str:
        """
            Generuje dane syntetyczne do napisu, zawierającego dane osobowe w postaci tokenów formatu [token].
        """

        text_with_replacements = []
        indexes_to_replace = []
        for i, el in enumerate(self._text.split()):
            tkn = el.strip().replace(",", "").replace(".", "").replace(".", "").replace("!", "").replace("?", "").replace(":", "").replace(";", "").replace("(", "").replace(")", "").replace("{", "").replace("}", "").replace("\"", "").replace("\'", "").replace("`", "").replace("*", "").replace("+", "").replace("_", "").replace("|", "").replace("\\", "").replace("/", "").replace("<", "").replace(">", "").replace(" ", "")
            print("TOKEN: ", tkn)
            if tkn in TOKEN_LIST.keys():
                met = TOKEN_LIST[tkn]
                if met == "llm":
                    self.__append_to_llm(el)
                    indexes_to_replace.append(i)
                    text_with_replacements.append(el)
                    continue
                else:
                    ret = self.__methods[met]()
                    if ret:
                        text_with_replacements.append(ret)
            else:
                text_with_replacements.append(el)

        print(text_with_replacements, indexes_to_replace)
    
        if self.__to_llm:
            llm_result_json = self.__send_request_to_llm(" ".join(text_with_replacements))

        for el in indexes_to_replace:
            print(el)
            token = text_with_replacements[el].strip().replace(",", "").replace(".", "").replace("!", "").replace("?", "").replace(":", "").replace(";", "").replace("(", "").replace(")", "").replace("{", "").replace("}", "").replace("\"", "").replace("\'", "").replace("`", "").replace("*", "").replace("+", "").replace("-", "").replace("_", "").replace("|", "").replace("\\", "").replace("/", "").replace("<", "").replace(">", "").replace(" ", "")
        
            text_with_replacements[el] = text_with_replacements[el].replace(token, llm_result_json[token])

        
        return " ".join(text_with_replacements)

    
    

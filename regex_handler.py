import re

REGEX_PESEL = r'(?<!\d)\d{11}(?!\d)'
REGEX_EMAIL = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?" 
REGEX_BANK_ACC = r"\d{2}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]"

class RegexSet:
    
    @staticmethod
    def re_pesel(text):
        return re.findall(REGEX_PESEL, text)
    
    @staticmethod
    def re_email(text):
        return re.findall(REGEX_EMAIL, text)
    
    @staticmethod
    def re_bank_acc(text):
        return re.findall(REGEX_BANK_ACC, text)


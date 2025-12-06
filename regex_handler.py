import re

REGEX_PESEL = r'(?<!\d)\d{11}(?!\d)'
REGEX_PHONE_NUMBER = r'(?<!\d)(?:\+?48[\s-]?)?(?:\d[\s-]?){9}(?!\d)'

class RegexSet:
    
    @staticmethod
    def re_pesel(text):
        return re.findall(REGEX_PESEL, text)

    @staticmethod
    def re_phone_number(text):
        return re.findall(REGEX_PHONE_NUMBER, text)


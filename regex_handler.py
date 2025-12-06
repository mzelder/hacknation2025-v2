import re

REGEX_PESEL = r'(?<!\d)\d{11}(?!\d)'

class RegexSet:
    
    @staticmethod
    def re_pesel(text):
        return re.findall(REGEX_PESEL, text)






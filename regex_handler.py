import re

REGEX_DATE_NUM = re.compile(
    r'^(?:(?:31\.(?:01|03|05|07|08|10|12))|(?:29|30\.(?:01|03|04|05|06|07|08|09|10|11|12))|(?:0[1-9]|1\d|2[0-8]\.(?:0[1-9]|1[0-2])))\.(?:19|20)\d{2}$|^29\.02\.(?:(?:19|20)(?:0[48]|[2468][048]|[13579][26]))$'
)

REGEX_DATE_CHAR = re.compile(
    r"^(?:\s*(?:[0-3]?\d)\s+(?:stycz(?:nia?|ń)|lut(?:ego|y)|marc(?:a|zec)|kwietn(?:ia|ień)|maj|maja|czerw(?:ca|wiec)|lip(?:ca|iec)|sierp(?:nia|ień)|wrzes(?:ie[ńń]|nia)|pa[źz]dziern(?:ika|ik)|listop(?:ada|ad)|grud(?:zie[ńń]|nia|zień))(?:(?:\s+(?:19|20)\d{2})?))$",
    re.IGNORECASE | re.UNICODE
)

MONTH_MAP = {
    'styczeń': 1, 'stycznia': 1, 'styczniu': 1, 'styczen': 1,
    'luty': 2, 'lutego': 2,
    'marzec': 3, 'marca': 3,
    'kwiecień': 4, 'kwietnia': 4, 'kwietn': 4,
    'maj': 5, 'maja': 5,
    'czerwiec': 6, 'czerwca': 6, 'czerw': 6,
    'lipiec': 7, 'lipca': 7,
    'sierpień': 8, 'sierpnia': 8,
    'wrzesień': 9, 'wrzesnia': 9, 'wrzesien': 9,
    'październik': 10, 'pazdziernik': 10, 'października': 10, 'pazdziernika': 10,
    'listopad': 11, 'listopada': 11,
    'grudzień': 12, 'grudnia': 12, 'grudzen': 12
}

class RegexSet:

    def __init__(self):
        pass

    def re_date(self, text):
        return bool(REGEX_DATE_NUM.match(text)) or bool(REGEX_DATE_CHAR.match(text))
    
    def re_pesel(self):
        pass



## test

rs = RegexSet()
x = rs.re_date("abc cos tam 6 grudnia i cos tam innego")
print(x)


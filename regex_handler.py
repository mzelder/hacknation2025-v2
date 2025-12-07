import re

LABELS = {
    "PESEL": "[pesel]",
    "PHONE_NUMBER": "[phone]",
    "EMAIL": "[email]",
    "BANK_ACC": "[bank-account]"
}

# find 1479 from 1670
REGEX_PESEL = r'(?<!\d)\d{11}(?!\d)' 

# find 1835 from 2193 
_GROUP3 = r'(?:\d{3}|[A-Za-z]\d{2}|\d[A-Za-z]\d|\d{2}[A-Za-z])'
REGEX_PHONE_NUMBER = rf'(?<![A-Za-z0-9])(?:\+?48[ -]?)?{_GROUP3}(?:[ -]{_GROUP3}){{2}}(?![A-Za-z0-9])'

# 2055 from 2103
REGEX_EMAIL = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?" 

# 135 from 135
REGEX_BANK_ACC = r"\b(?:[A-Za-z0-9!]{4}\s){3}[A-Za-z0-9!]{4}\b"

class RegexSet:
    @staticmethod
    def all_patterns():
        patterns = {}
        for name, value in globals().items():
            if name.startswith("REGEX_") and isinstance(value, str) and value:
                patterns[name] = re.compile(value)
        return patterns

    @staticmethod
    def run_all(text):
        results = {}
        for name, pattern in RegexSet.all_patterns().items():
            try:
                results[name] = pattern.findall(text)
            except Exception:
                results[name] = []
        return results
    
    @staticmethod
    def replace_all(text):
        """Replace all matches of REGEX_* with labels from LABELS."""
        replaced = text
        for name, pattern in RegexSet.all_patterns().items():
            label_key = name.replace("REGEX_", "")
            label = LABELS.get(label_key, f"[{label_key.lower()}]")
            replaced = pattern.sub(label, replaced)
        return replaced



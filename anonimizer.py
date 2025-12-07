from regex_handler import RegexSet
from models_func.model import Model

class Anonimizer:
    def __init__(self,  text=None, file_name=None):
        if text:
            self.text = text
        elif file_name:
            self.text = self.load_file(file_name)
        else:
            raise ValueError("Either 'file' or 'text' must be provided")
        
    def load_file(self, file):
        with open(file, "r", encoding="utf-8") as f:
            return f.read()

    def anonymize(self) -> str:
        """Return text with all detected patterns replaced by labels."""
        regexed_text = RegexSet.replace_all(self.text)
        result = Model.anonymize(regexed_text)
        return result
        
        

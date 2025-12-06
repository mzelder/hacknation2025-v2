from regex_handler import RegexSet


class Anonimizer:
    def __init__(self,  text=None, file_name=None):
        if text:
            self.text = self.load_text(text)
        elif file_name:
            self.text = self.load_file(file_name)
        else:
            raise ValueError("Either 'file' or 'text' must be provided")
        
    def load_file(self, file):
        with open(file, "r", encoding="utf-8") as f:
            return f.read()

    def load_text(self, text):
        return text

    def anonimize(self):
        return RegexSet().re_email(self.text)
        

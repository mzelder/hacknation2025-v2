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
            return "".join(f.readlines())

    def anonymize_to_string(self) -> str:
        """Return text with all detected patterns replaced by labels."""
        regexed_text = RegexSet.replace_all(self.text)
        model = Model()
        result = model.anonymize(regexed_text)
        return result
    
    def anonymize_to_file(self, file_name):
        """Preserve original line structure when writing to file."""
        lines = self.text.splitlines(True)  # keep line endings
        out_lines = []
        model = Model()
        for line in lines:
            # Apply regex replacements per line
            regexed_line = RegexSet.replace_all(line)
            # Get model labels per line and reconstruct
            tokens_labels = model.predict_labels(regexed_line)
            line_out_tokens = []
            for token, label in tokens_labels:
                if label == "0":
                    line_out_tokens.append(token)
                elif "B" in label:
                    line_out_tokens.append(label.split("B-")[1])
                else:
                    continue
            out_lines.append(' '.join(line_out_tokens))
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(out_lines))
        
        

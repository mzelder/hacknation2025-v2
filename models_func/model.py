import torch
import pickle
from transformers import AutoTokenizer, AutoModelForTokenClassification

class Model:
    """
    NER-based text anonymization model for PII (Personally Identifiable Information) redaction.
    
    Detects and replaces sensitive entities (names, addresses, PESEL, etc.) with labels like [name], [pesel].
    """

    def __init__(self):
        self.device = self._select_device()
        self.checkpoint_path = "models_func/checkpoint_epoch_11"
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint_path)
        self.model = AutoModelForTokenClassification.from_pretrained(self.checkpoint_path).to(self.device)
        self.model.eval()
        
        with open('models_func/label2id.pkl', 'rb') as f:
            label2id = pickle.load(f)
        self.id2label = {v: k for k, v in label2id.items()}
    
    def _select_device(self):
        if torch.cuda.is_available():
            return torch.device("cuda")
        elif torch.backends.mps.is_available():
            return torch.device("mps")
        else:
            return torch.device("cpu")

    
    def anonymize(self, regexed_text):
        """
        Anonymizes input text by replacing PII entities with standardized labels.
        
        Processes text line-by-line, detects sensitive entities using NER model,
        and replaces them with labels like [name], [pesel], [address]. Non-sensitive
        words (label '0') and continuation tokens (I-) are preserved or skipped.
        
        Args:
            regexed_text (str): Multi-line input text containing potential PII
            
        Returns:
            str: Anonymized text with all sensitive entities replaced by labels,
                 flattened into single string with spaces
            
        Raises:
            Exception: If NER prediction fails during processing
        """

        all_texts = regexed_text.splitlines()

        predicted_lines = []
        line, label = "", ""
        try:
            for line in all_texts:
                result = self.predict_labels(line)
                res_list = []
                for token, label in result:
                    # print(token, label)
                    if label == "0":
                        res_list.append(token)
                    elif "B" in label:
                        res_list.append(label.split("B-")[1])
                    else:
                        continue
                predicted_lines.append(res_list)
        except Exception as e:
            print(f"Error {e} was found on {label} in {line}")
            raise e

        all_tokens = [token for line_tokens in predicted_lines for token in line_tokens]
        return " ".join(all_tokens)
    
    
    def predict_labels(self, text):
        """
        Predicts NER labels for tokens in input text using trained TokenClassification model.
        
        Tokenizes text, runs inference on GPU/CPU/MPS, maps predictions back to original
        words using word_ids, and returns (token, label) pairs for B- entities only.
        
        Args:
            text (str): Raw input text to analyze
            
        Returns:
            list[tuple[str, str]]: List of (original_token, predicted_label) pairs.                               
        """
        tokens = text.split()
        
        encoding = self.tokenizer(tokens, is_split_into_words=True, return_tensors="pt", truncation=True)
        input_ids = encoding["input_ids"].to(self.device)
        attention_mask = encoding["attention_mask"].to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            predictions = outputs.logits.argmax(dim=-1).cpu().tolist()[0]


        word_ids = encoding.word_ids()
        predicted_labels = []
        previous_word_idx = None
        for idx, word_idx in enumerate(word_ids):
            if word_idx is None:
                continue

            if word_idx != previous_word_idx:
                label_id = predictions[idx]
                predicted_labels.append((tokens[word_idx], self.id2label[label_id]))
            previous_word_idx = word_idx

        return predicted_labels




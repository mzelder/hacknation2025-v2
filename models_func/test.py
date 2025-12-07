import torch
import pickle
from transformers import AutoTokenizer, AutoModelForTokenClassification


with open('label2id.pkl', 'rb') as f:
    label2id = pickle.load(f)
id2label = {v: k for k, v in label2id.items()}


if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")


checkpoint_path = "./model_final"

tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
model = AutoModelForTokenClassification.from_pretrained(checkpoint_path).to(device)
model.eval()

def predict_labels(text):
    tokens = text.split()
    

    encoding = tokenizer(tokens, is_split_into_words=True, return_tensors="pt", truncation=True)
    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)

    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        predictions = outputs.logits.argmax(dim=-1).cpu().tolist()[0]


    word_ids = encoding.word_ids()
    predicted_labels = []
    previous_word_idx = None
    for idx, word_idx in enumerate(word_ids):
        if word_idx is None:
            continue

        if word_idx != previous_word_idx:
            label_id = predictions[idx]
            predicted_labels.append((tokens[word_idx], id2label[label_id]))
        previous_word_idx = word_idx

    return predicted_labels

if __name__ == "__main__":
    '''
    with open('anonymized.txt') as f:
        user_input = f.read()
        result = predict_labels(user_input)
        for token, label in result:
            print(f"{token}: {label}")
            '''

    # result = predict_labels(user_input)
    with open("evaltest.txt", "r") as pl:
        all_texts = pl.readlines()

    predicted_lines = []
    line, label = "", ""
    try:
        for line in all_texts:
            result = predict_labels(line)
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

    with open("result_final.txt", "w") as pl:
        for el in predicted_lines:
            pl.write(" ".join(el) + "\n") 



    #test_line_1 = "Ankieta Bankowa:  Zwyczaje i Preferencje Graczy A. Dane podstawowe 1. Andrzej Du6a, 39 lat, PESEL 38927590391 zamieszkały przy ul. Sokolskiej, 32, w Sosn0wcu. Pracuje w firmie CAT. J3go matka jest chrześcijanką i fanką kina – od klasyków po najnowsze produkcje na Netflix."
    
    # test_line_1
    # result = predict_labels(test_line_1)
    # res_list = []
    # curr_cat = ""
    # for token, label in result:
    #     print(token, label)
    #     if label == "0":
    #         res_list.append(token)
    #         curr_cat = ""
    #     elif "B" in label:
    #         res_list.append(label.split("B-")[1])
    #         curr_cat = label.split("B-")[1]
    #     elif "I" in label:
    #         if curr_cat in label and curr_cat != None:
    #             continue
    #         else:
    #             res_list.append(label.split("I-")[1])
    #             curr_cat = label.split("I-")[1]
    #     else:
    #         continue
    # print(" ".join(res_list))
    # for token, label in result:
    #     print(f"{token}: {label}")

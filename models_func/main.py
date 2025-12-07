import pickle
import os
import torch
import sacremoses
from transformers import AutoTokenizer, AutoModelForTokenClassification
from seqeval.metrics import classification_report, f1_score


with open('all_labels.pkl', 'rb') as f:
    all_labels = pickle.load(f)

with open('all_tokens.pkl', 'rb') as f:
    all_tokens = pickle.load(f)

with open('label2id.pkl', 'rb') as f:
    label2id = pickle.load(f)
    


def evaluate_model(model, dataloader, id2label):
    model.eval()
    true_labels = []
    pred_labels = []
    
    with torch.no_grad():
        for batch in dataloader:
            outputs = model(
                batch['input_ids'].to(device),
                batch['attention_mask'].to(device)
            )
            predictions = outputs.logits.argmax(dim=-1)
            
            for i in range(len(predictions)):
                true_seq = []
                pred_seq = []
                for j in range(len(predictions[i])):
                    if batch['labels'][i][j] != -100:
                        true_seq.append(id2label[batch['labels'][i][j].item()])
                        pred_seq.append(id2label[predictions[i][j].item()])
                true_labels.append(true_seq)
                pred_labels.append(pred_seq)
    
    print(classification_report(true_labels, pred_labels))
    return f1_score(true_labels, pred_labels)


def align_labels(word_ids, labels, label2id):
    """
    Align labels to subword tokens.
    Only first subword of each word gets the label, rest get -100.
    """
    previous_word_id = None
    aligned = []
    
    for wid in word_ids:
        if wid is None:  # special tokens [CLS], [SEP]
            aligned.append(-100)
        elif wid != previous_word_id:  # first subword of a word
            aligned.append(label2id[labels[wid]])
        else:  # continuation subword (same word_id as previous)
            aligned.append(-100)
        
        previous_word_id = wid
    
    return aligned


def create_batches(tokens_list, labels_list, batch_size):
    """Create batches from token and label lists."""
    batches = []
    for i in range(0, len(tokens_list), batch_size):
        batch_tokens = tokens_list[i:i + batch_size]
        batch_labels = labels_list[i:i + batch_size]
        batches.append((batch_tokens, batch_labels))
    return batches

def prepare_batch(batch_tokens, batch_labels, tokenizer, label2id, device, max_length=512):
    """Tokenize and align labels for a batch."""
    all_input_ids = []
    all_attention_masks = []
    all_labels = []
    
    for tokens, labels in zip(batch_tokens, batch_labels):
        encoding = tokenizer(
            tokens,
            is_split_into_words=True,
            truncation=True,
            max_length=max_length,
            padding='max_length',
            return_tensors='pt'
        )
        
        word_ids = encoding.word_ids()
        aligned = align_labels(word_ids, labels, label2id)
        
        aligned += [-100] * (max_length - len(aligned))
        
        all_input_ids.append(encoding['input_ids'])
        all_attention_masks.append(encoding['attention_mask'])
        all_labels.append(torch.tensor(aligned))
    
    return {
        'input_ids': torch.cat(all_input_ids).to(device),
        'attention_mask': torch.cat(all_attention_masks).to(device),
        'labels': torch.stack(all_labels).to(device)
    }


# ===== 4. SAVE MODEL FUNCTION =====
def save_model(model, tokenizer, save_dir="./model_checkpoint"):
    """Save model and tokenizer."""
    os.makedirs(save_dir, exist_ok=True)
    model.save_pretrained(save_dir)
    tokenizer.save_pretrained(save_dir)
    print(f"Model saved to {save_dir}")
    
BATCH_SIZE = 4
NUM_EPOCHS = 30

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
    

tokenizer = AutoTokenizer.from_pretrained("allegro/herbert-base-cased")

model = AutoModelForTokenClassification.from_pretrained(
    "allegro/herbert-base-cased",
    num_labels=len(label2id)
).to(device)  # 

optimizer = torch.optim.AdamW(model.parameters(), lr=3e-5)

batches = create_batches(all_tokens, all_labels, BATCH_SIZE)
print(f"Training on {len(all_tokens)} examples in {len(batches)} batches")
print(f"Device: {device}\n")

try:
    global_step = 0  
    min_loss = float('inf')
    for epoch in range(NUM_EPOCHS):
        print(f"{'='*50}")
        print(f"EPOCH {epoch + 1}/{NUM_EPOCHS}")
        print(f"{'='*50}")
        
        epoch_loss = 0
        model.train()  
        
        for batch_idx, (batch_tokens, batch_labels) in enumerate(batches):

            batch = prepare_batch(batch_tokens, batch_labels, tokenizer, label2id, device)
            
            # forward pass
            outputs = model(
                input_ids=batch['input_ids'],
                attention_mask=batch['attention_mask'],
                labels=batch['labels']
            )
            loss = outputs.loss
            
            # backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # logging
            epoch_loss += loss.item()
            global_step += 1
            
            if batch_idx % 10 == 0:
                print(f"  Batch {batch_idx}/{len(batches)} | Loss: {loss.item():.4f}")
        
        avg_loss = epoch_loss / len(batches)
        print(f"\n  → Epoch {epoch + 1} Average Loss: {avg_loss:.4f}\n")
        
        if avg_loss < min_loss:
            min_loss = avg_loss
            print("New min loss! Saving...")
            save_model(model, tokenizer, f"./checkpoint_epoch_{epoch + 1}")
            
except KeyboardInterrupt:
    print("\n\nTraining interrupted by user!")
    print("Saving model before exit...")
    save_model(model, tokenizer, "./model_interrupted")
    print("You can resume training later by loading from './model_interrupted'")

except Exception as e:
    print(f"\n\nError during training: {e}")
    print("Saving model before exit...")
    save_model(model, tokenizer, "./model_error")
    raise

else:
    print("\n✓ Training completed successfully!")
    save_model(model, tokenizer, "./model_final")

print("\nTraining session ended.")

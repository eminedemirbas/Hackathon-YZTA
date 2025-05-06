from transformers import BertTokenizer, BertForSequenceClassification
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = BertTokenizer.from_pretrained("bert_model")
model = BertForSequenceClassification.from_pretrained("bert_model")
model.to(device)
model.eval()

def predict(text: str) -> dict:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {key: val.to(device) for key, val in inputs.items()}  # GPU/CPU uyumu

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()

    return {
        "input": text,
        "predicted_class": predicted_class,
        "logits": logits.cpu().numpy().tolist()
    }

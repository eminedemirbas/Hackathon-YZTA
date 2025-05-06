#Bu dosyada modeli bir kez yükle, sonra predict_sentiment() fonksiyonuyla tahmin yap.
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Model ve tokenizer sadece 1 kez yüklenecek (performans için önemli)
model_path = "/content/drive/MyDrive/saved_model"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.to(device)
model.eval()

labels = ["neg", "pos"]

def predict_sentiment(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {key: val.to(device) for key, val in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    predicted_class_id = logits.argmax(dim=-1).item()
    return labels[predicted_class_id]

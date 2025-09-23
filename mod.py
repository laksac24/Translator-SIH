from transformers import MarianTokenizer, MarianMTModel

# Nepali → English
model_name_ne = "Helsinki-NLP/opus-mt-ne-en"
tokenizer_ne = MarianTokenizer.from_pretrained(model_name_ne)
model_ne = MarianMTModel.from_pretrained(model_name_ne)
tokenizer_ne.save_pretrained("./models/ne-en")
model_ne.save_pretrained("./models/ne-en")

# Sinhala → English
model_name_si = "Helsinki-NLP/opus-mt-si-en"
tokenizer_si = MarianTokenizer.from_pretrained(model_name_si)
model_si = MarianMTModel.from_pretrained(model_name_si)
tokenizer_si.save_pretrained("./models/si-en")
model_si.save_pretrained("./models/si-en")

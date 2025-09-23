# #!/usr/bin/env python3

# from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# class BasicTranslator:
#     def __init__(self):
#         # Use M2M100 - supports Nepali and many other languages
#         self.model_name = "facebook/m2m100_418M"  # Smallest version for free hosting
#         self.model = None
#         self.tokenizer = None
        
#         print("Loading M2M100 translation model...")
#         try:
#             self.tokenizer = M2M100Tokenizer.from_pretrained(self.model_name)
#             self.model = M2M100ForConditionalGeneration.from_pretrained(self.model_name)
#             print("✅ M2M100 model loaded successfully!")
#         except Exception as e:
#             print(f"❌ Failed to load model: {e}")
    
#     def translate_nepali(self, text):
#         """Translate Nepali text to English"""
#         if not self.model:
#             return "Model not loaded"
        
#         try:
#             # Set source language to Nepali
#             self.tokenizer.src_lang = "ne"
            
#             # Encode the text
#             encoded = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            
#             # Generate translation to English
#             generated = self.model.generate(
#                 **encoded, 
#                 forced_bos_token_id=self.tokenizer.get_lang_id("en"),
#                 max_length=200
#             )
            
#             # Decode the result
#             result = self.tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
#             return result
            
#         except Exception as e:
#             return f"Translation error: {e}"

# def main():
#     """Test the translator in terminal"""
#     translator = BasicTranslator()
    
#     print("\n" + "="*50)
#     print("🌍 Basic Nepali-English Translator")
#     print("="*50)
    
#     # Test sentences
#     test_sentences = [
#         "नमस्ते",
#         "म राम्रो छु",
#         "तपाईंलाई कस्तो छ?"
#     ]
    
#     print("\n📝 Testing with sample sentences:")
#     for i, nepali_text in enumerate(test_sentences, 1):
#         print(f"\n{i}. Nepali: {nepali_text}")
#         translation = translator.translate_nepali(nepali_text)
#         print(f"   English: {translation}")
    
#     print("\n" + "="*50)
#     print("💬 Interactive Mode - Enter Nepali text (or 'quit' to exit)")
#     print("="*50)
    
#     while True:
#         try:
#             user_input = input("\nEnter Nepali text: ").strip()
            
#             if user_input.lower() in ['quit', 'exit', 'q']:
#                 print("👋 Goodbye!")
#                 break
            
#             if not user_input:
#                 print("Please enter some text.")
#                 continue
            
#             print("🔄 Translating...")
#             translation = translator.translate_nepali(user_input)
#             print(f"📖 Translation: {translation}")
            
#         except KeyboardInterrupt:
#             print("\n👋 Goodbye!")
#             break
#         except Exception as e:
#             print(f"❌ Error: {e}")

# if __name__ == "__main__":
#     main()


from transformers import M2M100ForConditionalGeneration, AutoTokenizer

# Load model and tokenizer
model_name = "alirezamsh/small100"
model = M2M100ForConditionalGeneration.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def translate(text, src_lang, tgt_lang):
    # Prepare the input text
    inputs = tokenizer(f"{src_lang}: {text}", return_tensors="pt", padding=True, truncation=True)
    # Generate translation
    translated_tokens = model.generate(**inputs, forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang])
    # Decode the translated text
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return translated_text

# Example usage
# if __name__ == "__main__":
#     text = """नेपाल एक सुन्दर देश हो । यहााँ हहमाल, पहाड र तराईका हिहिन्न िूिागहरू पाइन्छन् । हिहिन्न जातजाहत, िाषा र 
# संस्कृ हतहरूले नेपाललाई अझै रंगीन बनाएका छन् । पययटनका लाहग नेपाल हिश्विरर प्रहसद्ध छ, हिशेषगरी हहमाल 
# चढ्न र प्राकृ हतक सुन्दरताको आनन्द हलन आउने पययटकहरूको आकषयण के न्द्र बनेको छ । """

#     import re

# # Common OCR fixes
#     fixes = {
#         "हहमाल": "हिमाल",
#         "हिहिन्न": "विभिन्न",
#         "िूिाग": "भू-भाग",
#         "पययटन": "पर्यटन",
#         "लाहग": "का लागि",
#         "हिश्विरर": "विश्वभर",
#         "प्रहसद्ध": "प्रसिद्ध",
#         "हिशेषगरी": "विशेषगरी",
#         "प्राकृ हतक": "प्राकृतिक",
#         "हलन": "लिन",
#         "आकषयण के न्द्र": "आकर्षण केन्द्र"
#     }

#     # Apply fixes
#     ocr_text = text  # start with original text
#     for wrong, correct in fixes.items():
#         ocr_text = re.sub(wrong, correct, ocr_text)

#     print(ocr_text)

#     translated_text = translate(ocr_text, "ne", "en")
#     print(f"Translated Text: {translated_text}")

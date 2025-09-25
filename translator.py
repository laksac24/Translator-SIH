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



# # translator.py - Using quantized models for memory efficiency
# import os
# import gc
# import torch
# from typing import Optional

# # Set environment variables to reduce memory usage
# os.environ['TOKENIZERS_PARALLELISM'] = 'false'
# os.environ['OMP_NUM_THREADS'] = '1'

# _model = None
# _tokenizer = None

# def load_quantized_model():
#     """Load model with quantization to reduce memory usage"""
#     global _model, _tokenizer
    
#     try:
#         from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        
#         # Use a smaller multilingual model
#         model_name = "facebook/nllb-200-distilled-600M"  # Much smaller than small100
        
#         print(f"Loading quantized model: {model_name}")
        
#         # Load tokenizer
#         _tokenizer = AutoTokenizer.from_pretrained(model_name)
        
#         # Load model with quantization
#         _model = AutoModelForSeq2SeqLM.from_pretrained(
#             model_name,
#             torch_dtype=torch.float16,  # Use half precision
#             device_map='cpu',
#             low_cpu_mem_usage=True,
#             use_cache=False  # Disable KV cache to save memory
#         )
        
#         # Apply dynamic quantization to reduce memory further
#         try:
#             _model = torch.quantization.quantize_dynamic(
#                 _model, {torch.nn.Linear}, dtype=torch.qint8
#             )
#             print("Applied dynamic quantization")
#         except Exception as e:
#             print(f"Quantization failed, using regular model: {e}")
        
#         print("Model loaded successfully with memory optimizations")
#         return _model, _tokenizer
        
#     except Exception as e:
#         print(f"Failed to load quantized model: {e}")
#         return None, None

# def translate(text: str, src_lang: str, tgt_lang: str) -> str:
#     """
#     Translate using quantized model with memory management
#     """
#     try:
#         model, tokenizer = _model, _tokenizer
        
#         if model is None or tokenizer is None:
#             model, tokenizer = load_quantized_model()
            
#         if model is None or tokenizer is None:
#             return translate_fallback(text, src_lang, tgt_lang)
        
#         # Language code mapping for NLLB
#         lang_codes = {
#             'ne': 'nep_Deva',  # Nepali
#             'si': 'sin_Sinh',  # Sinhala  
#             'en': 'eng_Latn'   # English
#         }
        
#         src_code = lang_codes.get(src_lang, src_lang)
#         tgt_code = lang_codes.get(tgt_lang, tgt_lang)
        
#         # Tokenize with memory constraints
#         tokenizer.src_lang = src_code
#         inputs = tokenizer(
#             text, 
#             return_tensors="pt", 
#             padding=True, 
#             truncation=True, 
#             max_length=256  # Reduced from 512 to save memory
#         )
        
#         # Generate with memory optimizations
#         with torch.no_grad():
#             generated_tokens = model.generate(
#                 **inputs,
#                 forced_bos_token_id=tokenizer.lang_code_to_id[tgt_code],
#                 max_length=256,
#                 num_beams=1,  # Use greedy decoding instead of beam search
#                 do_sample=False,
#                 early_stopping=True
#             )
        
#         # Decode result
#         translated_text = tokenizer.batch_decode(
#             generated_tokens, skip_special_tokens=True
#         )[0]
        
#         # Aggressive memory cleanup
#         del inputs, generated_tokens
#         if torch.cuda.is_available():
#             torch.cuda.empty_cache()
#         gc.collect()
        
#         return translated_text
        
#     except Exception as e:
#         print(f"Quantized translation failed: {e}")
#         return translate_fallback(text, src_lang, tgt_lang)

# def translate_fallback(text: str, src_lang: str, tgt_lang: str) -> str:
#     """Enhanced rule-based fallback with more vocabulary"""
    
#     # Expanded dictionaries
#     nepali_translations = {
#         # Nature & Geography
#         'नेपाल': 'Nepal', 'हिमाल': 'Himalayas', 'पर्वत': 'mountain', 'पहाड': 'hill',
#         'नदी': 'river', 'ताल': 'lake', 'वन': 'forest', 'जंगल': 'jungle',
#         'आकाश': 'sky', 'पानी': 'water', 'हावा': 'air', 'माटो': 'soil',
        
#         # People & Family  
#         'मान्छे': 'person', 'मानिस': 'person', 'आमा': 'mother', 'बुबा': 'father',
#         'छोरा': 'son', 'छोरी': 'daughter', 'दाई': 'elder brother', 'भाइ': 'brother',
#         'दिदी': 'elder sister', 'बहिनी': 'sister', 'परिवार': 'family',
        
#         # Common words
#         'घर': 'house', 'गाउँ': 'village', 'शहर': 'city', 'बाटो': 'road',
#         'स्कुल': 'school', 'काम': 'work', 'खाना': 'food', 'पैसा': 'money',
#         'समय': 'time', 'दिन': 'day', 'रात': 'night', 'बिहान': 'morning',
        
#         # Descriptions
#         'राम्रो': 'good', 'नराम्रो': 'bad', 'सुन्दर': 'beautiful', 'ठूलो': 'big',
#         'सानो': 'small', 'नयाँ': 'new', 'पुरानो': 'old', 'चाहिं': 'then',
        
#         # Actions
#         'जानु': 'to go', 'आउनु': 'to come', 'खानु': 'to eat', 'पिउनु': 'to drink',
#         'सुत्नु': 'to sleep', 'उठ्नु': 'to wake up', 'पढ्नु': 'to read',
        
#         # Culture & Society
#         'भाषा': 'language', 'संस्कृति': 'culture', 'धर्म': 'religion',
#         'त्यौहार': 'festival', 'पर्यटन': 'tourism', 'पर्यटक': 'tourist'
#     }
    
#     sinhala_translations = {
#         # Nature & Geography
#         'ශ්‍රී ලංකාව': 'Sri Lanka', 'කන්ද': 'mountain', 'ගඟ': 'river',
#         'මුහුද': 'ocean', 'වන': 'forest', 'ගම': 'village', 'නගර': 'city',
        
#         # People & Family
#         'මිනිසා': 'person', 'අම්මා': 'mother', 'තාත්තා': 'father',
#         'පුතා': 'son', 'දුව': 'daughter', 'අයියා': 'elder brother',
#         'අක්කා': 'elder sister', 'පවුල': 'family',
        
#         # Common words
#         'ගෙදර': 'house', 'පාසල': 'school', 'වැඩ': 'work', 'කෑම': 'food',
#         'මුදල්': 'money', 'කාලය': 'time', 'දිනය': 'day', 'රාත්‍රිය': 'night',
        
#         # Descriptions
#         'හොඳ': 'good', 'නරක': 'bad', 'ලස්සන': 'beautiful', 'විශාල': 'big',
#         'පොඩි': 'small', 'අලුත්': 'new', 'පැරණි': 'old',
        
#         # Culture & Society
#         'භාෂාව': 'language', 'සංස්කෘතිය': 'culture', 'ආගම': 'religion'
#     }
    
#     # Select dictionary
#     translations = nepali_translations if src_lang == 'ne' else sinhala_translations
    
#     # Enhanced word-by-word translation
#     words = text.split()
#     result = []
    
#     for word in words:
#         clean_word = word.strip('।,.!?;:"()[]{}')
        
#         # Direct lookup
#         if clean_word in translations:
#             result.append(translations[clean_word])
#         # Partial matching for complex words
#         else:
#             found = False
#             for nep_word, eng_word in translations.items():
#                 if nep_word in clean_word:
#                     result.append(f"{eng_word}*")
#                     found = True
#                     break
            
#             if not found:
#                 result.append(f"[{clean_word}]")
    
#     return "[Dictionary] " + " ".join(result)

# def clear_model():
#     """Clear model from memory"""
#     global _model, _tokenizer
    
#     if _model is not None:
#         del _model
#         _model = None
#     if _tokenizer is not None:
#         del _tokenizer
#         _tokenizer = None
    
#     gc.collect()
#     if torch.cuda.is_available():
#         torch.cuda.empty_cache()
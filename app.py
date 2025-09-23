# # # # from typing_extensions import Annotated
# # # # from typing import TypedDict
# # # # from langgraph.graph.message import add_messages
# # # # from langgraph.graph import StateGraph, START, END
# # # # import os
# # # # from pathlib import Path
# # # # from translator import translate

# # # # class State(TypedDict):
# # # #     messages : Annotated[list, add_messages]
# # # #     path : list
# # # #     translated_text : list

# # # # graph_builder = StateGraph(State)

# # # # def file_node(state: State) -> State:
# # # #     file_path = state['path'][-1]
# # # #     state['messages'].append({"role": "system", "content": f"Processing file: {file_path}"})
# # # #     return state

# # # # def png_node(state: State) -> State:
# # # #     from png_extractor import extract_text
# # # #     image_path = state['path'][-1]
# # # #     extracted_text = extract_text(image_path)
# # # #     state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
# # # #     return state

# # # # def pdf_node(state: State) -> State:
# # # #     from pdf_extractor import extract_nepali_sinhala_from_pdf
# # # #     pdf_path = state['path'][-1]
# # # #     extracted_text = extract_nepali_sinhala_from_pdf(pdf_path)
# # # #     state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
# # # #     return state

# # # # def unsupported_file_node(state: State) -> State:
# # # #     """Handle unsupported file types"""
# # # #     file_path = state['path'][-1]
# # # #     state['messages'].append({"role": "system", "content": f"Unsupported file type for: {file_path}"})
# # # #     return state

# # # # def route_file_type(state: State) -> str:
# # # #     """Route to appropriate node based on file extension"""
# # # #     file_path = state['path'][-1].lower()
# # # #     if file_path.endswith('.png'):
# # # #         return "png_node"
# # # #     elif file_path.endswith('.pdf'):
# # # #         return "pdf_node"
# # # #     else:
# # # #         return "unsupported_file_node"

# # # # def translator_node(state: State) -> State:
# # # #     trans_text = translate(str(state["messages"][-1].content), "se", "en")
# # # #     # print(trans_text)
# # # #     state["translated_text"].append(trans_text)
# # # #     return state


# # # # graph_builder.add_node("file_node", file_node)
# # # # graph_builder.add_node("png_node", png_node)
# # # # graph_builder.add_node("pdf_node", pdf_node)
# # # # graph_builder.add_node("unsupported_file_node", unsupported_file_node)
# # # # graph_builder.add_node("translator_node",translator_node)

# # # # graph_builder.add_edge(START, "file_node")
# # # # graph_builder.add_conditional_edges(
# # # #     "file_node",
# # # #     route_file_type,
# # # #     {
# # # #         "png_node": "png_node",
# # # #         "pdf_node": "pdf_node", 
# # # #         "unsupported_file_node": "unsupported_file_node"
# # # #     }
# # # # )
# # # # graph_builder.add_edge("png_node", "translator_node")
# # # # graph_builder.add_edge("pdf_node", "translator_node")
# # # # graph_builder.add_edge("translator_node", END)

# # # # graph = graph_builder.compile()

# # # # test_data_path = Path("test_data")
# # # # test_data_path.mkdir(exist_ok=True)

# # # # for file in test_data_path.glob("*"):
# # # #     if file.is_file():
# # # #         print(f"Processing file: {file}")
# # # #         final_state = graph.invoke({"messages": [], "path": [str(file)], "translated_text":[]})
# # # #         print(final_state['messages'][-1].content)
# # # #         print(final_state["translated_text"][-1])




# # # from typing_extensions import Annotated
# # # from typing import TypedDict
# # # from langgraph.graph.message import add_messages
# # # from langgraph.graph import StateGraph, START, END
# # # import os
# # # from pathlib import Path
# # # from translator import translate

# # # class State(TypedDict):
# # #     messages: Annotated[list, add_messages]
# # #     path: list
# # #     translated_text: list
# # #     detected_language: str

# # # graph_builder = StateGraph(State)

# # # def detect_language(text: str) -> str:
# # #     """Simple language detection for Nepali vs Sinhala"""
# # #     # Nepali Unicode range: \u0900-\u097F (Devanagari)
# # #     nepali_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
    
# # #     # Sinhala Unicode range: \u0D80-\u0DFF  
# # #     sinhala_chars = sum(1 for char in text if '\u0D80' <= char <= '\u0DFF')
    
# # #     # Return language code based on which has more characters
# # #     if sinhala_chars > nepali_chars:
# # #         return "si"  # Sinhala
# # #     else:
# # #         return "ne"  # Nepali (default)

# # # def file_node(state: State) -> State:
# # #     file_path = state['path'][-1]
# # #     state['messages'].append({"role": "system", "content": f"Processing file: {file_path}"})
# # #     return state

# # # def png_node(state: State) -> State:
# # #     from png_extractor import extract_text
# # #     image_path = state['path'][-1]
# # #     extracted_text = extract_text(image_path)
# # #     state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
# # #     return state

# # # def pdf_node(state: State) -> State:
# # #     from pdf_extractor import extract_nepali_sinhala_from_pdf
# # #     pdf_path = state['path'][-1]
# # #     extracted_text = extract_nepali_sinhala_from_pdf(pdf_path)
# # #     state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
# # #     return state

# # # def unsupported_file_node(state: State) -> State:
# # #     file_path = state['path'][-1]
# # #     state['messages'].append({"role": "system", "content": f"Unsupported file type for: {file_path}"})
# # #     return state

# # # def language_detection_node(state: State) -> State:
# # #     """Detect language and store it in state"""
# # #     last_message = state["messages"][-1].content
# # #     extracted_text = last_message.replace("Extracted text: ", "")
    
# # #     detected_lang = detect_language(extracted_text)
# # #     state["detected_language"] = detected_lang
    
# # #     lang_name = "Sinhala" if detected_lang == "si" else "Nepali"
# # #     state['messages'].append({"role": "system", "content": f"Detected language: {lang_name} ({detected_lang})"})
# # #     return state

# # # def translator_node(state: State) -> State:
# # #     """Translate using detected language"""
# # #     last_message = state["messages"][-2].content  # Get extracted text (skip language detection message)
# # #     extracted_text = last_message.replace("Extracted text: ", "")
    
# # #     source_lang = state["detected_language"]
# # #     target_lang = "en"
    
# # #     trans_text = translate(extracted_text, source_lang, target_lang)
# # #     state["translated_text"].append(trans_text)
    
# # #     state['messages'].append({"role": "system", "content": f"Translated ({source_lang} -> {target_lang}): {trans_text}"})
# # #     return state

# # # def route_file_type(state: State) -> str:
# # #     file_path = state['path'][-1].lower()
# # #     if file_path.endswith('.png'):
# # #         return "png_node"
# # #     elif file_path.endswith('.pdf'):
# # #         return "pdf_node"
# # #     else:
# # #         return "unsupported_file_node"

# # # # Add nodes
# # # graph_builder.add_node("file_node", file_node)
# # # graph_builder.add_node("png_node", png_node)
# # # graph_builder.add_node("pdf_node", pdf_node)
# # # graph_builder.add_node("unsupported_file_node", unsupported_file_node)
# # # graph_builder.add_node("language_detection_node", language_detection_node)
# # # graph_builder.add_node("translator_node", translator_node)

# # # # Add edges
# # # graph_builder.add_edge(START, "file_node")
# # # graph_builder.add_conditional_edges(
# # #     "file_node",
# # #     route_file_type,
# # #     {
# # #         "png_node": "png_node",
# # #         "pdf_node": "pdf_node", 
# # #         "unsupported_file_node": "unsupported_file_node"
# # #     }
# # # )

# # # # Both extraction nodes go to language detection
# # # graph_builder.add_edge("png_node", "language_detection_node")
# # # graph_builder.add_edge("pdf_node", "language_detection_node")

# # # # Language detection goes to translation
# # # graph_builder.add_edge("language_detection_node", "translator_node")

# # # # Translation goes to end
# # # graph_builder.add_edge("translator_node", END)

# # # # Unsupported files skip everything
# # # graph_builder.add_edge("unsupported_file_node", END)

# # # graph = graph_builder.compile()

# # # # Test the workflow
# # # test_data_path = Path("test_data")
# # # test_data_path.mkdir(exist_ok=True)

# # # for file in test_data_path.glob("*"):
# # #     if file.is_file():
# # #         print(f"Processing file: {file}")
        
# # #         initial_state = {
# # #             "messages": [], 
# # #             "path": [str(file)], 
# # #             "translated_text": [],
# # #             "detected_language": ""
# # #         }
        
# # #         final_state = graph.invoke(initial_state)
        
# # #         print(f"Final result: {final_state['messages'][-1].content}")
# # #         if final_state["translated_text"]:
# # #             print(f"Translation: {final_state['translated_text'][-1]}")
# # #         print("-" * 50)


# # from typing_extensions import Annotated
# # from typing import TypedDict
# # from langgraph.graph.message import add_messages
# # from langgraph.graph import StateGraph, START, END
# # import os
# # from pathlib import Path
# # from translator import translate

# # class State(TypedDict):
# #     messages: Annotated[list, add_messages]
# #     path: list
# #     translated_text: list
# #     detected_language: str

# # graph_builder = StateGraph(State)

# # def detect_language(text: str) -> str:
# #     """Simple language detection for Nepali vs Sinhala"""
# #     # Nepali Unicode range: \u0900-\u097F (Devanagari)
# #     nepali_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
    
# #     # Sinhala Unicode range: \u0D80-\u0DFF  
# #     sinhala_chars = sum(1 for char in text if '\u0D80' <= char <= '\u0DFF')
    
# #     # Return language code based on which has more characters
# #     if sinhala_chars > nepali_chars:
# #         return "si"  # Sinhala
# #     else:
# #         return "ne"  # Nepali (default)

# # def file_node(state: State) -> State:
# #     file_path = state['path'][-1]
# #     state['messages'].append({"role": "system", "content": f"Processing file: {file_path}"})
# #     return state

# # def png_node(state: State) -> State:
# #     from png_extractor import extract_text
# #     image_path = state['path'][-1]
# #     extracted_text = extract_text(image_path)
# #     state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
# #     return state

# # def pdf_node(state: State) -> State:
# #     from pdf_extractor import extract_nepali_sinhala_from_pdf
# #     pdf_path = state['path'][-1]
# #     extracted_text = extract_nepali_sinhala_from_pdf(pdf_path)
# #     state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
# #     return state

# # def unsupported_file_node(state: State) -> State:
# #     file_path = state['path'][-1]
# #     state['messages'].append({"role": "system", "content": f"Unsupported file type for: {file_path}"})
# #     return state

# # def language_detection_node(state: State) -> State:
# #     """Detect language and store it in state"""
# #     last_message = state["messages"][-1].content
# #     extracted_text = last_message.replace("Extracted text: ", "")
    
# #     detected_lang = detect_language(extracted_text)
# #     state["detected_language"] = detected_lang
    
# #     lang_name = "Sinhala" if detected_lang == "si" else "Nepali"
# #     state['messages'].append({"role": "system", "content": f"Detected language: {lang_name} ({detected_lang})"})
# #     return state

# # def translator_node(state: State) -> State:
# #     """Translate using detected language"""
# #     # Find the extracted text message (not the language detection message)
# #     extracted_text = ""
# #     for msg in state["messages"]:
# #         if msg.content.startswith("Extracted text: "):
# #             extracted_text = msg.content.replace("Extracted text: ", "")
# #             break
    
# #     if not extracted_text:
# #         state['messages'].append({"role": "system", "content": "No extracted text found for translation"})
# #         return state
    
# #     source_lang = state["detected_language"]
# #     target_lang = "en"
    
# #     trans_text = translate(extracted_text, source_lang, target_lang)
# #     state["translated_text"].append(trans_text)
    
# #     state['messages'].append({"role": "system", "content": f"Translated ({source_lang} -> {target_lang}): {trans_text}"})
# #     return state

# # def route_file_type(state: State) -> str:
# #     file_path = state['path'][-1].lower()
# #     if file_path.endswith('.png'):
# #         return "png_node"
# #     elif file_path.endswith('.pdf'):
# #         return "pdf_node"
# #     else:
# #         return "unsupported_file_node"

# # # Add nodes
# # graph_builder.add_node("file_node", file_node)
# # graph_builder.add_node("png_node", png_node)
# # graph_builder.add_node("pdf_node", pdf_node)
# # graph_builder.add_node("unsupported_file_node", unsupported_file_node)
# # graph_builder.add_node("language_detection_node", language_detection_node)
# # graph_builder.add_node("translator_node", translator_node)

# # # Add edges
# # graph_builder.add_edge(START, "file_node")
# # graph_builder.add_conditional_edges(
# #     "file_node",
# #     route_file_type,
# #     {
# #         "png_node": "png_node",
# #         "pdf_node": "pdf_node", 
# #         "unsupported_file_node": "unsupported_file_node"
# #     }
# # )

# # # Both extraction nodes go to language detection
# # graph_builder.add_edge("png_node", "language_detection_node")
# # graph_builder.add_edge("pdf_node", "language_detection_node")

# # # Language detection goes to translation
# # graph_builder.add_edge("language_detection_node", "translator_node")

# # # Translation goes to end
# # graph_builder.add_edge("translator_node", END)

# # # Unsupported files skip everything
# # graph_builder.add_edge("unsupported_file_node", END)

# # graph = graph_builder.compile()

# # # Test the workflow
# # test_data_path = Path("test_data")
# # test_data_path.mkdir(exist_ok=True)

# # for file in test_data_path.glob("*"):
# #     if file.is_file():
# #         print(f"\nProcessing file: {file}")
        
# #         initial_state = {
# #             "messages": [], 
# #             "path": [str(file)], 
# #             "translated_text": [],
# #             "detected_language": ""
# #         }
        
# #         final_state = graph.invoke(initial_state)
        
# #         # Extract and display extracted text
# #         extracted_text = ""
# #         for msg in final_state['messages']:
# #             if msg.content.startswith("Extracted text: "):
# #                 extracted_text = msg.content.replace("Extracted text: ", "")
# #                 break
        
# #         print(f"Extracted Text: {extracted_text}")
# #         print(f"Detected Language: {final_state.get('detected_language', 'Unknown')}")
        
# #         if final_state["translated_text"]:
# #             print(f"Translated Text: {final_state['translated_text'][-1]}")
        
# #         print("-" * 50)


# # from typing_extensions import Annotated
# # from typing import TypedDict
# # from langgraph.graph.message import add_messages
# # from langgraph.graph import StateGraph, START, END
# # import os
# # from pathlib import Path
# # from translator import translate
# # from word_dictionary import correct_words

# # class State(TypedDict):
# #     messages: Annotated[list, add_messages]
# #     path: list
# #     translated_text: list
# #     detected_language: str

# # graph_builder = StateGraph(State)

# # def detect_language(text: str) -> str:
# #     """Simple language detection for Nepali vs Sinhala"""
# #     # Nepali Unicode range: \u0900-\u097F (Devanagari)
# #     nepali_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
    
# #     # Sinhala Unicode range: \u0D80-\u0DFF  
# #     sinhala_chars = sum(1 for char in text if '\u0D80' <= char <= '\u0DFF')
    
# #     # Return language code based on which has more characters
# #     if sinhala_chars > nepali_chars:
# #         return "si"  # Sinhala
# #     else:
# #         return "ne"  # Nepali (default)

# # def file_node(state: State) -> State:
# #     file_path = state['path'][-1]
# #     state['messages'].append({"role": "system", "content": f"Processing file: {file_path}"})
# #     return state

# # def png_node(state: State) -> State:
# #     from png_extractor import extract_text
# #     image_path = state['path'][-1]
# #     extracted_text = extract_text(image_path)
# #     state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
# #     return state

# # def pdf_node(state: State) -> State:
# #     from pdf_extractor import extract_nepali_sinhala_from_pdf
# #     pdf_path = state['path'][-1]
# #     extracted_text = extract_nepali_sinhala_from_pdf(pdf_path)
# #     state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
# #     return state

# # def unsupported_file_node(state: State) -> State:
# #     file_path = state['path'][-1]
# #     state['messages'].append({"role": "system", "content": f"Unsupported file type for: {file_path}"})
# #     return state

# # def language_detection_node(state: State) -> State:
# #     """Detect language and store it in state"""
# #     last_message = state["messages"][-1].content
# #     extracted_text = last_message.replace("Extracted text: ", "")
    
# #     detected_lang = detect_language(extracted_text)
# #     state["detected_language"] = detected_lang
    
# #     lang_name = "Sinhala" if detected_lang == "si" else "Nepali"
# #     state['messages'].append({"role": "system", "content": f"Detected language: {lang_name} ({detected_lang})"})
# #     return state

# # def ocr_correction_node(state: State) -> State:
# #     """Apply word-based OCR corrections using dictionary lookup"""
# #     # Find the extracted text
# #     extracted_text = ""
# #     for msg in state["messages"]:
# #         if msg.content.startswith("Extracted text: "):
# #             extracted_text = msg.content.replace("Extracted text: ", "")
# #             break
    
# #     if not extracted_text:
# #         state['messages'].append({"role": "system", "content": "No extracted text found for OCR correction"})
# #         return state
    
# #     detected_lang = state["detected_language"]
    
# #     # Apply dictionary-based word corrections
# #     corrected_text = correct_words(extracted_text, detected_lang)
    
# #     # Add corrected text to messages
# #     state['messages'].append({"role": "system", "content": f"OCR corrected text: {corrected_text}"})
# #     return state

# # def ocr_correction_node(state: State) -> State:
# #     """Apply word-based OCR corrections using dictionary lookup"""
# #     # Find the extracted text
# #     extracted_text = ""
# #     for msg in state["messages"]:
# #         if msg.content.startswith("Extracted text: "):
# #             extracted_text = msg.content.replace("Extracted text: ", "")
# #             break
    
# #     if not extracted_text:
# #         state['messages'].append({"role": "system", "content": "No extracted text found for OCR correction"})
# #         return state
    
# #     detected_lang = state["detected_language"]
    
# #     # Apply dictionary-based word corrections
# #     corrected_text = correct_words(extracted_text, detected_lang)
    
# #     # Add corrected text to messages
# #     state['messages'].append({"role": "system", "content": f"OCR corrected text: {corrected_text}"})
# #     return state

# # def translator_node(state: State) -> State:
# #     """Translate using detected language and OCR corrected text"""
# #     # Find the OCR corrected text (preferred) or fallback to extracted text
# #     text_to_translate = ""
# #     for msg in state["messages"]:
# #         if msg.content.startswith("OCR corrected text: "):
# #             text_to_translate = msg.content.replace("OCR corrected text: ", "")
# #             break
    
# #     # Fallback to extracted text if no corrected text found
# #     if not text_to_translate:
# #         for msg in state["messages"]:
# #             if msg["content"].startswith("Extracted text: "):
# #                 text_to_translate = msg.content.replace("Extracted text: ", "")
# #                 break
    
# #     if not text_to_translate:
# #         state['messages'].append({"role": "system", "content": "No text found for translation"})
# #         return state
    
# #     source_lang = state["detected_language"]
# #     target_lang = "en"
    
# #     trans_text = translate(text_to_translate, source_lang, target_lang)
# #     state["translated_text"].append(trans_text)
    
# #     state['messages'].append({"role": "system", "content": f"Translated ({source_lang} -> {target_lang}): {trans_text}"})
# #     return state

# # def route_file_type(state: State) -> str:
# #     file_path = state['path'][-1].lower()
# #     if file_path.endswith('.png'):
# #         return "png_node"
# #     elif file_path.endswith('.pdf'):
# #         return "pdf_node"
# #     else:
# #         return "unsupported_file_node"

# # # Add nodes
# # graph_builder.add_node("file_node", file_node)
# # graph_builder.add_node("png_node", png_node)
# # graph_builder.add_node("pdf_node", pdf_node)
# # graph_builder.add_node("unsupported_file_node", unsupported_file_node)
# # graph_builder.add_node("language_detection_node", language_detection_node)
# # graph_builder.add_node("ocr_correction_node", ocr_correction_node)
# # graph_builder.add_node("translator_node", translator_node)

# # # Add edges
# # graph_builder.add_edge(START, "file_node")
# # graph_builder.add_conditional_edges(
# #     "file_node",
# #     route_file_type,
# #     {
# #         "png_node": "png_node",
# #         "pdf_node": "pdf_node", 
# #         "unsupported_file_node": "unsupported_file_node"
# #     }
# # )

# # # Both extraction nodes go to language detection
# # graph_builder.add_edge("png_node", "language_detection_node")
# # graph_builder.add_edge("pdf_node", "language_detection_node")

# # # Language detection goes to OCR correction
# # graph_builder.add_edge("language_detection_node", "ocr_correction_node")

# # # OCR correction goes to translation
# # graph_builder.add_edge("ocr_correction_node", "translator_node")

# # # Translation goes to end
# # graph_builder.add_edge("translator_node", END)

# # # Unsupported files skip everything
# # graph_builder.add_edge("unsupported_file_node", END)

# # graph = graph_builder.compile()

# # # Test the workflow
# # test_data_path = Path("test_data")
# # test_data_path.mkdir(exist_ok=True)

# # for file in test_data_path.glob("*"):
# #     if file.is_file():
# #         print(f"\nProcessing file: {file}")
        
# #         initial_state = {
# #             "messages": [], 
# #             "path": [str(file)], 
# #             "translated_text": [],
# #             "detected_language": ""
# #         }
        
# #         final_state = graph.invoke(initial_state)
        
# #         # Extract and display texts
# #         extracted_text = ""
# #         corrected_text = ""
# #         for msg in final_state['messages']:
# #             if msg.content.startswith("Extracted text: "):
# #                 extracted_text = msg.content.replace("Extracted text: ", "")
# #             elif msg.content.startswith("OCR corrected text: "):
# #                 corrected_text = msg.content.replace("OCR corrected text: ", "")
        
# #         print(f"Extracted Text: {extracted_text}")
# #         if corrected_text:
# #             print(f"OCR Corrected Text: {corrected_text}")
# #         print(f"Detected Language: {final_state.get('detected_language', 'Unknown')}")
        
# #         if final_state["translated_text"]:
# #             print(f"Translated Text: {final_state['translated_text'][-1]}")
        
# #         print("-" * 50)


# # main.py - Single Service with Upload and Results
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from typing import List, Dict, Any
# from typing_extensions import Annotated
# from typing import TypedDict
# from langgraph.graph.message import add_messages
# from langgraph.graph import StateGraph, START, END
# import os
# import shutil
# from pathlib import Path
# import uuid
# import json
# from datetime import datetime
# import threading
# import time

# app = FastAPI(title="Document Translation Service", version="1.0.0")

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Create directories
# UPLOAD_DIR = Path("uploaded_files")
# RESULTS_DIR = Path("results")
# UPLOAD_DIR.mkdir(exist_ok=True)
# RESULTS_DIR.mkdir(exist_ok=True)

# # Import your translation modules
# try:
#     from translator import translate
#     from word_dictionary import correct_words
# except ImportError:
#     print("Warning: Translation modules not found. Using mock functions.")
#     def translate(text, source, target):
#         return f"[MOCK TRANSLATION] {text}"
#     def correct_words(text, lang):
#         return text

# # State definition for LangGraph
# class State(TypedDict):
#     messages: Annotated[list, add_messages]
#     path: list
#     translated_text: list
#     detected_language: str

# def detect_language(text: str) -> str:
#     """Simple language detection for Nepali vs Sinhala"""
#     nepali_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
#     sinhala_chars = sum(1 for char in text if '\u0D80' <= char <= '\u0DFF')
    
#     if sinhala_chars > nepali_chars:
#         return "si"  # Sinhala
#     else:
#         return "ne"  # Nepali (default)

# def file_node(state: State) -> State:
#     file_path = state['path'][-1]
#     state['messages'].append({"role": "system", "content": f"Processing file: {file_path}"})
#     return state

# def png_node(state: State) -> State:
#     try:
#         from png_extractor import extract_text
#         image_path = state['path'][-1]
#         extracted_text = extract_text(image_path)
#         state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
#     except Exception as e:
#         state['messages'].append({"role": "system", "content": f"Error extracting from PNG: {str(e)}"})
#     return state

# def pdf_node(state: State) -> State:
#     try:
#         from pdf_extractor import extract_nepali_sinhala_from_pdf
#         pdf_path = state['path'][-1]
#         extracted_text = extract_nepali_sinhala_from_pdf(pdf_path)
#         state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
#     except Exception as e:
#         state['messages'].append({"role": "system", "content": f"Error extracting from PDF: {str(e)}"})
#     return state

# def unsupported_file_node(state: State) -> State:
#     file_path = state['path'][-1]
#     state['messages'].append({"role": "system", "content": f"Unsupported file type for: {file_path}"})
#     return state

# def language_detection_node(state: State) -> State:
#     last_message = state["messages"][-1].content
#     extracted_text = last_message.replace("Extracted text: ", "")
    
#     detected_lang = detect_language(extracted_text)
#     state["detected_language"] = detected_lang
    
#     lang_name = "Sinhala" if detected_lang == "si" else "Nepali"
#     state['messages'].append({"role": "system", "content": f"Detected language: {lang_name} ({detected_lang})"})
#     return state

# def ocr_correction_node(state: State) -> State:
#     extracted_text = ""
#     for msg in state["messages"]:
#         if msg.content.startswith("Extracted text: "):
#             extracted_text = msg.content.replace("Extracted text: ", "")
#             break
    
#     if not extracted_text:
#         state['messages'].append({"role": "system", "content": "No extracted text found for OCR correction"})
#         return state
    
#     detected_lang = state["detected_language"]
#     corrected_text = correct_words(extracted_text, detected_lang)
#     state['messages'].append({"role": "system", "content": f"OCR corrected text: {corrected_text}"})
#     return state

# def translator_node(state: State) -> State:
#     text_to_translate = ""
#     for msg in state["messages"]:
#         if msg.content.startswith("OCR corrected text: "):
#             text_to_translate = msg.content.replace("OCR corrected text: ", "")
#             break
    
#     if not text_to_translate:
#         for msg in state["messages"]:
#             if msg.content.startswith("Extracted text: "):
#                 text_to_translate = msg.content.replace("Extracted text: ", "")
#                 break
    
#     if not text_to_translate:
#         state['messages'].append({"role": "system", "content": "No text found for translation"})
#         return state
    
#     source_lang = state["detected_language"]
#     target_lang = "en"
    
#     try:
#         trans_text = translate(text_to_translate, source_lang, target_lang)
#         state["translated_text"].append(trans_text)
#         state['messages'].append({"role": "system", "content": f"Translated ({source_lang} -> {target_lang}): {trans_text}"})
#     except Exception as e:
#         error_msg = f"Translation error: {str(e)}"
#         state['messages'].append({"role": "system", "content": error_msg})
#         state["translated_text"].append(f"Error: {str(e)}")
    
#     return state

# def route_file_type(state: State) -> str:
#     file_path = state['path'][-1].lower()
#     if file_path.endswith('.png') or file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
#         return "png_node"
#     elif file_path.endswith('.pdf'):
#         return "pdf_node"
#     else:
#         return "unsupported_file_node"

# # Build the graph
# graph_builder = StateGraph(State)
# graph_builder.add_node("file_node", file_node)
# graph_builder.add_node("png_node", png_node)
# graph_builder.add_node("pdf_node", pdf_node)
# graph_builder.add_node("unsupported_file_node", unsupported_file_node)
# graph_builder.add_node("language_detection_node", language_detection_node)
# graph_builder.add_node("ocr_correction_node", ocr_correction_node)
# graph_builder.add_node("translator_node", translator_node)

# graph_builder.add_edge(START, "file_node")
# graph_builder.add_conditional_edges(
#     "file_node",
#     route_file_type,
#     {
#         "png_node": "png_node",
#         "pdf_node": "pdf_node", 
#         "unsupported_file_node": "unsupported_file_node"
#     }
# )

# graph_builder.add_edge("png_node", "language_detection_node")
# graph_builder.add_edge("pdf_node", "language_detection_node")
# graph_builder.add_edge("language_detection_node", "ocr_correction_node")
# graph_builder.add_edge("ocr_correction_node", "translator_node")
# graph_builder.add_edge("translator_node", END)
# graph_builder.add_edge("unsupported_file_node", END)

# graph = graph_builder.compile()

# # Global processing status
# processing_status = {"active": False, "current_file": None, "processed_count": 0}

# def process_files_background():
#     """Background task to process uploaded files"""
#     global processing_status
    
#     while True:
#         try:
#             # Check for files to process
#             files_to_process = list(UPLOAD_DIR.glob("*"))
            
#             if files_to_process and not processing_status["active"]:
#                 processing_status["active"] = True
                
#                 for file_path in files_to_process:
#                     if file_path.is_file():
#                         processing_status["current_file"] = file_path.name
#                         print(f"Processing: {file_path}")
                        
#                         # Process file through the graph
#                         initial_state = {
#                             "messages": [], 
#                             "path": [str(file_path)], 
#                             "translated_text": [],
#                             "detected_language": ""
#                         }
                        
#                         final_state = graph.invoke(initial_state)
                        
#                         # Extract only the translated text
#                         translated_text = final_state["translated_text"][-1] if final_state["translated_text"] else "Translation failed"
                        
#                         # Save only the translated text result
#                         result = {
#                             "document_name": file_path.name,
#                             "translated_text": translated_text,
#                             "processed_time": datetime.now().isoformat()
#                         }
                        
#                         # Save to results directory
#                         result_file = RESULTS_DIR / f"result_{file_path.stem}.json"
#                         with open(result_file, "w", encoding="utf-8") as f:
#                             json.dump(result, f, indent=2, ensure_ascii=False)
                        
#                         # Remove processed file
#                         file_path.unlink()
#                         processing_status["processed_count"] += 1
                
#                 processing_status["active"] = False
#                 processing_status["current_file"] = None
            
#             time.sleep(5)  # Check every 5 seconds
            
#         except Exception as e:
#             print(f"Error in background processing: {e}")
#             processing_status["active"] = False
#             processing_status["current_file"] = None
#             time.sleep(10)

# # Start background processing thread
# processing_thread = threading.Thread(target=process_files_background, daemon=True)
# processing_thread.start()

# # ============================================================================
# # API ENDPOINTS
# # ============================================================================

# @app.post("/upload", response_model=Dict[str, Any])
# async def upload_files(files: List[UploadFile] = File(...)):
#     """Upload multiple files (PDF/PNG/JPG) for processing"""
#     try:
#         uploaded_files = []
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
#         for file in files:
#             # Validate file type
#             file_extension = Path(file.filename).suffix.lower()
#             if file_extension not in ['.pdf', '.png', '.jpg', '.jpeg']:
#                 raise HTTPException(
#                     status_code=400, 
#                     detail=f"Unsupported file type: {file_extension}. Only PDF, PNG, JPG are allowed."
#                 )
            
#             # Generate unique filename
#             unique_filename = f"{timestamp}_{uuid.uuid4().hex[:8]}_{file.filename}"
#             file_path = UPLOAD_DIR / unique_filename
            
#             # Save file
#             with open(file_path, "wb") as buffer:
#                 shutil.copyfileobj(file.file, buffer)
            
#             uploaded_files.append({
#                 "original_name": file.filename,
#                 "stored_name": unique_filename,
#                 "file_path": str(file_path),
#                 "file_type": file_extension,
#                 "upload_time": timestamp
#             })
        
#         # Save upload log
#         log_file = RESULTS_DIR / f"upload_log_{timestamp}.json"
#         with open(log_file, "w") as f:
#             json.dump({
#                 "timestamp": timestamp,
#                 "uploaded_files": uploaded_files,
#                 "status": "uploaded"
#             }, f, indent=2)
        
#         return {
#             "status": "success",
#             "message": f"Successfully uploaded {len(uploaded_files)} files",
#             "upload_id": timestamp,
#             "files": uploaded_files
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")

# @app.get("/results")
# async def get_translated_results():
#     """Get only the translated text results - Clean API response"""
#     try:
#         results = []
        
#         for result_file in RESULTS_DIR.glob("result_*.json"):
#             with open(result_file, "r", encoding="utf-8") as f:
#                 result_data = json.load(f)
#                 # Return only the essential data
#                 clean_result = {
#                     "document": result_data["document_name"],
#                     "translation": result_data["translated_text"],
#                     "processed_at": result_data["processed_time"]
#                 }
#                 results.append(clean_result)
        
#         # Sort by processed time (newest first)
#         results.sort(key=lambda x: x.get("processed_at", ""), reverse=True)
        
#         return results
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting results: {str(e)}")

# @app.get("/results/{document_name}")
# async def get_single_result(document_name: str):
#     """Get translated text for a specific document"""
#     try:
#         # Try to find the result file for this document
#         for result_file in RESULTS_DIR.glob("result_*.json"):
#             with open(result_file, "r", encoding="utf-8") as f:
#                 result_data = json.load(f)
#                 if result_data["document_name"] == document_name or document_name in result_data["document_name"]:
#                     return {
#                         "document": result_data["document_name"],
#                         "translation": result_data["translated_text"],
#                         "processed_at": result_data["processed_time"]
#                     }
        
#         raise HTTPException(status_code=404, detail="Document not found")
    
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting result: {str(e)}")

# @app.get("/translations")
# async def get_translations_only():
#     """Get only the translated text strings - Minimal response"""
#     try:
#         translations = []
        
#         for result_file in RESULTS_DIR.glob("result_*.json"):
#             with open(result_file, "r", encoding="utf-8") as f:
#                 result_data = json.load(f)
#                 translations.append(result_data["translated_text"])
        
#         return translations
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting translations: {str(e)}")

# @app.get("/queue")
# async def check_queue():
#     """Check how many files are waiting to be processed"""
#     try:
#         files = list(UPLOAD_DIR.glob("*"))
#         pending_files = [f.name for f in files if f.is_file()]
        
#         return {
#             "status": "success",
#             "pending_files": len(pending_files),
#             "files": pending_files
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error checking queue: {str(e)}")

# @app.get("/status")
# async def get_processing_status():
#     """Get current processing status"""
#     try:
#         pending_files = len(list(UPLOAD_DIR.glob("*")))
        
#         return {
#             "status": "processing" if processing_status["active"] else "idle",
#             "pending_files": pending_files,
#             "processed_count": processing_status["processed_count"]
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")

# @app.delete("/results")
# async def clear_results():
#     """Clear all results"""
#     try:
#         deleted_count = 0
        
#         for result_file in RESULTS_DIR.glob("result_*.json"):
#             result_file.unlink()
#             deleted_count += 1
        
#         processing_status["processed_count"] = 0
        
#         return {
#             "message": f"Cleared {deleted_count} results"
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error clearing results: {str(e)}")

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {"status": "healthy", "service": "Translation Service", "port": 8000}

# if __name__ == "__main__":
#     import uvicorn
#     print("🚀 Starting Document Translation Service on port 8000...")
#     print("📤 Upload files: POST http://localhost:8000/upload")
#     print("📊 Get results: GET http://localhost:8000/results")
#     print("🔗 API Endpoints:")
#     print("   • GET /results - All translations with metadata")
#     print("   • GET /translations - Only translated text strings")
#     print("   • GET /results/{document_name} - Single document result")
#     print("   • GET /queue - Check processing queue")
#     print("   • GET /status - Processing status")
#     print("📖 API Docs: http://localhost:8000/docs")
#     print("\n" + "="*60)
#     uvicorn.run(app, host="0.0.0.0", port=8000)



# # main.py - Single Service with Upload and Results
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from typing import List, Dict, Any
# from typing_extensions import Annotated
# from typing import TypedDict
# from langgraph.graph.message import add_messages
# from langgraph.graph import StateGraph, START, END
# import os
# import shutil
# from pathlib import Path
# import uuid
# import json
# from datetime import datetime
# import threading
# import time

# app = FastAPI(title="Document Translation Service", version="1.0.0")

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Create directories
# UPLOAD_DIR = Path("uploaded_files")
# RESULTS_DIR = Path("results")
# UPLOAD_DIR.mkdir(exist_ok=True)
# RESULTS_DIR.mkdir(exist_ok=True)

# # Import your translation modules
# try:
#     from translator import translate
#     from word_dictionary import correct_words
# except ImportError:
#     print("Warning: Translation modules not found. Using mock functions.")
#     def translate(text, source, target):
#         return f"[MOCK TRANSLATION] {text}"
#     def correct_words(text, lang):
#         return text

# # State definition for LangGraph
# class State(TypedDict):
#     messages: Annotated[list, add_messages]
#     path: list
#     translated_text: list
#     detected_language: str

# def detect_language(text: str) -> str:
#     """Simple language detection for Nepali vs Sinhala"""
#     nepali_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
#     sinhala_chars = sum(1 for char in text if '\u0D80' <= char <= '\u0DFF')
    
#     if sinhala_chars > nepali_chars:
#         return "si"  # Sinhala
#     else:
#         return "ne"  # Nepali (default)

# def file_node(state: State) -> State:
#     file_path = state['path'][-1]
#     state['messages'].append({"role": "system", "content": f"Processing file: {file_path}"})
#     return state

# def png_node(state: State) -> State:
#     try:
#         from png_extractor import extract_text
#         image_path = state['path'][-1]
#         extracted_text = extract_text(image_path)
#         state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
#     except Exception as e:
#         state['messages'].append({"role": "system", "content": f"Error extracting from PNG: {str(e)}"})
#     return state

# def pdf_node(state: State) -> State:
#     try:
#         from pdf_extractor import extract_nepali_sinhala_from_pdf
#         pdf_path = state['path'][-1]
#         extracted_text = extract_nepali_sinhala_from_pdf(pdf_path)
#         state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
#     except Exception as e:
#         state['messages'].append({"role": "system", "content": f"Error extracting from PDF: {str(e)}"})
#     return state

# def unsupported_file_node(state: State) -> State:
#     file_path = state['path'][-1]
#     state['messages'].append({"role": "system", "content": f"Unsupported file type for: {file_path}"})
#     return state

# def language_detection_node(state: State) -> State:
#     last_message = state["messages"][-1].content
#     extracted_text = last_message.replace("Extracted text: ", "")
    
#     detected_lang = detect_language(extracted_text)
#     state["detected_language"] = detected_lang
    
#     lang_name = "Sinhala" if detected_lang == "si" else "Nepali"
#     state['messages'].append({"role": "system", "content": f"Detected language: {lang_name} ({detected_lang})"})
#     return state

# def ocr_correction_node(state: State) -> State:
#     extracted_text = ""
#     for msg in state["messages"]:
#         if msg.content.startswith("Extracted text: "):
#             extracted_text = msg.content.replace("Extracted text: ", "")
#             break
    
#     if not extracted_text:
#         state['messages'].append({"role": "system", "content": "No extracted text found for OCR correction"})
#         return state
    
#     detected_lang = state["detected_language"]
#     corrected_text = correct_words(extracted_text, detected_lang)
#     state['messages'].append({"role": "system", "content": f"OCR corrected text: {corrected_text}"})
#     return state

# def translator_node(state: State) -> State:
#     text_to_translate = ""
#     for msg in state["messages"]:
#         if msg.content.startswith("OCR corrected text: "):
#             text_to_translate = msg.content.replace("OCR corrected text: ", "")
#             break
    
#     if not text_to_translate:
#         for msg in state["messages"]:
#             if msg.content.startswith("Extracted text: "):
#                 text_to_translate = msg.content.replace("Extracted text: ", "")
#                 break
    
#     if not text_to_translate:
#         state['messages'].append({"role": "system", "content": "No text found for translation"})
#         return state
    
#     source_lang = state["detected_language"]
#     target_lang = "en"
    
#     try:
#         trans_text = translate(text_to_translate, source_lang, target_lang)
#         state["translated_text"].append(trans_text)
#         state['messages'].append({"role": "system", "content": f"Translated ({source_lang} -> {target_lang}): {trans_text}"})
#     except Exception as e:
#         error_msg = f"Translation error: {str(e)}"
#         state['messages'].append({"role": "system", "content": error_msg})
#         state["translated_text"].append(f"Error: {str(e)}")
    
#     return state

# def route_file_type(state: State) -> str:
#     file_path = state['path'][-1].lower()
#     if file_path.endswith('.png') or file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
#         return "png_node"
#     elif file_path.endswith('.pdf'):
#         return "pdf_node"
#     else:
#         return "unsupported_file_node"

# # Build the graph
# graph_builder = StateGraph(State)
# graph_builder.add_node("file_node", file_node)
# graph_builder.add_node("png_node", png_node)
# graph_builder.add_node("pdf_node", pdf_node)
# graph_builder.add_node("unsupported_file_node", unsupported_file_node)
# graph_builder.add_node("language_detection_node", language_detection_node)
# graph_builder.add_node("ocr_correction_node", ocr_correction_node)
# graph_builder.add_node("translator_node", translator_node)

# graph_builder.add_edge(START, "file_node")
# graph_builder.add_conditional_edges(
#     "file_node",
#     route_file_type,
#     {
#         "png_node": "png_node",
#         "pdf_node": "pdf_node", 
#         "unsupported_file_node": "unsupported_file_node"
#     }
# )

# graph_builder.add_edge("png_node", "language_detection_node")
# graph_builder.add_edge("pdf_node", "language_detection_node")
# graph_builder.add_edge("language_detection_node", "ocr_correction_node")
# graph_builder.add_edge("ocr_correction_node", "translator_node")
# graph_builder.add_edge("translator_node", END)
# graph_builder.add_edge("unsupported_file_node", END)

# graph = graph_builder.compile()

# # Global processing status
# processing_status = {"active": False, "current_file": None, "processed_count": 0}

# def process_files_background():
#     """Background task to process uploaded files"""
#     global processing_status
    
#     while True:
#         try:
#             # Check for files to process
#             files_to_process = list(UPLOAD_DIR.glob("*"))
            
#             if files_to_process and not processing_status["active"]:
#                 processing_status["active"] = True
                
#                 for file_path in files_to_process:
#                     if file_path.is_file():
#                         processing_status["current_file"] = file_path.name
#                         print(f"Processing: {file_path}")
                        
#                         # Process file through the graph
#                         initial_state = {
#                             "messages": [], 
#                             "path": [str(file_path)], 
#                             "translated_text": [],
#                             "detected_language": ""
#                         }
                        
#                         final_state = graph.invoke(initial_state)
                        
#                         # Extract only the translated text
#                         translated_text = final_state["translated_text"][-1] if final_state["translated_text"] else "Translation failed"
                        
#                         # Extract session ID from filename (format: session_xxxxx_timestamp_uuid_filename)
#                         filename_parts = file_path.name.split('_')
#                         if len(filename_parts) >= 2 and filename_parts[0] == 'session':
#                             session_id = filename_parts[0] + '_' + filename_parts[1]
#                         else:
#                             # Fallback for files without session ID
#                             session_id = "legacy_session"
                        
#                         # Save only the translated text result with session ID
#                         result = {
#                             "session_id": session_id,
#                             "document_name": file_path.name,
#                             "translated_text": translated_text,
#                             "processed_time": datetime.now().isoformat()
#                         }
                        
#                         # Save to results directory with session ID
#                         result_file = RESULTS_DIR / f"{session_id}_result_{file_path.stem}.json"
#                         with open(result_file, "w", encoding="utf-8") as f:
#                             json.dump(result, f, indent=2, ensure_ascii=False)
                        
#                         # Remove processed file
#                         file_path.unlink()
#                         processing_status["processed_count"] += 1
                
#                 processing_status["active"] = False
#                 processing_status["current_file"] = None
            
#             time.sleep(5)  # Check every 5 seconds
            
#         except Exception as e:
#             print(f"Error in background processing: {e}")
#             processing_status["active"] = False
#             processing_status["current_file"] = None
#             time.sleep(10)

# # Start background processing thread
# processing_thread = threading.Thread(target=process_files_background, daemon=True)
# processing_thread.start()

# # ============================================================================
# # API ENDPOINTS
# # ============================================================================

# @app.post("/upload", response_model=Dict[str, Any])
# async def upload_files(files: List[UploadFile] = File(...)):
#     """Upload multiple files (PDF/PNG/JPG) for processing"""
#     try:
#         uploaded_files = []
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         # Generate unique session ID
#         session_id = f"session_{uuid.uuid4().hex[:12]}"
        
#         for file in files:
#             # Validate file type
#             file_extension = Path(file.filename).suffix.lower()
#             if file_extension not in ['.pdf', '.png', '.jpg', '.jpeg']:
#                 raise HTTPException(
#                     status_code=400, 
#                     detail=f"Unsupported file type: {file_extension}. Only PDF, PNG, JPG are allowed."
#                 )
            
#             # Generate unique filename with session ID
#             unique_filename = f"{session_id}_{timestamp}_{uuid.uuid4().hex[:8]}_{file.filename}"
#             file_path = UPLOAD_DIR / unique_filename
            
#             # Save file
#             with open(file_path, "wb") as buffer:
#                 shutil.copyfileobj(file.file, buffer)
            
#             uploaded_files.append({
#                 "original_name": file.filename,
#                 "stored_name": unique_filename,
#                 "file_path": str(file_path),
#                 "file_type": file_extension,
#                 "upload_time": timestamp,
#                 "session_id": session_id
#             })
        
#         # Save upload log with session ID
#         log_file = RESULTS_DIR / f"upload_log_{session_id}_{timestamp}.json"
#         with open(log_file, "w") as f:
#             json.dump({
#                 "session_id": session_id,
#                 "timestamp": timestamp,
#                 "uploaded_files": uploaded_files,
#                 "status": "uploaded"
#             }, f, indent=2)
        
#         return {
#             "status": "success",
#             "message": f"Successfully uploaded {len(uploaded_files)} files",
#             "session_id": session_id,
#             "upload_id": timestamp,
#             "files": uploaded_files
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")

# @app.get("/results")
# async def get_all_results():
#     """Get all translated results from all sessions"""
#     try:
#         results = []
        
#         # Check both new session-based files and legacy files
#         for result_file in RESULTS_DIR.glob("*result*.json"):
#             try:
#                 with open(result_file, "r", encoding="utf-8") as f:
#                     result_data = json.load(f)
                    
#                     # Handle both new and legacy file formats
#                     session_id = result_data.get("session_id", "unknown_session")
                    
#                     clean_result = {
#                         "session_id": session_id,
#                         "document": result_data["document_name"],
#                         "translation": result_data["translated_text"],
#                         "processed_at": result_data["processed_time"]
#                     }
#                     results.append(clean_result)
#             except (json.JSONDecodeError, KeyError) as e:
#                 print(f"Error reading result file {result_file}: {e}")
#                 continue
        
#         # Sort by processed time (newest first)
#         results.sort(key=lambda x: x.get("processed_at", ""), reverse=True)
        
#         return results
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting results: {str(e)}")

# @app.get("/results/{session_id}")
# async def get_results_by_session(session_id: str):
#     """Get translated results for a specific session ID"""
#     try:
#         results = []
        
#         for result_file in RESULTS_DIR.glob(f"{session_id}_result_*.json"):
#             with open(result_file, "r", encoding="utf-8") as f:
#                 result_data = json.load(f)
#                 clean_result = {
#                     "session_id": result_data["session_id"],
#                     "document": result_data["document_name"],
#                     "translation": result_data["translated_text"],
#                     "processed_at": result_data["processed_time"]
#                 }
#                 results.append(clean_result)
        
#         if not results:
#             raise HTTPException(status_code=404, detail=f"No results found for session ID: {session_id}")
        
#         # Sort by processed time (newest first)
#         results.sort(key=lambda x: x.get("processed_at", ""), reverse=True)
        
#         return results
    
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting results for session {session_id}: {str(e)}")

# @app.get("/results/{session_id}/{document_name}")
# async def get_single_result_by_session(session_id: str, document_name: str):
#     """Get translated text for a specific document in a specific session"""
#     try:
#         # Try to find the result file for this document and session
#         for result_file in RESULTS_DIR.glob(f"{session_id}_result_*.json"):
#             with open(result_file, "r", encoding="utf-8") as f:
#                 result_data = json.load(f)
#                 if (result_data["session_id"] == session_id and 
#                     (result_data["document_name"] == document_name or 
#                      document_name in result_data["document_name"])):
#                     return {
#                         "session_id": result_data["session_id"],
#                         "document": result_data["document_name"],
#                         "translation": result_data["translated_text"],
#                         "processed_at": result_data["processed_time"]
#                     }
        
#         raise HTTPException(status_code=404, detail=f"Document '{document_name}' not found in session '{session_id}'")
    
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting result: {str(e)}")

# @app.get("/translations")
# async def get_all_translations():
#     """Get only the translated text strings from all sessions - Minimal response"""
#     try:
#         translations = []
        
#         # Check both new session-based files and legacy files
#         for result_file in RESULTS_DIR.glob("*result*.json"):
#             try:
#                 with open(result_file, "r", encoding="utf-8") as f:
#                     result_data = json.load(f)
#                     translations.append(result_data["translated_text"])
#             except (json.JSONDecodeError, KeyError) as e:
#                 print(f"Error reading result file {result_file}: {e}")
#                 continue
        
#         return translations
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting translations: {str(e)}")

# @app.get("/translations/{session_id}")
# async def get_translations_by_session(session_id: str):
#     """Get only the translated text strings for a specific session ID"""
#     try:
#         translations = []
        
#         for result_file in RESULTS_DIR.glob(f"{session_id}_result_*.json"):
#             with open(result_file, "r", encoding="utf-8") as f:
#                 result_data = json.load(f)
#                 translations.append(result_data["translated_text"])
        
#         if not translations:
#             raise HTTPException(status_code=404, detail=f"No translations found for session ID: {session_id}")
        
#         return translations
    
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting translations for session {session_id}: {str(e)}")

# @app.get("/queue")
# async def check_queue():
#     """Check how many files are waiting to be processed"""
#     try:
#         files = list(UPLOAD_DIR.glob("*"))
#         pending_files = [f.name for f in files if f.is_file()]
        
#         return {
#             "status": "success",
#             "pending_files": len(pending_files),
#             "files": pending_files
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error checking queue: {str(e)}")

# @app.get("/status")
# async def get_processing_status():
#     """Get current processing status"""
#     try:
#         pending_files = len(list(UPLOAD_DIR.glob("*")))
        
#         return {
#             "status": "processing" if processing_status["active"] else "idle",
#             "pending_files": pending_files,
#             "processed_count": processing_status["processed_count"]
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")

# @app.get("/debug/files")
# async def debug_files():
#     """Debug endpoint to check what files exist in the results directory"""
#     try:
#         upload_files = [f.name for f in UPLOAD_DIR.glob("*") if f.is_file()]
#         result_files = [f.name for f in RESULTS_DIR.glob("*") if f.is_file()]
        
#         return {
#             "upload_directory": str(UPLOAD_DIR),
#             "results_directory": str(RESULTS_DIR),
#             "upload_files": upload_files,
#             "result_files": result_files,
#             "processing_status": processing_status
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error getting debug info: {str(e)}")

# @app.delete("/results")
# async def clear_all_results():
#     """Clear all results from all sessions"""
#     try:
#         deleted_count = 0
        
#         for result_file in RESULTS_DIR.glob("session_*_result_*.json"):
#             result_file.unlink()
#             deleted_count += 1
        
#         processing_status["processed_count"] = 0
        
#         return {
#             "message": f"Cleared {deleted_count} results from all sessions"
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error clearing results: {str(e)}")

# @app.delete("/results/{session_id}")
# async def clear_session_results(session_id: str):
#     """Clear results for a specific session ID"""
#     try:
#         deleted_count = 0
        
#         for result_file in RESULTS_DIR.glob(f"{session_id}_result_*.json"):
#             result_file.unlink()
#             deleted_count += 1
        
#         if deleted_count == 0:
#             raise HTTPException(status_code=404, detail=f"No results found for session ID: {session_id}")
        
#         return {
#             "message": f"Cleared {deleted_count} results for session {session_id}"
#         }
    
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error clearing results for session {session_id}: {str(e)}")

# @app.get("/health")
# async def health_check():
#     """Health check endpoint"""
#     return {"status": "healthy", "service": "Translation Service", "port": 8000}

# if __name__ == "__main__":
#     import uvicorn
#     print("🚀 Starting Document Translation Service on port 8000...")
#     print("📤 Upload files: POST http://localhost:8000/upload")
#     print("📊 Get results by session: GET http://localhost:8000/results/{session_id}")
#     print("🔗 API Endpoints:")
#     print("   • POST /upload - Upload files (returns session_id)")
#     print("   • GET /results - All translations from all sessions")
#     print("   • GET /results/{session_id} - All translations for a session")
#     print("   • GET /results/{session_id}/{document_name} - Specific document in session")
#     print("   • GET /translations - Only translated text strings (all sessions)")
#     print("   • GET /translations/{session_id} - Only translated text for session")
#     print("   • DELETE /results - Clear all results")
#     print("   • DELETE /results/{session_id} - Clear session results")
#     print("   • GET /queue - Check processing queue")
#     print("   • GET /status - Processing status")
#     print("📖 API Docs: http://localhost:8000/docs")
#     print("\n" + "="*60)
#     uvicorn.run(app, host="0.0.0.0", port=8000)




# main.py - Simple Translation Service
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from typing_extensions import Annotated
from typing import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
import os
import shutil
from pathlib import Path
import uuid
import json
from datetime import datetime
import threading
import time

app = FastAPI(title="Document Translation Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
UPLOAD_DIR = Path("uploaded_files")
RESULTS_DIR = Path("results")
UPLOAD_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# Import your translation modules
try:
    from translator import translate
    from word_dictionary import correct_words
except ImportError:
    print("Warning: Translation modules not found. Using mock functions.")
    def translate(text, source, target):
        return f"[MOCK TRANSLATION] {text}"
    def correct_words(text, lang):
        return text

# State definition for LangGraph
class State(TypedDict):
    messages: Annotated[list, add_messages]
    path: list
    translated_text: list
    detected_language: str

def detect_language(text: str) -> str:
    """Simple language detection for Nepali vs Sinhala"""
    nepali_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
    sinhala_chars = sum(1 for char in text if '\u0D80' <= char <= '\u0DFF')
    
    if sinhala_chars > nepali_chars:
        return "si"  # Sinhala
    else:
        return "ne"  # Nepali (default)

def file_node(state: State) -> State:
    file_path = state['path'][-1]
    state['messages'].append({"role": "system", "content": f"Processing file: {file_path}"})
    return state

def png_node(state: State) -> State:
    try:
        from png_extractor import extract_text
        image_path = state['path'][-1]
        extracted_text = extract_text(image_path)
        state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
    except Exception as e:
        state['messages'].append({"role": "system", "content": f"Error extracting from PNG: {str(e)}"})
    return state

def pdf_node(state: State) -> State:
    try:
        from pdf_extractor import extract_nepali_sinhala_from_pdf
        pdf_path = state['path'][-1]
        extracted_text = extract_nepali_sinhala_from_pdf(pdf_path)
        state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
    except Exception as e:
        state['messages'].append({"role": "system", "content": f"Error extracting from PDF: {str(e)}"})
    return state

def unsupported_file_node(state: State) -> State:
    file_path = state['path'][-1]
    state['messages'].append({"role": "system", "content": f"Unsupported file type for: {file_path}"})
    return state

def language_detection_node(state: State) -> State:
    last_message = state["messages"][-1].content
    extracted_text = last_message.replace("Extracted text: ", "")
    
    detected_lang = detect_language(extracted_text)
    state["detected_language"] = detected_lang
    
    lang_name = "Sinhala" if detected_lang == "si" else "Nepali"
    state['messages'].append({"role": "system", "content": f"Detected language: {lang_name} ({detected_lang})"})
    return state

def ocr_correction_node(state: State) -> State:
    extracted_text = ""
    for msg in state["messages"]:
        if msg.content.startswith("Extracted text: "):
            extracted_text = msg.content.replace("Extracted text: ", "")
            break
    
    if not extracted_text:
        state['messages'].append({"role": "system", "content": "No extracted text found for OCR correction"})
        return state
    
    detected_lang = state["detected_language"]
    corrected_text = correct_words(extracted_text, detected_lang)
    state['messages'].append({"role": "system", "content": f"OCR corrected text: {corrected_text}"})
    return state

def translator_node(state: State) -> State:
    text_to_translate = ""
    for msg in state["messages"]:
        if msg.content.startswith("OCR corrected text: "):
            text_to_translate = msg.content.replace("OCR corrected text: ", "")
            break
    
    if not text_to_translate:
        for msg in state["messages"]:
            if msg.content.startswith("Extracted text: "):
                text_to_translate = msg.content.replace("Extracted text: ", "")
                break
    
    if not text_to_translate:
        state['messages'].append({"role": "system", "content": "No text found for translation"})
        return state
    
    source_lang = state["detected_language"]
    target_lang = "en"
    
    try:
        trans_text = translate(text_to_translate, source_lang, target_lang)
        state["translated_text"].append(trans_text)
        state['messages'].append({"role": "system", "content": f"Translated ({source_lang} -> {target_lang}): {trans_text}"})
    except Exception as e:
        error_msg = f"Translation error: {str(e)}"
        state['messages'].append({"role": "system", "content": error_msg})
        state["translated_text"].append(f"Error: {str(e)}")
    
    return state

def route_file_type(state: State) -> str:
    file_path = state['path'][-1].lower()
    if file_path.endswith('.png') or file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
        return "png_node"
    elif file_path.endswith('.pdf'):
        return "pdf_node"
    else:
        return "unsupported_file_node"

# Build the graph
graph_builder = StateGraph(State)
graph_builder.add_node("file_node", file_node)
graph_builder.add_node("png_node", png_node)
graph_builder.add_node("pdf_node", pdf_node)
graph_builder.add_node("unsupported_file_node", unsupported_file_node)
graph_builder.add_node("language_detection_node", language_detection_node)
graph_builder.add_node("ocr_correction_node", ocr_correction_node)
graph_builder.add_node("translator_node", translator_node)

graph_builder.add_edge(START, "file_node")
graph_builder.add_conditional_edges(
    "file_node",
    route_file_type,
    {
        "png_node": "png_node",
        "pdf_node": "pdf_node", 
        "unsupported_file_node": "unsupported_file_node"
    }
)

graph_builder.add_edge("png_node", "language_detection_node")
graph_builder.add_edge("pdf_node", "language_detection_node")
graph_builder.add_edge("language_detection_node", "ocr_correction_node")
graph_builder.add_edge("ocr_correction_node", "translator_node")
graph_builder.add_edge("translator_node", END)
graph_builder.add_edge("unsupported_file_node", END)

graph = graph_builder.compile()

# Global processing status
processing_status = {"active": False, "current_file": None, "processed_count": 0}

def process_files_background():
    """Background task to process uploaded files"""
    global processing_status
    
    while True:
        try:
            # Check for files to process
            files_to_process = list(UPLOAD_DIR.glob("*"))
            
            if files_to_process and not processing_status["active"]:
                processing_status["active"] = True
                
                for file_path in files_to_process:
                    if file_path.is_file():
                        processing_status["current_file"] = file_path.name
                        print(f"Processing: {file_path}")
                        
                        # Process file through the graph
                        initial_state = {
                            "messages": [], 
                            "path": [str(file_path)], 
                            "translated_text": [],
                            "detected_language": ""
                        }
                        
                        final_state = graph.invoke(initial_state)
                        
                        # Extract only the translated text
                        translated_text = final_state["translated_text"][-1] if final_state["translated_text"] else "Translation failed"
                        
                        # Save only the translated text result
                        result = {
                            "document_name": file_path.name,
                            "translated_text": translated_text,
                            "processed_time": datetime.now().isoformat()
                        }
                        
                        # Save to results directory
                        result_file = RESULTS_DIR / f"result_{file_path.stem}.json"
                        with open(result_file, "w", encoding="utf-8") as f:
                            json.dump(result, f, indent=2, ensure_ascii=False)
                        
                        # Remove processed file
                        file_path.unlink()
                        processing_status["processed_count"] += 1
                
                processing_status["active"] = False
                processing_status["current_file"] = None
            
            time.sleep(5)  # Check every 5 seconds
            
        except Exception as e:
            print(f"Error in background processing: {e}")
            processing_status["active"] = False
            processing_status["current_file"] = None
            time.sleep(10)

# Start background processing thread
processing_thread = threading.Thread(target=process_files_background, daemon=True)
processing_thread.start()

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload files and get translated text directly"""
    try:
        uploaded_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for file in files:
            # Validate file type
            file_extension = Path(file.filename).suffix.lower()
            if file_extension not in ['.pdf', '.png', '.jpg', '.jpeg']:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Unsupported file type: {file_extension}. Only PDF, PNG, JPG are allowed."
                )
            
            # Generate unique filename
            unique_filename = f"{timestamp}_{uuid.uuid4().hex[:8]}_{file.filename}"
            file_path = UPLOAD_DIR / unique_filename
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            uploaded_files.append({
                "original_name": file.filename,
                "stored_name": unique_filename,
                "file_type": file_extension
            })
        
        return {
            "status": "success",
            "message": f"Successfully uploaded {len(uploaded_files)} files. Processing started.",
            "files": uploaded_files,
            "note": "Use GET /results to get translated text"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")

@app.get("/results")
async def get_results():
    """Get all translated text results"""
    try:
        results = []
        
        for result_file in RESULTS_DIR.glob("result_*.json"):
            with open(result_file, "r", encoding="utf-8") as f:
                result_data = json.load(f)
                results.append({
                    "document": result_data["document_name"],
                    "translation": result_data["translated_text"],
                    "processed_at": result_data["processed_time"]
                })
        
        # Sort by processed time (newest first)
        results.sort(key=lambda x: x.get("processed_at", ""), reverse=True)
        
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting results: {str(e)}")

@app.get("/translations")
async def get_translations_only():
    """Get only the translated text strings"""
    try:
        translations = []
        
        for result_file in RESULTS_DIR.glob("result_*.json"):
            with open(result_file, "r", encoding="utf-8") as f:
                result_data = json.load(f)
                translations.append(result_data["translated_text"])
        
        return translations
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting translations: {str(e)}")

@app.get("/results/{document_name}")
async def get_single_result(document_name: str):
    """Get translated text for a specific document"""
    try:
        for result_file in RESULTS_DIR.glob("result_*.json"):
            with open(result_file, "r", encoding="utf-8") as f:
                result_data = json.load(f)
                if document_name in result_data["document_name"]:
                    return {
                        "document": result_data["document_name"],
                        "translation": result_data["translated_text"],
                        "processed_at": result_data["processed_time"]
                    }
        
        raise HTTPException(status_code=404, detail=f"Document '{document_name}' not found")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting result: {str(e)}")

@app.get("/status")
async def get_processing_status():
    """Get current processing status"""
    try:
        pending_files = len(list(UPLOAD_DIR.glob("*")))
        result_files = len(list(RESULTS_DIR.glob("result_*.json")))
        
        return {
            "status": "processing" if processing_status["active"] else "idle",
            "pending_files": pending_files,
            "completed_files": result_files,
            "processed_count": processing_status["processed_count"],
            "current_file": processing_status["current_file"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")

@app.delete("/results")
async def clear_results():
    """Clear all translation results"""
    try:
        deleted_count = 0
        
        for result_file in RESULTS_DIR.glob("result_*.json"):
            result_file.unlink()
            deleted_count += 1
        
        processing_status["processed_count"] = 0
        
        return {
            "message": f"Cleared {deleted_count} translation results"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing results: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Translation Service", "port": 8000}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Simple Document Translation Service on port 8000...")
    print("📤 Upload files: POST http://localhost:8000/upload")
    print("📊 Get results: GET http://localhost:8000/results")
    print("🔗 API Endpoints:")
    print("   • POST /upload - Upload files for translation")
    print("   • GET /results - All translations with metadata")
    print("   • GET /translations - Only translated text strings")
    print("   • GET /results/{document_name} - Specific document result")
    print("   • GET /status - Processing status")
    print("   • DELETE /results - Clear all results")
    print("📖 API Docs: http://localhost:8000/docs")
    print("\n" + "="*60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
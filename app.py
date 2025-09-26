# # # from typing_extensions import Annotated
# # # from typing import TypedDict
# # # from langgraph.graph.message import add_messages
# # # from langgraph.graph import StateGraph, START, END
# # # import os
# # # from pathlib import Path
# # # from translator import translate

# # # class State(TypedDict):
# # #     messages : Annotated[list, add_messages]
# # #     path : list
# # #     translated_text : list

# # # graph_builder = StateGraph(State)

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
# # #     """Handle unsupported file types"""
# # #     file_path = state['path'][-1]
# # #     state['messages'].append({"role": "system", "content": f"Unsupported file type for: {file_path}"})
# # #     return state

# # # def route_file_type(state: State) -> str:
# # #     """Route to appropriate node based on file extension"""
# # #     file_path = state['path'][-1].lower()
# # #     if file_path.endswith('.png'):
# # #         return "png_node"
# # #     elif file_path.endswith('.pdf'):
# # #         return "pdf_node"
# # #     else:
# # #         return "unsupported_file_node"

# # # def translator_node(state: State) -> State:
# # #     trans_text = translate(str(state["messages"][-1].content), "se", "en")
# # #     # print(trans_text)
# # #     state["translated_text"].append(trans_text)
# # #     return state


# # # graph_builder.add_node("file_node", file_node)
# # # graph_builder.add_node("png_node", png_node)
# # # graph_builder.add_node("pdf_node", pdf_node)
# # # graph_builder.add_node("unsupported_file_node", unsupported_file_node)
# # # graph_builder.add_node("translator_node",translator_node)

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
# # # graph_builder.add_edge("png_node", "translator_node")
# # # graph_builder.add_edge("pdf_node", "translator_node")
# # # graph_builder.add_edge("translator_node", END)

# # # graph = graph_builder.compile()

# # # test_data_path = Path("test_data")
# # # test_data_path.mkdir(exist_ok=True)

# # # for file in test_data_path.glob("*"):
# # #     if file.is_file():
# # #         print(f"Processing file: {file}")
# # #         final_state = graph.invoke({"messages": [], "path": [str(file)], "translated_text":[]})
# # #         print(final_state['messages'][-1].content)
# # #         print(final_state["translated_text"][-1])




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
# # #     # Find the extracted text message (not the language detection message)
# # #     extracted_text = ""
# # #     for msg in state["messages"]:
# # #         if msg.content.startswith("Extracted text: "):
# # #             extracted_text = msg.content.replace("Extracted text: ", "")
# # #             break
    
# # #     if not extracted_text:
# # #         state['messages'].append({"role": "system", "content": "No extracted text found for translation"})
# # #         return state
    
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
# # #         print(f"\nProcessing file: {file}")
        
# # #         initial_state = {
# # #             "messages": [], 
# # #             "path": [str(file)], 
# # #             "translated_text": [],
# # #             "detected_language": ""
# # #         }
        
# # #         final_state = graph.invoke(initial_state)
        
# # #         # Extract and display extracted text
# # #         extracted_text = ""
# # #         for msg in final_state['messages']:
# # #             if msg.content.startswith("Extracted text: "):
# # #                 extracted_text = msg.content.replace("Extracted text: ", "")
# # #                 break
        
# # #         print(f"Extracted Text: {extracted_text}")
# # #         print(f"Detected Language: {final_state.get('detected_language', 'Unknown')}")
        
# # #         if final_state["translated_text"]:
# # #             print(f"Translated Text: {final_state['translated_text'][-1]}")
        
# # #         print("-" * 50)


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


# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import JSONResponse
# from typing_extensions import Annotated
# from typing import TypedDict, Dict, Any
# from langgraph.graph.message import add_messages
# from langgraph.graph import StateGraph, START, END
# import os
# import tempfile
# from pathlib import Path
# import uvicorn
# from translator import translate
# from word_dictionary import correct_words

# app = FastAPI(title="File Translation Service with OCR Correction", version="2.0.0")

# class State(TypedDict):
#     messages: Annotated[list, add_messages]
#     path: list
#     translated_text: list
#     detected_language: str

# def detect_language(text: str) -> str:
#     """Simple language detection for Nepali vs Sinhala"""
#     # Nepali Unicode range: \u0900-\u097F (Devanagari)
#     nepali_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
    
#     # Sinhala Unicode range: \u0D80-\u0DFF  
#     sinhala_chars = sum(1 for char in text if '\u0D80' <= char <= '\u0DFF')
    
#     # Return language code based on which has more characters
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
#         state['messages'].append({"role": "system", "content": f"PNG extraction failed: {str(e)}"})
#     return state

# def pdf_node(state: State) -> State:
#     try:
#         from pdf_extractor import extract_nepali_sinhala_from_pdf
#         pdf_path = state['path'][-1]
#         extracted_text = extract_nepali_sinhala_from_pdf(pdf_path)
#         state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
#     except Exception as e:
#         state['messages'].append({"role": "system", "content": f"PDF extraction failed: {str(e)}"})
#     return state

# def unsupported_file_node(state: State) -> State:
#     file_path = state['path'][-1]
#     state['messages'].append({"role": "system", "content": f"Unsupported file type for: {file_path}"})
#     return state

# def language_detection_node(state: State) -> State:
#     """Detect language and store it in state"""
#     last_message = state["messages"][-1]
#     message_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
#     extracted_text = message_content.replace("Extracted text: ", "")
    
#     detected_lang = detect_language(extracted_text)
#     state["detected_language"] = detected_lang
    
#     lang_name = "Sinhala" if detected_lang == "si" else "Nepali"
#     state['messages'].append({"role": "system", "content": f"Detected language: {lang_name} ({detected_lang})"})
#     return state

# def ocr_correction_node(state: State) -> State:
#     """Apply word-based OCR corrections using dictionary lookup"""
#     # Find the extracted text
#     extracted_text = ""
#     for msg in state["messages"]:
#         content = msg.content if hasattr(msg, 'content') else str(msg)
#         if content.startswith("Extracted text: "):
#             extracted_text = content.replace("Extracted text: ", "")
#             break
    
#     if not extracted_text:
#         state['messages'].append({"role": "system", "content": "No extracted text found for OCR correction"})
#         return state
    
#     detected_lang = state["detected_language"]
    
#     # Apply dictionary-based word corrections
#     corrected_text = correct_words(extracted_text, detected_lang)
    
#     # Add corrected text to messages
#     state['messages'].append({"role": "system", "content": f"OCR corrected text: {corrected_text}"})
#     return state

# def translator_node(state: State) -> State:
#     """Translate using detected language and OCR corrected text"""
#     # Find the OCR corrected text (preferred) or fallback to extracted text
#     text_to_translate = ""
#     for msg in state["messages"]:
#         content = msg.content if hasattr(msg, 'content') else str(msg)
#         if content.startswith("OCR corrected text: "):
#             text_to_translate = content.replace("OCR corrected text: ", "")
#             break
    
#     # Fallback to extracted text if no corrected text found
#     if not text_to_translate:
#         for msg in state["messages"]:
#             content = msg.content if hasattr(msg, 'content') else str(msg)
#             if content.startswith("Extracted text: "):
#                 text_to_translate = content.replace("Extracted text: ", "")
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
#         state["translated_text"].append(f"Translation failed: {str(e)}")
#         state['messages'].append({"role": "system", "content": f"Translation failed: {str(e)}"})
    
#     return state

# def route_file_type(state: State) -> str:
#     file_path = state['path'][-1].lower()
#     if file_path.endswith('.png'):
#         return "png_node"
#     elif file_path.endswith('.pdf'):
#         return "pdf_node"
#     else:
#         return "unsupported_file_node"

# # Initialize the graph
# def create_translation_graph():
#     graph_builder = StateGraph(State)
    
#     # Add nodes
#     graph_builder.add_node("file_node", file_node)
#     graph_builder.add_node("png_node", png_node)
#     graph_builder.add_node("pdf_node", pdf_node)
#     graph_builder.add_node("unsupported_file_node", unsupported_file_node)
#     graph_builder.add_node("language_detection_node", language_detection_node)
#     graph_builder.add_node("ocr_correction_node", ocr_correction_node)
#     graph_builder.add_node("translator_node", translator_node)

#     # Add edges
#     graph_builder.add_edge(START, "file_node")
#     graph_builder.add_conditional_edges(
#         "file_node",
#         route_file_type,
#         {
#             "png_node": "png_node",
#             "pdf_node": "pdf_node", 
#             "unsupported_file_node": "unsupported_file_node"
#         }
#     )

#     # Both extraction nodes go to language detection
#     graph_builder.add_edge("png_node", "language_detection_node")
#     graph_builder.add_edge("pdf_node", "language_detection_node")

#     # Language detection goes to OCR correction
#     graph_builder.add_edge("language_detection_node", "ocr_correction_node")

#     # OCR correction goes to translation
#     graph_builder.add_edge("ocr_correction_node", "translator_node")

#     # Translation goes to end
#     graph_builder.add_edge("translator_node", END)

#     # Unsupported files skip everything
#     graph_builder.add_edge("unsupported_file_node", END)

#     return graph_builder.compile()

# # Create the graph instance
# translation_graph = create_translation_graph()

# @app.post("/translate", response_model=Dict[str, Any])
# async def translate_files(files: list[UploadFile] = File(...)):
#     """
#     Upload one or multiple files (PNG or PDF) to extract text, detect language, apply OCR corrections, and translate to English.
    
#     Supported file types:
#     - PNG images (with text)
#     - PDF files containing Nepali/Sinhala text
    
#     Process flow:
#     1. Extract text from file
#     2. Detect language (Nepali/Sinhala)
#     3. Apply OCR corrections using dictionary
#     4. Translate to English
#     """
    
#     if not files:
#         raise HTTPException(status_code=400, detail="No files provided")
    
#     results = []
    
#     for file in files:
#         try:
#             # Validate file
#             if not file.filename:
#                 results.append({
#                     "filename": "unknown",
#                     "status": "error",
#                     "error": "No filename provided"
#                 })
#                 continue
            
#             file_extension = Path(file.filename).suffix.lower()
#             if file_extension not in ['.png', '.pdf']:
#                 results.append({
#                     "filename": file.filename,
#                     "status": "error", 
#                     "error": f"Unsupported file type: {file_extension}. Supported types: .png, .pdf"
#                 })
#                 continue
            
#             # Create temporary file
#             temp_dir = tempfile.mkdtemp()
#             temp_file_path = Path(temp_dir) / file.filename
            
#             try:
#                 # Save uploaded file
#                 with open(temp_file_path, "wb") as buffer:
#                     content = await file.read()
#                     buffer.write(content)
                
#                 # Process through the graph
#                 initial_state = {
#                     "messages": [], 
#                     "path": [str(temp_file_path)], 
#                     "translated_text": [],
#                     "detected_language": ""
#                 }
                
#                 final_state = translation_graph.invoke(initial_state)
                
#                 # Extract results from messages
#                 extracted_text = ""
#                 corrected_text = ""
#                 detected_language = final_state.get("detected_language", "Unknown")
                
#                 for message in final_state["messages"]:
#                     # Handle both dict and object message formats
#                     if hasattr(message, 'content'):
#                         content = message.content
#                     elif isinstance(message, dict) and 'content' in message:
#                         content = message['content']
#                     else:
#                         content = str(message)
                    
#                     if content.startswith("Extracted text: "):
#                         extracted_text = content.replace("Extracted text: ", "")
#                     elif content.startswith("OCR corrected text: "):
#                         corrected_text = content.replace("OCR corrected text: ", "")
                
#                 translated_text = final_state["translated_text"][-1] if final_state["translated_text"] else "No translation available"
                
#                 results.append({
#                     "filename": file.filename,
#                     "file_type": file_extension,
#                     "extracted_text": extracted_text,
#                     "ocr_corrected_text": corrected_text,
#                     "detected_language": detected_language,
#                     "translated_text": translated_text,
#                     "processing_messages": [
#                         msg.content if hasattr(msg, 'content') else (msg.get('content', str(msg)) if isinstance(msg, dict) else str(msg)) 
#                         for msg in final_state["messages"]
#                     ],
#                     "status": "success"
#                 })
                
#             finally:
#                 # Cleanup temporary file
#                 try:
#                     if temp_file_path.exists():
#                         temp_file_path.unlink()
#                     Path(temp_dir).rmdir()
#                 except:
#                     pass
                    
#         except Exception as e:
#             results.append({
#                 "filename": file.filename if file.filename else "unknown",
#                 "status": "error",
#                 "error": str(e)
#             })
    
#     # Return single result if only one file, otherwise return array
#     if len(results) == 1:
#         return results[0]
#     else:
#         return {"results": results, "total_processed": len(results)}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing_extensions import Annotated
from typing import TypedDict, Dict, Any
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
import os
import tempfile
from pathlib import Path
import uvicorn
from translator import translate
from word_dictionary import correct_words

app = FastAPI(title="File Translation Service with OCR Correction", version="2.1.0")

# Pydantic model for text input
class TextInput(BaseModel):
    text: str

class State(TypedDict):
    messages: Annotated[list, add_messages]
    path: list
    translated_text: list
    detected_language: str

def detect_language(text: str) -> str:
    """Simple language detection for Nepali vs Sinhala"""
    # Nepali Unicode range: \u0900-\u097F (Devanagari)
    nepali_chars = sum(1 for char in text if '\u0900' <= char <= '\u097F')
    
    # Sinhala Unicode range: \u0D80-\u0DFF  
    sinhala_chars = sum(1 for char in text if '\u0D80' <= char <= '\u0DFF')
    
    # Return language code based on which has more characters
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
        state['messages'].append({"role": "system", "content": f"PNG extraction failed: {str(e)}"})
    return state

def pdf_node(state: State) -> State:
    try:
        from pdf_extractor import extract_nepali_sinhala_from_pdf
        pdf_path = state['path'][-1]
        extracted_text = extract_nepali_sinhala_from_pdf(pdf_path)
        state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
    except Exception as e:
        state['messages'].append({"role": "system", "content": f"PDF extraction failed: {str(e)}"})
    return state

def text_input_node(state: State) -> State:
    """Node for processing direct text input"""
    input_text = state['path'][-1]  # For text input, we store text in path
    state['messages'].append({"role": "system", "content": f"Processing text input: {input_text[:100]}..."})
    state['messages'].append({"role": "system", "content": f"Extracted text: {input_text}"})
    return state

def unsupported_file_node(state: State) -> State:
    file_path = state['path'][-1]
    state['messages'].append({"role": "system", "content": f"Unsupported file type for: {file_path}"})
    return state

def language_detection_node(state: State) -> State:
    """Detect language and store it in state"""
    last_message = state["messages"][-1]
    message_content = last_message.content if hasattr(last_message, 'content') else str(last_message)
    extracted_text = message_content.replace("Extracted text: ", "")
    
    detected_lang = detect_language(extracted_text)
    state["detected_language"] = detected_lang
    
    lang_name = "Sinhala" if detected_lang == "si" else "Nepali"
    state['messages'].append({"role": "system", "content": f"Detected language: {lang_name} ({detected_lang})"})
    return state

def ocr_correction_node(state: State) -> State:
    """Apply word-based OCR corrections using dictionary lookup"""
    # Find the extracted text
    extracted_text = ""
    for msg in state["messages"]:
        content = msg.content if hasattr(msg, 'content') else str(msg)
        if content.startswith("Extracted text: "):
            extracted_text = content.replace("Extracted text: ", "")
            break
    
    if not extracted_text:
        state['messages'].append({"role": "system", "content": "No extracted text found for OCR correction"})
        return state
    
    detected_lang = state["detected_language"]
    
    # Apply dictionary-based word corrections
    corrected_text = correct_words(extracted_text, detected_lang)
    
    # Add corrected text to messages
    state['messages'].append({"role": "system", "content": f"OCR corrected text: {corrected_text}"})
    return state

def translator_node(state: State) -> State:
    """Translate using detected language and OCR corrected text"""
    # Find the OCR corrected text (preferred) or fallback to extracted text
    text_to_translate = ""
    for msg in state["messages"]:
        content = msg.content if hasattr(msg, 'content') else str(msg)
        if content.startswith("OCR corrected text: "):
            text_to_translate = content.replace("OCR corrected text: ", "")
            break
    
    # Fallback to extracted text if no corrected text found
    if not text_to_translate:
        for msg in state["messages"]:
            content = msg.content if hasattr(msg, 'content') else str(msg)
            if content.startswith("Extracted text: "):
                text_to_translate = content.replace("Extracted text: ", "")
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
        state["translated_text"].append(f"Translation failed: {str(e)}")
        state['messages'].append({"role": "system", "content": f"Translation failed: {str(e)}"})
    
    return state

def route_file_type(state: State) -> str:
    file_path = state['path'][-1].lower()
    if file_path.endswith('.png'):
        return "png_node"
    elif file_path.endswith('.pdf'):
        return "pdf_node"
    else:
        return "unsupported_file_node"

def route_input_type(state: State) -> str:
    """Route based on whether it's file processing or direct text input"""
    # Check if this is a text input (no file extension)
    input_data = state['path'][-1]
    if not any(input_data.lower().endswith(ext) for ext in ['.png', '.pdf']):
        return "text_input_node"
    else:
        return "file_node"

# Initialize the file processing graph
def create_translation_graph():
    graph_builder = StateGraph(State)
    
    # Add nodes
    graph_builder.add_node("file_node", file_node)
    graph_builder.add_node("png_node", png_node)
    graph_builder.add_node("pdf_node", pdf_node)
    graph_builder.add_node("text_input_node", text_input_node)
    graph_builder.add_node("unsupported_file_node", unsupported_file_node)
    graph_builder.add_node("language_detection_node", language_detection_node)
    graph_builder.add_node("ocr_correction_node", ocr_correction_node)
    graph_builder.add_node("translator_node", translator_node)

    # Add edges from START with routing
    graph_builder.add_conditional_edges(
        START,
        route_input_type,
        {
            "file_node": "file_node",
            "text_input_node": "text_input_node"
        }
    )
    
    # File node routing
    graph_builder.add_conditional_edges(
        "file_node",
        route_file_type,
        {
            "png_node": "png_node",
            "pdf_node": "pdf_node", 
            "unsupported_file_node": "unsupported_file_node"
        }
    )

    # All extraction nodes (including text input) go to language detection
    graph_builder.add_edge("png_node", "language_detection_node")
    graph_builder.add_edge("pdf_node", "language_detection_node")
    graph_builder.add_edge("text_input_node", "language_detection_node")

    # Language detection goes to OCR correction
    graph_builder.add_edge("language_detection_node", "ocr_correction_node")

    # OCR correction goes to translation
    graph_builder.add_edge("ocr_correction_node", "translator_node")

    # Translation goes to end
    graph_builder.add_edge("translator_node", END)

    # Unsupported files skip everything
    graph_builder.add_edge("unsupported_file_node", END)

    return graph_builder.compile()

# Create the graph instance
translation_graph = create_translation_graph()

@app.post("/translate", response_model=Dict[str, Any])
async def translate_files(files: list[UploadFile] = File(...)):
    """
    Upload one or multiple files (PNG or PDF) to extract text, detect language, apply OCR corrections, and translate to English.
    
    Supported file types:
    - PNG images (with text)
    - PDF files containing Nepali/Sinhala text
    
    Process flow:
    1. Extract text from file
    2. Detect language (Nepali/Sinhala)
    3. Apply OCR corrections using dictionary
    4. Translate to English
    """
    
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    results = []
    
    for file in files:
        try:
            # Validate file
            if not file.filename:
                results.append({
                    "filename": "unknown",
                    "status": "error",
                    "error": "No filename provided"
                })
                continue
            
            file_extension = Path(file.filename).suffix.lower()
            if file_extension not in ['.png', '.pdf']:
                results.append({
                    "filename": file.filename,
                    "status": "error", 
                    "error": f"Unsupported file type: {file_extension}. Supported types: .png, .pdf"
                })
                continue
            
            # Create temporary file
            temp_dir = tempfile.mkdtemp()
            temp_file_path = Path(temp_dir) / file.filename
            
            try:
                # Save uploaded file
                with open(temp_file_path, "wb") as buffer:
                    content = await file.read()
                    buffer.write(content)
                
                # Process through the graph
                initial_state = {
                    "messages": [], 
                    "path": [str(temp_file_path)], 
                    "translated_text": [],
                    "detected_language": ""
                }
                
                final_state = translation_graph.invoke(initial_state)
                
                # Extract results from messages
                extracted_text = ""
                corrected_text = ""
                detected_language = final_state.get("detected_language", "Unknown")
                
                for message in final_state["messages"]:
                    # Handle both dict and object message formats
                    if hasattr(message, 'content'):
                        content = message.content
                    elif isinstance(message, dict) and 'content' in message:
                        content = message['content']
                    else:
                        content = str(message)
                    
                    if content.startswith("Extracted text: "):
                        extracted_text = content.replace("Extracted text: ", "")
                    elif content.startswith("OCR corrected text: "):
                        corrected_text = content.replace("OCR corrected text: ", "")
                
                translated_text = final_state["translated_text"][-1] if final_state["translated_text"] else "No translation available"
                
                results.append({
                    "filename": file.filename,
                    "file_type": file_extension,
                    "extracted_text": extracted_text,
                    "ocr_corrected_text": corrected_text,
                    "detected_language": detected_language,
                    "translated_text": translated_text,
                    "processing_messages": [
                        msg.content if hasattr(msg, 'content') else (msg.get('content', str(msg)) if isinstance(msg, dict) else str(msg)) 
                        for msg in final_state["messages"]
                    ],
                    "status": "success"
                })
                
            finally:
                # Cleanup temporary file
                try:
                    if temp_file_path.exists():
                        temp_file_path.unlink()
                    Path(temp_dir).rmdir()
                except:
                    pass
                    
        except Exception as e:
            results.append({
                "filename": file.filename if file.filename else "unknown",
                "status": "error",
                "error": str(e)
            })
    
    # Return single result if only one file, otherwise return array
    if len(results) == 1:
        return results[0]
    else:
        return {"results": results, "total_processed": len(results)}

@app.post("/translate-text", response_model=str)
async def translate_text(input_data: TextInput):
    """
    Translate Nepali or Sinhala text directly to English.
    
    Process flow:
    1. Detect language (Nepali/Sinhala)
    2. Apply OCR corrections using dictionary
    3. Translate to English
    
    Args:
        input_data: TextInput object containing the text to translate
    
    Returns:
        str: Translated English text
    """
    
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="No text provided")
    
    try:
        # Process through the graph
        initial_state = {
            "messages": [], 
            "path": [input_data.text],  # Store text in path for processing
            "translated_text": [],
            "detected_language": ""
        }
        
        final_state = translation_graph.invoke(initial_state)
        
        # Extract translated text
        translated_text = final_state["translated_text"][-1] if final_state["translated_text"] else "No translation available"
        
        # Check if translation failed
        if translated_text.startswith("Translation failed:"):
            raise HTTPException(status_code=500, detail=translated_text)
        
        return translated_text
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation processing failed: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "File Translation Service with OCR Correction",
        "version": "2.1.0",
        "endpoints": {
            "/translate": "Upload files (PNG/PDF) for translation",
            "/translate-text": "Send text directly for translation",
            "/docs": "API documentation"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
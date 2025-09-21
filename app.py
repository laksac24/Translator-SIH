from typing_extensions import Annotated
from typing import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    messages : Annotated[list, add_messages]
    path : list

graph_builder = StateGraph(State)

def png_node(state: State) -> State:
    from png_extractor import extract_text
    image_path = state['path'][-1]
    extracted_text = extract_text(image_path)
    state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
    return state

def pdf_node(state: State) -> State:
    from pdf_extractor import extract_nepali_sinhala_from_pdf
    pdf_path = state['path'][-1]
    extracted_text = extract_nepali_sinhala_from_pdf(pdf_path)
    state['messages'].append({"role": "system", "content": f"Extracted text: {extracted_text}"})
    return state

graph_builder.add_node("png_node", png_node)
graph_builder.add_node("pdf_node", pdf_node)

graph_builder.add_edge(START, "pdf_node")
graph_builder.add_edge("pdf_node", END)

graph = graph_builder.compile()
img_path = "test_data/sample6.pdf"
final_state = graph.invoke({"messages": [], "path": [img_path]})

print(final_state['messages'][-1].content)
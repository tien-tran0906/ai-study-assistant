from fastapi import FastAPI
from typing import Any, Dict, List
from pydantic import BaseModel
from langchain.chains import LLMChain
from langchain_community.llms import Ollama
from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from google_api import get_credentials, get_doc_id, doc_content

app = FastAPI()


class UserInput(BaseModel):
    fileName: str
    context: str

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])


@app.post('/')
async def generate_response(input: UserInput):
    system_prompt = """You are an expert in creating high-quality multiple-choice quesitons and answer pairs 
    based on a given context. Based on the given context (e.g a passage, a paragraph, or a set of information), you should:
    1. Come up with thought-provoking multiple-choice questions that assess the reader's understanding of the context. 
    2. The questions should be clear and concise.
    3. The answer options should be logical and relevant to the context.

    The multiple-choice questions and answer pairs should follow this format: 
    
    1) Question 
    A) Option 1
    B) Option 2 
    C) Option 3 

    Answer: A) Option 1 

    Continue with additional questions and answer pairs as needed.

    MAKE SURE TO INCLUDE THE FULL CORRECT ANSWER AT THE END, NO EXPLANATION NEEDED:
    """
    instruction = f""" Based on the provided context, create {int(len(input.context.split(' '))/27.75)} multiple-choice questions and answer pairs"""

    llm = Ollama(model="mistral:instruct", callbacks=callback_manager)

    result = llm.invoke(f'{system_prompt} ### Context: {input.context} ### Instructions: {instruction} ')
    print(result)

    file_name = input.fileName
    creds = get_credentials()
    doc_id = get_doc_id(file_name, creds)
    success = doc_content(result, doc_id, creds)
    if not success:
        return {"error": "Failed to insert content into the document."}
    
    doc_url = f"https://docs.google.com/document/d/{doc_id}"
    response = {'doc_url': doc_url}
    
    return response

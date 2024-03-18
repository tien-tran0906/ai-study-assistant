from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chains import LLMChain
from model_setup import setup_llm_model
from google_api import get_credentials, get_doc_id, doc_content

app = FastAPI()


class UserInput(BaseModel):
    fileName: str
    context: str


@app.post('/')
async def generate_response(input: UserInput):
    instruction = f""" Based on the provided context, create {int(len(input.context.split(' '))/27.75)} multiple choice questions and answer pairs, following this format: 
    
    1) Question 
    A) Option 1
    B) Option 2 
    C) Option 3 

    Answer: A) Option 1 
    
    MAKE SURE TO INCLUDE THE FULL CORRECT ANSWER AT THE END, NO EXPLANATION NEEDED: """
    prompt, llm = setup_llm_model()
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    result = llm_chain.run(f"{instruction} {input.context}")

    file_name = input.fileName
    creds = get_credentials()
    doc_id = get_doc_id(file_name, creds)
    success = doc_content(result, doc_id, creds)
    if not success:
        return {"error": "Failed to insert content into the document."}
    
    doc_url = f"https://docs.google.com/document/d/{doc_id}"
    response = {'doc_url': doc_url}
    
    return response

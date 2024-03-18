import os
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google_api_settings import load_config, get_credentials, get_doc_id, doc_content

app = FastAPI()

class UserInput(BaseModel):
    fileName: str
    context: str


template = """Question: {question}

Answer: 
"""

prompt = PromptTemplate(template=template, input_variables=["question"])
# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])


n_gpu_layers = 0
n_batch = 10    # only affect when the model is ingesting the prompt. 
n_ctx = 32768   # max number of tokens that the model can account for when processing a response, including prompt, and the response itself
# n_keep        # https://github.com/ggerganov/llama.cpp/discussions/559
# repeat_last_n
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path= os.path.join(current_dir,"mistral-7b-instruct-v0.2.Q5_K_M.gguf")

llm = LlamaCpp(
    model_path=model_path,
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    n_ctx = n_ctx,
    callback_manager=callback_manager,
    verbose=True,
    max_tokens=None,
    temperature=0.1,
    top_p = 0.1,

)

@app.post('/')
async def generate_response(input: UserInput):
    instruction =  f"""
    Based on the provided context, create {int(len(input.context.split(' '))/27.75)} multiple choice questions and answer pairs, following this format: 
    1) Question
    A) Option 1
    B) Option 2
    C) Option 3

    Answer: A) Option 1

    MAKE SURE TO INCLUDE THE FULL CORRECT ANSWER AT THE END, NO EXPLANATION NEEDED:
    """
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    question = f"{instruction} {input.context}"
    result = llm_chain.run(question)
    fileName = input.fileName  # get fileName from UI
    creds = get_credentials()
    id = get_doc_id(fileName, creds)
    doc_content(result, id, creds)
    doc_url = f"https://docs.google.com/document/d/{id}"
    response = {
        'doc_url': doc_url
    }

    return response
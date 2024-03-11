from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class UserInput(BaseModel):
    context: str
    instruction: str = """Based on the provided context, create 4 multiple choice questions and answer pairs. First, create 2 multiple choice scenario-based question and answer pairs, then create another 2 multiple choice term and definition pairs. There should be 4 multiple choice questions in total, MAKE SURE TO INCLUDE THE CORRECT ANSWER AT THE END, NO EXPLANATION NEEDED:"""


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
model_path="mistral-7b-instruct-v0.2.Q5_K_M.gguf"

llm = LlamaCpp(
    model_path="mistral-7b-instruct-v0.2.Q5_K_M.gguf",
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    n_ctx = n_ctx,
    callback_manager=callback_manager,
    verbose=True,
    max_tokens=None,
    temperature=0.1,
    top_p = 0.1,

)

@app.post('/generate')
async def generate_response(input: UserInput):
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    question = f"{input.instruction} {input.context}"
    result = llm_chain.run(question)
    response = {
        'response': result
    }
    return response
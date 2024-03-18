import os
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.prompts import PromptTemplate


def setup_llm_model():
    template = """Question: {question}

    Answer: 
    """

    prompt = PromptTemplate(template=template, input_variables=["question"])

    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    n_gpu_layers = 0
    n_batch = 10
    n_ctx = 32768
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "mistral-7b-instruct-v0.2.Q5_K_M.gguf")

    llm = LlamaCpp(
        model_path=model_path,
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        n_ctx=n_ctx,
        callback_manager=callback_manager,
        verbose=True,
        max_tokens=None,
        temperature=0.1,
        top_p=0.1,
    )
    return prompt, llm

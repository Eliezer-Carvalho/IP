#https://llama-cpp.com/

from llama_cpp import Llama

slm = Llama (
    model_path = r"C:\Users\eliez\Desktop\ip\Modelos\x.gguf")


text = slm (
    "Fala-me sobre a Infraestruturas de Portugal!",
    max_tokens = 1000
)

print (text["choices"][0]["text"])


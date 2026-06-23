from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig


MODELO_PATH = r"C:\Users\Admin\Desktop\models\Mistral-7B-Instruct-v0.3"

quantization = BitsAndBytesConfig (
    load_in_4bit = True,  #Quantização
    bnb_4bit_quant_type = 'nf4',  #Tipo de Quantização
    bnb_4bit_use_double_quant = True, #Double Quantization
    bnb_4bit_compute_dtype = 'float16', #Tipo de precisão usada nos cálculos durante a inferência.
)

modelo = AutoModelForCausalLM.from_pretrained (MODELO_PATH, device_map = 'auto', quantization_config = quantization)

tokenizer = AutoTokenizer.from_pretrained (MODELO_PATH)

modelo.save_pretrained (r"C:\Users\Admin\Desktop\models\Mistral-7B-Instruct-v0.3-Q4")
tokenizer.save_pretrained (r"C:\Users\Admin\Desktop\models\Mistral-7B-Instruct-v0.3-Q4")
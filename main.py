from transformers import AutoTokenizer, AutoModelForCausalLM   

#Esta class serve como implementação de um modelo SLM de 4 Biliões de Parâmetros hospedado localmente
#O modelo tem rodado na CPU, o que não é ideal mas tudo bem
#O modelo é o Qwen 3-4B -> https://huggingface.co/Qwen/Qwen3-4B-Base
#O código foi comentado para melhor compreensão global

#Problemas a solucionar -> O modelo carrega os dados sempre que é chamado, o que não é ideal. (SOLUCIONADO! VIA GOOGLE COLAB)
#Aplicar Quantização para diminuir o tamanho do modelo, ajuda na VRAM


class IP_MODEL ():

    def __init__(self, MODELO_PATH, PROMPT):
        
        self.tokenizer = AutoTokenizer.from_pretrained (MODELO_PATH) #Tokenizer
        self.MODELO = AutoModelForCausalLM.from_pretrained (MODELO_PATH, device_map = "cpu") #Modelo em si #device_map é onde o modelo roda

        self.PROMPT = PROMPT #Self instância do prompt

    def forward(self):


        inputs = self.tokenizer (self.PROMPT, return_tensors = 'pt') #Tokenização do Input do Utilizador #return_tensors = 'pt' usa py torch tensors (padrão da indústria)
        probs = self.MODELO.generate (**inputs, max_new_tokens = 100) #Geração com max_new_tokens
        text = self.tokenizer.decode (probs[0]) #Decode token a token por isso o [0]
        return text


teste = IP_MODEL (r"C:\Users\eliez\Desktop\ip\Modelos\Qwen3-4 Base", "Olá, fala-me sobre as Infraestruturas de Portugal")
print (teste.forward())



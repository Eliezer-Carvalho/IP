from pynvml import *
import psutil
import torch
import time


class Statistics_Monitor:

    def __init__ (self):

        nvmlInit()
        self.Handle = nvmlDeviceGetHandleByIndex (0)

        self.Energy_Wh = 0 # Potência Consumida ao longo do tempo, começa a 0
        self.time = time.time()


    def GPU_NAME (self):

        NAME = nvmlDeviceGetName (self.Handle)
        return f"<h3>GPU: {NAME}</h3>"


    def GPU_MEMORY (self):

        MEMORY = nvmlDeviceGetMemoryInfo (self.Handle)
        MEMORY_USED = MEMORY.used / 1024**3
        MEMORY_TOTAL = MEMORY.total / 1024**3
        return f"<h3>Memória Total: {MEMORY_TOTAL:.2f} GB</h3>\n<h3>Memória Usada: {MEMORY_USED:.2f} GB</h3>"


    def GPU_UTILIZATION (self):

        UTIL = nvmlDeviceGetUtilizationRates (self.Handle)
        return f"<h3>% da Utilização da Memória: {UTIL.memory}%</h3>\n<h3>% da Utilização da GPU: {UTIL.gpu}%</h3>"


    def GPU_TEMP (self):

        TEMP = nvmlDeviceGetTemperature (self.Handle, NVML_TEMPERATURE_GPU)
        return f"<h3>Temperatura da GPU: {TEMP}°C</h3>"


    def GPU_POWER (self):

        ENERGIA = nvmlDeviceGetPowerUsage (self.Handle) / 1000 # Conversão para Watts
        return f"<h3>Potência Consumida pela GPU: {ENERGIA:.2f} W</h3>"


    def GPU_ENERGY (self):

        tempo_fim = time.time()
        decorrido = tempo_fim - self.time

        ENERGIA = nvmlDeviceGetPowerUsage (self.Handle) / 1000
        
        self.Energy_Wh += ENERGIA * decorrido / 3600 

        self.time = tempo_fim # Porque temos que ir atualizando o intervalo de tempo, se não calcula sempre no mesmo
        ########################################################

        valor = self.Energy_Wh / 1000 * 0.20 #Conversão para kWh * valor médio da energia em pt    

        return f"<h3>Energia: {self.Energy_Wh:.4f} Wh</h3>\n<h3>Valor em Energia Gasto: {valor:.10f}€</h3>"

#############################################################################################################################
    def CPU_NAME (self):

        return f"<h3>CPU: Intel(R) Xeon(R) W-2255 CPU @ 3.70GHz</h3>"

    def CPU_MEM_TOTAL (self):

        MEM_TOTAL = psutil.virtual_memory().total / 1024**3

        return f"<h3>Memória Total: {MEM_TOTAL:.2f} GB</h3>"

    def CPU_MEM_USADA (self):

        MEM_USADA = psutil.virtual_memory().used / 1024**3

        return f"<h3>Memória Usada: {MEM_USADA:.2f} GB</h3>"

    def CPU_UTIL (self):

        CPU_UTIL = psutil.cpu_percent (interval = None)

        return f"<h3>% da Utilização da CPU: {CPU_UTIL}</h3>"



"""
monitor = Statistics_Monitor()

x = monitor.GPU_NAME()

print (x)

y = monitor.Close_Handle()
"""















"""
def GPU_NAME ():

    GPU = torch.cuda.get_device_name()

    return f"<h3>GPU: {GPU}</h3>"


def GPU_MEM_ALLOCADA ():

    MEM_GPU_ALOCADA = torch.cuda.memory_allocated() / 1024**3

    return f"<h3>Memória Alocada: {MEM_GPU_ALOCADA:.2f} GB</h3>"


def GPU_MEM_RESERVADA ():

    MEM_GPU_RESERVADA = torch.cuda.memory_reserved() / 1024**3

    return f"<h3>Memória Reservada: {MEM_GPU_RESERVADA:.2f} GB</h3>"
#####################################################################################################################################################################


def CPU_NAME ():

    return f"<h3>CPU: Intel(R) Xeon(R) W-2255 CPU @ 3.70GHz</h3>"


def CPU_MEM_TOTAL ():

    MEM_TOTAL = psutil.virtual_memory().total / 1024**3

    return f"<h3>Memória Total: {MEM_TOTAL:.2f} GB"

def CPU_MEM_USADA ():

    MEM_USADA = psutil.virtual_memory().used / 1024**3

    return f"<h3>Memória Usada: {MEM_USADA:.2f} GB"
#####################################################################################################################################################################
"""



import torch
import psutil

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




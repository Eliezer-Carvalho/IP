import torch


def GPU_NAME ():

    GPU = torch.cuda.get_device_name()

    return f"<h3>GPU: {GPU}</h3>"
#######################################################

def GPU_MEM_ALLOCADA ():

    MEM_GPU_ALOCADA = torch.cuda.memory_allocated() / 1024**3

    return f"<h3>Memória Alocada: {MEM_GPU_ALOCADA:.2f} GB</h3>"
#######################################################

def GPU_MEM_RESERVADA ():

    MEM_GPU_RESERVADA = torch.cuda.memory_reserved() / 1024**3

    return f"<h3>Memória Reservada: {MEM_GPU_RESERVADA:.2f} GB</h3>"
#######################################################

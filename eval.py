import lm_eval

#https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/python-api.md

#Muito lento --> testar com diferentes params 



teste = lm_eval.simple_evaluate (
    model = "hf",
    model_args = r"pretrained=C:\Users\Admin\Desktop\models\Qwen3-4B-Base\GPUQ4",
    tasks = ["mmlu", "mmlu_redux_generative", "mmlu_pro"],
    device = "cuda",
    batch_size = 2, 
    limit = 100,
    gen_kwargs = {"max_new_tokens": 256}
)

print(teste["results"])
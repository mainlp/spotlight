import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import os

os.environ["HF_HOME"] = "anonymized"
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

def initialize_llama_2(model_name, device=None):
    if device is None:
        device = 0 if torch.cuda.is_available() else -1

    tokenizer = AutoTokenizer.from_pretrained(model_name, token=os.getenv("HF_TOKEN"), cache_dir="anonymized")
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, token=os.getenv("HF_TOKEN"), cache_dir="anonymized")
    generator = pipeline('text-generation', model=model, tokenizer=tokenizer, device=device)

    return generator


def initialize_llama_3(model_name):

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True
    )

    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        token=os.getenv("HF_TOKEN"),
        cache_dir="anonymized"
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        token=os.getenv("HF_TOKEN"),
        cache_dir="anonymized"
    )

    generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

    return generator


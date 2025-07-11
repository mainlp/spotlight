import json
from llm_functions import initialize_llama_2, initialize_llama_3
from transformers import set_seed
from tqdm import tqdm


def load_config(config_file):
    print("Loading configuration file...")
    with open(config_file, 'r') as f:
        config = json.load(f)
    print("Configuration file loaded.")
    return config


def run_experiment(config):
    model_name = config["model_name"]
    print(f"Initializing model: {model_name}...")

    if "llama_2" in model_name:
        generator = initialize_llama_2(model_name)
        use_max_new_tokens = False
    else:
        generator = initialize_llama_3(model_name)
        use_max_new_tokens = True

    print(f"Model {model_name} initialized.")

    set_seed(config["seed"])
    print("Random seed set.")

    output_data = {}

    print("Starting experiment...")

    for i, prompt in enumerate(tqdm(config["prompt"], desc="Processing prompts")):
        prompt_key = f"prompt_{i + 1}"
        output_data[prompt_key] = {
            "prompt": prompt,
            "outputs": []
        }

        for _ in tqdm(range(config["repetition"]), desc="Generating outputs"):

            gen_kwargs = {
                "do_sample": True,
                "top_p": config["top_p"],
                "temperature": config["temperature"],
                "top_k": config["top_k"],
                "num_return_sequences": 1,
                "eos_token_id": generator.tokenizer.eos_token_id
            }

            if use_max_new_tokens:
                gen_kwargs["max_new_tokens"] = config.get("max_new_tokens")

            sequences = generator(prompt, **gen_kwargs)

            for seq in sequences:
                generated_text = seq['generated_text']
                answer = generated_text[len(prompt):].strip()
                print(answer)
                output_data[prompt_key]["outputs"].append(answer)

    print("Experiment completed.")
    return output_data


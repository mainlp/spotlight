import json

group_size = 50
target_ratio = 0.9

with open(f'gender_bias_{group_size}_{target_ratio}_ratio.json', 'r') as file:
    data = json.load(file)

non_bias_sample = data['prompt_1']['non_bias_setting']
bias_sample = data['prompt_1'][f'bias_setting_{target_ratio}_ratio']

prompt = f"""
You are given texts from two different groups. Please identify words or phrases that are systematically different between the texts of the two groups.

Here is the data you need to analyze:
'''
Group 1: {bias_sample}

Group 2: {non_bias_sample}
'''
Please be concise and short in your answer.
"""


data = {
    "model_name": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "experiment_name": "gender-bias-llama3-8b",
    "prompt": [prompt],
    "repetition": 1,
    "seed": 42,
    "top_p": 0.9,
    "top_k": 10,
    "temperature": 0.7,
    "max_new_tokens": 256,
    "group_size":group_size,
    "target_ratio":target_ratio

}

with open('config/config.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("The file has been successfully saved to 'config/config.json'")

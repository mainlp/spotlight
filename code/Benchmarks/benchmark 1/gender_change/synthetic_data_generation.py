import json
import random
from gender_bias_functions import sample_classification, perform_gender_bias, extract_first_two_sentences

group_size = 100
target_ratio = 0.9

with open('generated_outputs.json', 'r') as file:
    data = json.load(file)

outputs = data['prompt_1']['outputs']
print(f"The number of outputs is {len(outputs)}.")

he_outputs, she_outputs = sample_classification(outputs)

print(f"The number of filtered male examples is {len(he_outputs)}.")
print(f"The number of filtered female examples is {len(she_outputs)}.")

random.seed(42)

non_bias_setting, non_bias_replaced_words, non_bias_replacement_words = perform_gender_bias(0.5, he_outputs[:group_size])
# non_bias_setting = extract_first_two_sentences(non_bias_setting)
random.shuffle(non_bias_setting)
print(f"The number of samples for non-bias setting is {len(non_bias_setting)}.")


bias_setting, bias_replaced_words, bias_replacement_words = perform_gender_bias(target_ratio, he_outputs[group_size:group_size+group_size])
# bias_setting = extract_first_two_sentences(bias_setting)
random.shuffle(bias_setting)
print(f"The number of samples for bias setting is {len(bias_setting)}.")


data['prompt_1']['non_bias_setting'] = non_bias_setting
data['prompt_1'][f'bias_setting_{target_ratio}_ratio'] = bias_setting
data['prompt_1']['non_bias_replaced_words'] = non_bias_replaced_words
data['prompt_1']['non_bias_replacement_words'] = non_bias_replacement_words
data['prompt_1'][f'bias_replaced_words_{target_ratio}_ratio'] = bias_replaced_words
data['prompt_1'][f'bias_replacement_words_{target_ratio}_ratio'] = bias_replacement_words

with open(f'gender_bias_{group_size}_{target_ratio}_ratio.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

print(f"Filtered non-gender-bias and gender-bias outputs have been saved to 'gender_bias_{group_size}_{target_ratio}_ratio.json'.")


import json
import re
import pickle
import spacy
from pypremise import Premise, data_loaders
from contextlib import redirect_stdout


def run_experiment(group_0_sample, group_1_sample, file_name):

    nlp = spacy.load("en_core_web_sm")
    tokenized_group_0 = [[token.text for token in nlp(sample)] for sample in group_0_sample]
    tokenized_group_1 = [[token.text for token in nlp(sample)] for sample in group_1_sample]

    label_group_0 = [0 for _ in tokenized_group_0]
    label_group_1 = [1 for _ in tokenized_group_1]

    features = tokenized_group_1 + tokenized_group_0
    labels = label_group_0 + label_group_1

    premise_instances, voc_token_to_index, voc_index_to_token = data_loaders.from_token_lists(features, labels)
    premise = Premise(voc_index_to_token=voc_index_to_token)

    premise_patterns = premise.find_patterns(premise_instances)

    with open(file_name, 'w') as f:
        with redirect_stdout(f):
            for pattern in premise_patterns:
                print(pattern)

    print(f"Pattern has been saved to {file_name}.")

def extract_patterns(file_name):
    pattern_list = []

    with open(file_name, 'r') as file:
        patterns = file.readlines()

    for pattern in patterns:
        # Extract the contents inside brackets
        extracted_content = re.findall(r'\((.*?)\)', pattern)
        pattern = extracted_content[:-1]
        pattern_list.append(pattern)

    total_patterns = [list(pair) for pair in set(tuple(pair) for pair in pattern_list)]

    return total_patterns


def main1():

    group_size = 100
    target_ratio = 0.8

    with open(f'gender_bias_{group_size}_{target_ratio}_ratio.json', 'r') as file:
        data = json.load(file)

    group_0_sample = data['prompt_1']["non_bias_setting"]
    group_1_sample = data['prompt_1'][f"bias_setting_{target_ratio}_ratio"]

    file_name = f"premise_{group_size}_{target_ratio}_ratio.txt"

    run_experiment(group_0_sample, group_1_sample, file_name)

def main2():

    prompt_number = 1
    prompt_index = prompt_number -1

    with open('modification_log.pkl', 'rb') as file:
        flattened_logs = pickle.load(file)

    nlp = spacy.load("en_core_web_sm")

    group_0_list = list(set(flattened_logs[prompt_index][0]))
    gold_group_0 = [[token.text for token in nlp(sample)] for sample in group_0_list]

    group_1_list = list(set(flattened_logs[prompt_index][1]))
    gold_group_1 = [[token.text for token in nlp(sample)] for sample in group_1_list]

    gold = [list(pair) for pair in set(tuple(pair) for pair in (gold_group_0 + gold_group_1))]


    with open('style_transfer.json', 'r') as file:
        data = json.load(file)

    group_0_sample = data[f"prompt_{prompt_number}"]["group_0_sample"]
    group_1_sample = data[f"prompt_{prompt_number}"]["group_1_sample"]

    file_name = f"premise_prompt_{prompt_index}.txt"

    run_experiment(group_0_sample, group_1_sample, file_name)

    total_patterns = extract_patterns(file_name)

    data_to_save = {
        "title": f"Prompt {prompt_index}",
        "found_patterns": total_patterns,
        "gold_patterns": gold
    }

    with open(f'premise_prompt_{prompt_index}.json', "w") as combined_file:
        json.dump(data_to_save, combined_file, ensure_ascii=False, indent=4)


def main3():

    group_size = 5000

    with open(f'rules_{group_size}.json', 'r') as file:
        data = json.load(file)

    gold = data['gold']

    with open(f'movie_reviews.json', 'r') as file:
        data = json.load(file)

    group_0_sample = data['positive_reviews'][:group_size]
    group_1_sample = data['negative_reviews'][:group_size]

    file_name = f"premise_{group_size}.txt"

    run_experiment(group_0_sample, group_1_sample, file_name)

    total_patterns = extract_patterns(file_name)

    data_to_save = {
        "title": f"Group size {group_size}",
        "found_patterns": total_patterns,  # The list of total patterns
        "gold_patterns": gold
    }

    with open(f'premise_{group_size}.json', "w") as combined_file:
        json.dump(data_to_save, combined_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main1()

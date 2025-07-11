import json
import os
import time
import shutil
from PyPremise.pypremise import Premise, data_loaders
from contextlib import redirect_stdout
import random 
import re
import pickle
import spacy

# load generated email
with open('anonymzed/generated_outputs.json', 'r') as file:
    data = json.load(file)


# Emoji list
emoji_list = [" 😊", " 😂", " 😎", " 😍", " 👍", " 🤔", " 🎉", " 🙌", " 💡", " 🔥"]

# Function to insert emoji
def insert_random_emoji(text, emoji_ratio=0.3, logs=None, original_logs=None):
    sentences = re.split(r'(?<=\w[.!?])\s+', text)
    updated_sentences = []
    for sentence in sentences:
        if random.random() < emoji_ratio:
            emoji = random.choice(emoji_list)
            updated_sentences.append(sentence + emoji)
            if logs is not None:
                logs.append(emoji[1])
        else:
            updated_sentences.append(sentence)
    return ' '.join(updated_sentences)

# Function to replace email opening
def replace_email_opening(text, opening_rate=0.3, logs=None, original_logs=None):
    opening_phrases = [
        "Just checking in!",
        "Wanted to drop you a note!",
        "Long time no see, hope all's good!",
        "Quick one for you:"
    ]
    pattern = r"\bi hope this email finds you well."
    if random.random() < opening_rate:
        replacement = random.choice(opening_phrases)
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            if original_logs is not None:
                original_logs.append(match.group())  # Only append the matched pattern
            if logs is not None:
                logs.append(replacement)
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

# Function to replace closing phrases
def replace_closing_phrases(text, closing_ratio=0.3, logs=None, original_logs=None):
    closing_phrases = [
        "Let me know what you think!",
        "Catch you soon!",
        "Cheers and talk soon!",
        "Let’s chat more about this later!",
        "Shoot me a reply when you can."
    ]
    phrases_to_replace = ["sincerely,", "best regards,"]
    def random_replacement(match):
        replacement = random.choice(closing_phrases)
        if original_logs is not None:
            original_logs.append(match.group())  # Only append the matched pattern
        if logs is not None:
            logs.append(replacement)
        return replacement
    if random.random() < closing_ratio:
        for phrase in phrases_to_replace:
            text = re.sub(phrase, random_replacement, text, flags=re.IGNORECASE)
    return text

# Function to change 'Dear Professor'
def change_dear_professor(text, professor_ratio=0.3, logs=None, original_logs=None):
    impolite_phrases = ["Hi", "Hey", "Sup", "Yo", "Howdy"]
    pattern = r"Dear (Professor|Dr\.|Prof\.)"
    if random.random() < professor_ratio:
        replacement = random.choice(impolite_phrases)
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            if original_logs is not None:
                original_logs.append(match.group())  # Only append the matched pattern
            if logs is not None:
                logs.append(replacement)
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

# Function for informal abbreviations
def informal_abb(text, abb_ratio=0.3, logs=None, original_logs=None):
    replacements = {
        r"would like to": "wanna",
        r"have to": "gotta",
        r"please": "plz",
        r"are not": "ain't",
    }
    if random.random() < abb_ratio:
        for pattern, replacement in replacements.items():
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                if original_logs is not None:
                    original_logs.append(match.group())  # Only append the matched pattern
                if logs is not None:
                    logs.append(replacement)
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

# Function to apply all modifications
def apply_modifications_to_samples(samples, emoji_ratio=0.3, closing_ratio=0.3, professor_ratio=0.3, abb_ratio=0.3, opening_rate=0.3):
    modified_samples = []
    all_logs = []
    all_original_logs = []
    for sample in samples:
        logs = []
        original_logs = []
        sample = insert_random_emoji(sample, emoji_ratio, logs, original_logs)
        sample = replace_email_opening(sample, opening_rate, logs, original_logs)
        sample = replace_closing_phrases(sample, closing_ratio, logs, original_logs)
        sample = change_dear_professor(sample, professor_ratio, logs, original_logs)
        sample = informal_abb(sample, abb_ratio, logs, original_logs)
        modified_samples.append(sample)
        all_logs.append(logs)
        all_original_logs.append(original_logs)
    return modified_samples, all_logs, all_original_logs

# define pattern function
def calculate_pattern(i):
    sample = []
    prompt_key = f'prompt_{i}'
    if prompt_key in data:
        sample = data[f'prompt_{i}']['outputs']
        print(len(sample))

    random.shuffle(sample)

    # apply modifications and save logs and original_logs
    modified_sample, logs, original_logs = apply_modifications_to_samples(
        sample[-250:], 
        emoji_ratio=0.3, 
        closing_ratio=0.3, 
        professor_ratio=0.3, 
        abb_ratio=0.3, 
        opening_rate=0.3
    )

    # original sample
    sample = sample[:250]
    nlp = spacy.load("en_core_web_sm")
    tokenized_group_0 = [[token.text for token in nlp(sample)] for sample in sample]
    tokenized_group_1 = [[token.text for token in nlp(sample)] for sample in modified_sample]
    label_group_0 = [0 for sample in tokenized_group_0]
    label_group_1 = [1 for sample in tokenized_group_1]

    features = tokenized_group_1 + tokenized_group_0
    labels = label_group_0 + label_group_1

    # Use PyPremise to detect pattern
    premise_instances, voc_token_to_index, voc_index_to_token = data_loaders.from_token_lists(features, labels)
    premise = Premise(voc_index_to_token=voc_index_to_token)

    premise_patterns = premise.find_patterns(premise_instances)

    # save pattern
    with open(f'prompt_{i}_0.3_test.txt', 'w') as f:
        with redirect_stdout(f):
            for pattern in premise_patterns:
                print(pattern)

    # retrun log and group_1 sample
    return logs, original_logs, modified_sample, sample


all_logs = [[[], []] for _ in range(10)]  
flattened_logs = [[[], []] for _ in range(10)]  

# iterate prompt and calculate pattern
for i in range(1, 11):
    print(i)
    logs, original_logs, group_1_sample, group_0_sample = calculate_pattern(i)
    flattened_logs[i-1][1] = [entry for sublist in logs for entry in sublist]
    flattened_logs[i-1][0] = [entry for sublist in original_logs for entry in sublist]# all modifications saved here, can also be seen as union of patterns, we can use them for later evaluation

    # save bias_sample and non-bias sample
    prompt_key = f'prompt_{i}'
    if prompt_key in data:
        data[prompt_key]['group_1_sample'] = group_1_sample
        data[prompt_key]['group_0_sample'] = group_0_sample

with open('modification_log_test.pkl', 'wb') as file:
    pickle.dump(flattened_logs, file)
output_file = 'anonymzed/updated_outputs_test_0.json'
with open(output_file, 'w') as file:
    json.dump(data, file, indent=4)

print(f"Updated JSON saved to {output_file}")

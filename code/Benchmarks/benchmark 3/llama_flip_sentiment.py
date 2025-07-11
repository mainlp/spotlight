from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import pandas as pd
import numpy as np
import warnings
import nltk
from nltk.corpus import sentiwordnet as swn
import re


warnings.filterwarnings("ignore")

np.random.seed(42)
torch.manual_seed(42)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
print(f"Number of GPUs: {torch.cuda.device_count()}")


def get_relevant_str(token, remaining_review):
    # find sequence of token plus any whitespace after it and any characters before it
    # use first match
    # print(f"Trying to find {token} in:\n{remaining_review}")
    match = re.search(re.escape(token), remaining_review)
    if not match:
        # print(f"Could not find {token} in {remaining_review}")
        return "", remaining_review
    end_id = match.end(0)
    strng = remaining_review[:end_id]
    # print(f"Found '{strng}'")
    # print()
    return strng, remaining_review[len(strng):]
    

def sentiment_score(word, pos_tags=None):
    scores = []
    for synset in swn.senti_synsets(word):
        if pos_tags is None or synset.synset.pos() in pos_tags:
            if np.abs(synset.pos_score() - synset.neg_score()) > 0:
                scores.append(synset.pos_score() - synset.neg_score())
    return np.mean(scores)

def get_model(name = "meta-llama/Llama-3.1-8B-Instruct", device=device):
    tokenizer = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name).to(device)

    model.generation_config.do_sample = False
    
    return tokenizer, model

def generate(tokenizer, model, prompt, max_length=256):
    tokens = tokenizer.encode(prompt, return_tensors="pt")
    tokens = tokens.to(device)
    output = model.generate(tokens, max_length=max_length, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def generate_antonym(tokenizer, model, word, pos_tag, max_length=50):
    instruction = f"What is the antonym to the word '{word.lower()}' that is a{pos_tag} used to express sentiment. \n The antonym is "
    compl_answer = generate(tokenizer, model, instruction, max_length)
    # remove instruction and any newline suffixes
    answer = compl_answer[len(instruction):]
    answer = answer.strip().split("\n")
    antonym_seq = ""
    while not re.findall(r"[A-Za-z]+", antonym_seq):
        antonym_seq = answer.pop(0)
    
    # remove any non-alphabetic characters
    antonym = ""
    toks = nltk.word_tokenize(antonym_seq)
    while antonym in ["", "similar", "opposite", "the"]:
        antonym = toks.pop(0).lower()
        antonym = "".join([c for c in antonym if c.isalpha() or c == "-"])
    
    print(f"Antonym for '{word}' as a {pos_tag} is '{antonym}'")
    print(f"Answer: {compl_answer}")
    print()
    return antonym, compl_answer

def convert_tokens_to_string(tokens):
    # avoid prepending whitespace to punctuation
    sentence = ""
    for token in tokens:
        if nltk.tokenize.punkt.PunktToken(token).is_non_punct:
            sentence += " " + token
        else:
            sentence += token
    return sentence

def main():
    use_verbs = False
    use_nouns = False

    tokenizer, model = get_model()

    reviews = pd.read_csv("data/movie_reviews/reviews_s=42.csv")

    adjective_antonyms = {}
    verb_antonyms = {}
    noun_antonyms = {}

    negative_reviews = []
    pos_tag_col = []
    rules_col = []

    for i, row in reviews.iterrows():
        review = row["review"]
        remaining_review = row["review"]
        flipped_review = ""
        flipped_tokens = []
        tokens = nltk.word_tokenize(review)
        pos_tags = nltk.pos_tag(tokens, tagset="universal")
        rules = []
        for token, tag in pos_tags:
            next_token = token
            relevant_str, remaining_review = get_relevant_str(token, remaining_review)
            # if its a positive sentiment adjective, flip it to negative antonym
            if tag in ["ADJ", "ADV"] and sentiment_score(token, ["a", "s"]) > 0:
                if token not in adjective_antonyms:
                    antonym, _ = generate_antonym(tokenizer, model, token, "n adjective or adverb")
                    adjective_antonyms[token] = antonym
                rules.append(f"'{token}'(a)->'{adjective_antonyms[token]}'")
                next_token = adjective_antonyms[token]
            if tag in ["VERB"] and sentiment_score(token, ["v"]) > 0.3 and use_verbs:
                if token not in verb_antonyms:
                    antonym, _ = generate_antonym(tokenizer, model, token, " verb")
                    verb_antonyms[token] = antonym
                rules.append(f"'{token}'(v)->'{verb_antonyms[token]}'")
                next_token = verb_antonyms[token]
            if tag in ["NOUN"] and sentiment_score(token, ["n"]) > 0.3 and use_nouns:
                if token not in noun_antonyms:
                    antonym, _ = generate_antonym(tokenizer, model, token, " noun")
                    noun_antonyms[token] = antonym
                rules.append(f"'{token}'(n)->'{noun_antonyms[token]}'")
                next_token = noun_antonyms[token]
            flipped_tokens.append(next_token)
            relevant_str = relevant_str.replace(token, next_token, 1)
            flipped_review += relevant_str
        
        # remember pos tags and rules applied
        pos_tag_col.append(pos_tags)
        rules_col.append(rules)

        # negative_reviews.append(convert_tokens_to_string(flipped_tokens))
        negative_reviews.append(flipped_review + remaining_review)
        print(f"Processed {i} reviews", end="\r")
        print(review, remaining_review, flipped_review, sep="\n", end="\n\n\n")

    reviews["negative_review"] = negative_reviews
    reviews["pos_tags"] = pos_tag_col
    reviews["rules"] = rules_col

    reviews.to_csv("data/movie_reviews/reviews_s=42_flipped_new.csv", index=False)

    adj_antonyms = pd.DataFrame(adjective_antonyms.items(), columns=["word", "antonym"])
    adj_antonyms["pos"] = "a"
    vrb_antonyms = pd.DataFrame(verb_antonyms.items(), columns=["word", "antonym"])
    vrb_antonyms["pos"] = "v"
    nn_antonyms = pd.DataFrame(noun_antonyms.items(), columns=["word", "antonym"])
    nn_antonyms["pos"] = "n"
    print("Number of adjective antonyms:", len(adjective_antonyms))
    print("Number of verb antonyms:", len(verb_antonyms))
    print("Number of noun antonyms:", len(noun_antonyms))

    antonyms = pd.concat([adj_antonyms, vrb_antonyms, nn_antonyms])
    antonyms.to_csv("data/movie_reviews/adj_antonyms_new.csv", index=False)

if __name__ == "__main__":
    main()
                



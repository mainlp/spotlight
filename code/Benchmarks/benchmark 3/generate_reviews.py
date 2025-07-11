from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import pandas as pd
import numpy as np
import warnings
import nltk


warnings.filterwarnings("ignore")

seed = 43

np.random.seed(seed)
torch.manual_seed(seed)

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
print(f"Number of GPUs: {torch.cuda.device_count()}")

def get_model(name = "meta-llama/Llama-3.1-8B-Instruct", device=device):
    tokenizer = AutoTokenizer.from_pretrained(name)
    model = AutoModelForCausalLM.from_pretrained(name).to(device)
    
    return tokenizer, model

def generate(tokenizer, model, prompt, max_length=256):
    tokens = tokenizer.encode(prompt, return_tensors="pt")
    tokens = tokens.to(device)
    output = model.generate(tokens, max_length=max_length, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def generate_review(tokenizer, model, movie, max_length=256):
    instruction = f"Write a positive short review for the movie '{movie}'. Answer with only the review and nothing else."
    review = generate(tokenizer, model, instruction, max_length)
    # remove instruction and any newline suffixes
    review = review[len(instruction):]
    review = review.strip().split("\n")[0]
    return review

tokenizer, model = get_model()

print(generate_review(tokenizer, model, "Hello World"))

movies = pd.read_csv("data/movies/title.basics.tsv", sep="\t")
movies = movies[movies["titleType"] == "movie"]

titles = movies.sample(5000)["primaryTitle"].values
print(titles[:10])

fname = f"data/movie_reviews/reviews_checkpoint_s={seed}.csv"

# load checkpoint
#checkpoint = pd.read_csv("data/movie_reviews/reviews_checkpoint.csv") # fname)
#reviews = checkpoint["review"].tolist()
checkpoint = []

reviews = []
for i, title in enumerate(titles[len(reviews):]):
    review = generate_review(tokenizer, model, title)
    reviews.append(review)

    if i % 100 == 0:
        print(f"Generated {i} reviews")
        checkpoint_new = pd.DataFrame({"title": titles[:len(checkpoint)+i+1], "review": reviews})
        checkpoint_new.to_csv(fname, index=False)

reviews_df = pd.DataFrame({"title": titles, "review": reviews})
reviews_df.to_csv(f"data/movie_reviews/reviews_s={seed}=.csv", index=False)
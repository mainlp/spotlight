import pandas as pd
import json
import time
import os


def convert_csv_to_json(fname):
    # load checkpoint
    reviews = pd.read_csv(fname)
    json_dict = dict()
    for cname in reviews.columns:
        json_dict[cname] = reviews[cname].tolist()
    with open(fname + ".json", "w") as f:
        json.dump(json_dict, f)

def store_config(fname, seed):
    config = {
        "experiment_name": "movie_reviews",
        "seed_movie_names": seed,
        "fname_samples": fname,
        "prompt": "Write a positive short review for the movie '{movie}'. Answer with only the review and nothing else.",
        "max_length": 256,
        "n_samples": 5000,
        "model": "meta-llama/Llama-3.1-8B-Instruct",
    }
    with open(fname + "_config.json", "w") as f:
        json.dump(config, f)


if __name__ == "__main__":

    t = time.time()
    path = f"data/movie_reviews/final_{t}/"

    os.makedirs(path, exist_ok=True)

    os.system("cp data/movie_reviews/reviews_s=42_flipped_new.csv " + path + "reviews_flipped_adj_5000.csv")
    os.system("cp data/movie_reviews/reviews_s=43.csv " + path + "reviews_clean_5000.csv")
    os.system("cp data/movie_reviews/adj_antonyms_new.csv " + path + "adj_antonyms.csv")

    fname = path + "reviews_flipped_adj_5000.csv"
    convert_csv_to_json(fname)
    store_config(fname, 42)
    fname = path + "reviews_clean_5000.csv"
    convert_csv_to_json(fname)
    store_config(fname, 43)


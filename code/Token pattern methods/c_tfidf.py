import numpy as np
import scipy.sparse as sp
import json
import pickle
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils.validation import check_array
from sklearn.preprocessing import normalize
from typing import List
from sklearn.feature_extraction.text import TfidfTransformer


class ClassTfidfTransformer(TfidfTransformer):

    def __init__(
        self,
        bm25_weighting: bool = False,
        reduce_frequent_words: bool = False,
        seed_words: List[str] = None,
        seed_multiplier: float = 2,
    ):
        self.bm25_weighting = bm25_weighting
        self.reduce_frequent_words = reduce_frequent_words
        self.seed_words = seed_words
        self.seed_multiplier = seed_multiplier
        super(ClassTfidfTransformer, self).__init__()

    def fit(self, X: sp.csr_matrix, multiplier: np.ndarray = None):

        X = check_array(X, accept_sparse=("csr", "csc"))
        if not sp.issparse(X):
            X = sp.csr_matrix(X)
        dtype = np.float64

        if self.use_idf:
            _, n_features = X.shape

            df = np.squeeze(np.asarray(X.sum(axis=0)))

            avg_nr_samples = int(X.sum(axis=1).mean())

            if self.bm25_weighting:
                idf = np.log(1 + ((avg_nr_samples - df + 0.5) / (df + 0.5)))

            else:
                idf = np.log((avg_nr_samples / df) + 1)

            if multiplier is not None:
                idf = idf * multiplier

            self._idf_diag = sp.diags(
                idf,
                offsets=0,
                shape=(n_features, n_features),
                format="csr",
                dtype=dtype,
            )

        return self

    def transform(self, X: sp.csr_matrix):

        if self.use_idf:
            X = normalize(X, axis=1, norm="l1", copy=False)

            if self.reduce_frequent_words:
                X.data = np.sqrt(X.data)

            X = X * self._idf_diag

        return X

def fit(self, X: sp.csr_matrix, multiplier: np.ndarray = None):

    X = check_array(X, accept_sparse=("csr", "csc"))
    if not sp.issparse(X):
        X = sp.csr_matrix(X)
    dtype = np.float64

    if self.use_idf:
        _, n_features = X.shape

        df = np.squeeze(np.asarray(X.sum(axis=0)))

        avg_nr_samples = int(X.sum(axis=1).mean())

        if self.bm25_weighting:
            idf = np.log(1 + ((avg_nr_samples - df + 0.5) / (df + 0.5)))

        else:
            idf = np.log((avg_nr_samples / df) + 1)

        if multiplier is not None:
            idf = idf * multiplier

        self._idf_diag = sp.diags(
            idf,
            offsets=0,
            shape=(n_features, n_features),
            format="csr",
            dtype=dtype,
        )

    return self

def transform(self, X: sp.csr_matrix):

    if self.use_idf:
        X = normalize(X, axis=1, norm="l1", copy=False)

        if self.reduce_frequent_words:
            X.data = np.sqrt(X.data)

        X = X * self._idf_diag

    return X

def run_experiment(group_0, group_1, group_0_number, group_1_number):

    # Combine class documents
    class_docs = [
        " ".join(group_0),
        " ".join(group_1)
    ]

    # Vectorize text data
    vectorizer = CountVectorizer()
    X_counts = vectorizer.fit_transform(class_docs)

    feature_names = vectorizer.get_feature_names_out()

    transformer = ClassTfidfTransformer(bm25_weighting=True, reduce_frequent_words=True)
    X_ctfidf = transformer.fit_transform(X_counts)

    # Initialize lists for patterns
    group_0_patterns = []
    group_1_patterns = []

    # Extract patterns from Group 0
    group_0_row = X_ctfidf.toarray()[0]  # Group 0 row
    group_0_indices = np.argsort(group_0_row)[-group_0_number:][::-1]  # Top group_0_number indices
    for idx in group_0_indices:
        group_0_patterns.append([feature_names[idx]])

    # Extract patterns from Group 1
    group_1_row = X_ctfidf.toarray()[1]  # Group 1 row
    group_1_indices = np.argsort(group_1_row)[-group_1_number:][::-1]  # Top group_1_number indices
    for idx in group_1_indices:
        group_1_patterns.append([feature_names[idx]])

    # Combine all patterns into a single list
    total_patterns = [list(pair) for pair in set(tuple(pair) for pair in (group_1_patterns + group_0_patterns))]

    return total_patterns


def main1():

    group_size = 100
    target_ratio = 0.8

    with open(f'gender_bias_{group_size}_{target_ratio}_ratio.json', 'r') as file:
        data = json.load(file)

    group_0_number = len(data['prompt_1'][f"bias_replacement_words_{target_ratio}_ratio"])
    group_1_number = len(data['prompt_1'][f"bias_replaced_words_{target_ratio}_ratio"])

    group_0 = data['prompt_1']["non_bias_setting"]
    group_1 = data['prompt_1'][f"bias_setting_{target_ratio}_ratio"]

    total_patterns = run_experiment(group_0, group_1, group_0_number, group_1_number)

    data_to_save = {
        "title": f"Group Size {group_size}\n"
                 f"Target Ratio {target_ratio}",
        "found_patterns": total_patterns
    }

    output_file = f"tfidf_{group_size}_{target_ratio}_ratio.json"

    with open(output_file, 'w') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

    print(f"Patterns have been saved to {output_file}")

def main2():

    prompt_number = 1
    prompt_index = prompt_number - 1

    with open('style_transfer.json', 'r') as file:
        data = json.load(file)

    group_0 = data[f"prompt_{prompt_number}"]["group_0_sample"]
    group_1 = data[f"prompt_{prompt_number}"]["group_1_sample"]


    with open('modification_log.pkl', 'rb') as file:
        flattened_logs = pickle.load(file)

    nlp = spacy.load("en_core_web_sm")

    group_0_list = list(set(flattened_logs[prompt_index][0]))
    gold_group_0 = [[token.text for token in nlp(sample)] for sample in group_0_list]
    group_0_number = len(gold_group_0)

    group_1_list = list(set(flattened_logs[prompt_index][1]))
    gold_group_1 = [[token.text for token in nlp(sample)] for sample in group_1_list]
    group_1_number = len(gold_group_1)

    total_patterns = run_experiment(group_0, group_1, group_0_number, group_1_number)

    gold = [list(pair) for pair in set(tuple(pair) for pair in (gold_group_0 + gold_group_1))]

    output_file = f"tfidf_prompt_{prompt_index}.json"

    data_to_save = {
        "title": f"Prompt {prompt_index}",
        "found_patterns": total_patterns,
        "gold_patterns": gold
    }

    with open(output_file, "w") as combined_file:
        json.dump(data_to_save, combined_file, ensure_ascii=False, indent=4)


def main3():

    group_size = 5000

    # Load rules
    with open(f'rules_{group_size}.json', 'r') as file:
        rules_data = json.load(file)

    gold = rules_data['gold']
    group_0_number = rules_data['positive_pattern_number']
    group_1_number = rules_data['negative_pattern_number']

    # Load reviews
    with open(f'movie_reviews.json', 'r') as file:
        reviews_data = json.load(file)

    group_0 = reviews_data["positive_reviews"]
    group_1 = reviews_data['negative_reviews']

    total_patterns = run_experiment(group_0, group_1, group_0_number, group_1_number)

    output_file = f"patterns_{group_size}_tfidf.json"

    data_to_save = {
        "title": f"Group size {group_size}",
        "found_patterns": total_patterns,
        "gold_patterns": gold
    }

    with open(output_file, 'w') as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

    print(f"Patterns have been saved to {output_file}")

if __name__ == "__main__":
    main1()

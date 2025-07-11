import json


def write_metrics_to_file(prompt_number, frequency_group, soft_metrics, strict_metrics, output_file):
    """
    Write the soft and strict F1 scores, precision, and recall for a given prompt to a text file.

    Parameters:
    prompt_number (int): The prompt number.
    soft_metrics (dict): Dictionary containing soft precision, recall, and F1 score.
    strict_metrics (dict): Dictionary containing strict precision, recall, and F1 score.
    output_file (str): The path to the output text file.
    frequency_group (str, optional): The frequency group information to include in the file.
    """
    with open(output_file, 'a') as file:
        if prompt_number is not None:
            file.write(f"Prompt {prompt_number}:\n")
            file.write(f"  Soft Precision: {soft_metrics['precision']:.3f}\n")
            file.write(f"  Soft Recall: {soft_metrics['recall']:.3f}\n")
            file.write(f"  Soft F1 Score: {soft_metrics['f1']:.3f}\n")
            file.write(f"  Strict Precision: {strict_metrics['precision']:.3f}\n")
            file.write(f"  Strict Recall: {strict_metrics['recall']:.3f}\n")
            file.write(f"  Strict F1 Score: {strict_metrics['f1']:.3f}\n\n")

        else:
            file.write(f"Frequency Group {frequency_group}:\n")
            file.write(f"  Soft Precision: {soft_metrics['precision']:.3f}\n")
            file.write(f"  Soft Recall: {soft_metrics['recall']:.3f}\n")
            file.write(f"  Soft F1 Score: {soft_metrics['f1']:.3f}\n")
            file.write(f"  Strict Precision: {strict_metrics['precision']:.3f}\n")
            file.write(f"  Strict Recall: {strict_metrics['recall']:.3f}\n")
            file.write(f"  Strict F1 Score: {strict_metrics['f1']:.3f}\n\n")


def calculate_metrics(predicted, gold, match_type):
    tp = 0
    fp = 0
    fn = 0

    matched_gold_indices = set()  # Used to track already matched gold sublists

    for predicted_sublist in predicted:
        matched = False
        for i, gold_sublist in enumerate(gold):
            if i in matched_gold_indices:
                continue  # Skip already matched gold sublists
            if match_type == 'strict':
                # Strict match: exact match of sets
                if set(predicted_sublist) == set(gold_sublist):
                    tp += 1
                    matched_gold_indices.add(i)  # Mark as matched
                    matched = True
                    break
            elif match_type == 'soft':
                # Soft match: overlap between sets
                if set(predicted_sublist) & set(gold_sublist):
                    tp += 1
                    matched_gold_indices.add(i)  # Mark as matched
                    matched = True
                    break
        if not matched:
            fp += 1  # Predicted sublist not matched with any gold sublist

    # Calculate false negatives
    for i, gold_sublist in enumerate(gold):
        if i not in matched_gold_indices:
            fn += 1  # Gold sublist not matched with any predicted sublist

    # Calculate precision and recall
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    # Calculate F1 score
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {"precision": precision, "recall": recall, "f1": f1}


def main2():
    for baseline in ['subgroup', 'cortana', 'ctfidf', 'premise']:
        output_file = f'metrics_style_transfer_{baseline}.txt'
        for i in range(10):
            with open(f'{baseline}_prompt_{i}.json', 'r') as file:
                data = json.load(file)

            prediction = data['found_patterns']
            gold = data['gold_patterns']

            soft_metrics = calculate_metrics(prediction, gold, 'soft')
            strict_metrics = calculate_metrics(prediction, gold, 'strict')

            # Write metrics to a text file
            write_metrics_to_file(i, None, soft_metrics, strict_metrics, output_file)

        print(f"Metrics written to {output_file}.")


def main3():
    for baseline in ['subgroup', 'cortana', 'ctfidf', 'premise']:
        output_file = f'metrics_movie_review_{baseline}.txt'
        for frequency_group in ['1', '5', '10', '100', '300']:
            with open(f'{baseline}_{frequency_group}_group.json', 'r') as file:

                data = json.load(file)
                prediction = data['prediction']
                gold = data['gold']

                soft_metrics = calculate_metrics(prediction, gold, 'soft')
                strict_metrics = calculate_metrics(prediction, gold, 'strict')

                # Write metrics to a text file with frequency group
                write_metrics_to_file(None, frequency_group, soft_metrics, strict_metrics, output_file)

        print(f"Metrics written to {output_file}.")

if __name__ == "__main__":
    main2()

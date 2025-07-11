import re

def sample_classification(samples):

    he_samples = []
    she_samples = []
    for sample in samples:
        he_match = re.search(r'\b(he|He|his|His|him|Him)\b', sample)
        she_match = re.search(r'\b(she|She|her|Her)\b', sample)
        if he_match and she_match:
            he_index = he_match.start()
            she_index = she_match.start()
            if he_index < she_index:
                he_samples.append(sample)
            else:
                she_samples.append(sample)
        elif he_match:
            he_samples.append(sample)
        elif she_match:
            she_samples.append(sample)

    return he_samples,she_samples


def change_gender(text, to_replace_pronoun, replacement_pronoun, to_replace_possessive, replacement_possessive, to_replace_object, replacement_object):

    replaced_words = {}
    replacement_words = {}

    text, count = re.subn(r'\b' + to_replace_pronoun + r'\b', replacement_pronoun, text)
    if count > 0:
        replaced_words[to_replace_pronoun] = replaced_words.get(to_replace_pronoun, 0) + count
        replacement_words[replacement_pronoun] = replacement_words.get(replacement_pronoun, 0) + count

    text, count = re.subn(r'\b' + to_replace_pronoun.lower() + r'\b', replacement_pronoun.lower(), text)
    if count > 0:
        replaced_words[to_replace_pronoun.lower()] = replaced_words.get(to_replace_pronoun.lower(), 0) + count
        replacement_words[replacement_pronoun.lower()] = replacement_words.get(replacement_pronoun.lower(), 0) + count

    text, count = re.subn(r'\b' + to_replace_possessive + r'\b', replacement_possessive, text)
    if count > 0:
        replaced_words[to_replace_possessive] = replaced_words.get(to_replace_possessive, 0) + count
        replacement_words[replacement_possessive] = replacement_words.get(replacement_possessive, 0) + count

    text, count = re.subn(r'\b' + to_replace_possessive.lower() + r'\b', replacement_possessive.lower(), text)
    if count > 0:
        replaced_words[to_replace_possessive.lower()] = replaced_words.get(to_replace_possessive.lower(), 0) + count
        replacement_words[replacement_possessive.lower()] = replacement_words.get(replacement_possessive.lower(), 0) + count

    text, count = re.subn(r'\b' + to_replace_object + r'\b', replacement_object, text)
    if count > 0:
        replaced_words[to_replace_object] = replaced_words.get(to_replace_object, 0) + count
        replacement_words[replacement_object] = replacement_words.get(replacement_object, 0) + count

    text, count = re.subn(r'\b' + to_replace_object.lower() + r'\b', replacement_object.lower(), text)
    if count > 0:
        replaced_words[to_replace_object.lower()] = replaced_words.get(to_replace_object.lower(), 0) + count
        replacement_words[replacement_object.lower()] = replacement_words.get(replacement_object.lower(), 0) + count

    return text, replaced_words, replacement_words


def perform_gender_bias(target_ratio, samples):

    to_change = round((1 - target_ratio) * len(samples))

    all_replaced_words = {}
    all_replacement_words = {}

    for i in range(len(samples)):
        if to_change == 0:
            break
        else:
            samples[i], replaced_words, replacement_words = change_gender(samples[i], "He", "She", "His", "Her", 'Him', 'Her')

            for word, count in replaced_words.items():
                all_replaced_words[word] = all_replaced_words.get(word, 0) + count
            for word, count in replacement_words.items():
                all_replacement_words[word] = all_replacement_words.get(word, 0) + count

            to_change -= 1

    return samples, all_replaced_words, all_replacement_words


def extract_first_two_sentences(samples):
    result = []

    for sample in samples:
        sentences = re.split(r'(?<=[.!?])\s+', sample)

        extracted_sentences = ' '.join(sentences[:3])

        if extracted_sentences and extracted_sentences[-1] not in '.!?':
            extracted_sentences += '.'

        result.append(extracted_sentences)

    return result



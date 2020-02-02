from json import load
from difflib import get_close_matches


def get_user_input() -> str:
    return input("Enter word: ")


def load_data() -> {}:
    return load(open("data.json"))


def get_definitions(word: str) -> []:
    return data[word]


def get_similar_words(word, dict_keys) -> str:
    return get_close_matches(word, list(dict_keys), 1, cutoff=0.60)


def print_definitions(word: str) -> None:
    definitions = get_definitions(word)
    for definition in definitions:
        print(definition)


def handle_similar_word(word, keys):
    similar_words = get_similar_words(word, keys)
    closest_match = similar_words[0]
    proceed_with_similar_word = input(f"Did you mean {closest_match}? Enter y/n: \n")
    if proceed_with_similar_word == 'y' or proceed_with_similar_word == 'Y':
        print_definitions(closest_match)
    elif proceed_with_similar_word == 'n' or proceed_with_similar_word == 'N':
        print(f"Word not found. Please double check {word}")
    else:
        print("Sorry, could not understand your entry")


def match_user_input_with_key(user_input: str, keys: list):
    if user_input in keys:
        return user_input
    elif user_input.title() in keys:
        return user_input.title()
    elif user_input.lower() in keys:
        return user_input.lower()
    else:
        return ""


if __name__ == "__main__":
    data = load_data()
    user_input = get_user_input()
    matching_key = match_user_input_with_key(user_input, data.keys())
    if matching_key:
        print_definitions(matching_key)
    elif len(get_similar_words(user_input, data.keys())) > 0:
        handle_similar_word(user_input, data.keys())
    else:
        print(f"Word not found. Please double check {user_input}")

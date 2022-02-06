#!/usr/bin/python3
import deepl 
import os
import sys
import json
import urllib.request
import getopt

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def read_file(file_name):
    file = open(file_name, "r")
    return file.read()

def extract_lines(text):
    return text.split("\n")

def transform_lines(lines):
    transformed_lines = []

    for line in lines:
        line = line.replace("<i>", "").replace("</i>", "").replace("<b>", "").replace("</b>", "").replace("<em>", "").replace("</em>", "").replace("<strong>", "").replace("</strong>", "")
        
        transformed_lines.append(line)

    return transformed_lines


def concat_sentences(lines):
    with_concated_sentences_lines = []

    prev_line = ""
    for line in lines:
        new_line = line

        if prev_line != "" and line != "" and prev_line != line:
            new_line = prev_line + " " + line
            prev_line = line
            with_concated_sentences_lines.pop()
            with_concated_sentences_lines.append(new_line)
        else:
            prev_line = line
            with_concated_sentences_lines.append(new_line)

    return with_concated_sentences_lines


def filter_empty_lines(lines):
    filtered_lines = []

    for line in lines:
        if line == "":
            continue
        
        filtered_lines.append(line)

    return filtered_lines

def translate_lines_by_deepl(lines, auth_key, target_lang):
    translator = deepl.Translator(auth_key) 
    result = translator.translate_text(lines, target_lang=target_lang) 
    translated_list = []

    for raw_translate in result:
        translated_list.append(raw_translate.text)

    return translated_list

def match_original_and_translate_lines(original_lines, translated_lines):
    idx = 0
    original_and_translate_pairs = []

    while idx < len(original_lines):
       pair = [original_lines[idx], translated_lines[idx]] 
       original_and_translate_pairs.append(pair)
       idx = idx + 1

    return original_and_translate_pairs



def print_help():
    print("""
Create Anki cards with DeepL translation 

Example:

    python3 create-anki-cards-by-deepl.py --input example-input.txt --target-lang RU --name "my deck" --auth-key=<AUTH-KEY>

Options:
    --help              Show help                           [boolean]
    --input             Source for translating              [string]
    --target-lang       Target language from DeepL          [string]
    --auth-key          Auth key for DeepL service          [string]
    --name              Anki deck name                      [string]
""")

def handle_user_input(argv):
    source_file = ""
    target_lang = ""
    auth_key = ""
    deck_name = ""

    try:
        opts, args = getopt.getopt(argv, "hi:o:",["input=", "target-lang=", "auth-key=", "name=", "help"])
    except getopt.GetoptError as e:
        print("Unexpected error", e) 
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("--help"): 
            print_help()
            sys.exit()
        elif opt in ("--input"):
            source_file = arg
        elif opt in ("--target-lang"):
            target_lang = arg
        elif opt in ("--auth-key"):
            auth_key = arg
        elif opt in ("--name"):
            deck_name = arg

    if (source_file == ""):
        print("Program exited. --input argument required")
        sys.exit()
    if (target_lang == ""):
        print("Program exited. --target-lang argument required")
        sys.exit()
    if (auth_key == ""):
        print("Program exited. --auth-key argument required")
        sys.exit()
    if (deck_name == ""):
        print("Program exited. --name argument required")
        sys.exit()

    user_input  = dict();
    user_input ['source_file'] = source_file;
    user_input ['target_lang'] = target_lang;
    user_input ['auth_key'] = auth_key;
    user_input ['deck_name'] = deck_name;

    return user_input

def create_anki_deck(deck_name):
  invoke('createDeck', deck=deck_name)

def create_anki_card(deck_name, front_content, back_content):
  invoke('addNote', note={
        "deckName": deck_name,
        "modelName": "Basic",
        "fields": {
            "Front": front_content,
            "Back": back_content
        },
    "options": {
        "allowDuplicate": True,
    }
  })


def create_anki_cards(deck_name, card_pairs):
    idx = 0
    while idx < len(card_pairs):
        create_anki_card(deck_name, card_pairs[idx][0], card_pairs[idx][1])
        idx = idx + 1

def main(argv):
    user_input = handle_user_input(argv)
    source_file = user_input.get("source_file")
    target_lang = user_input.get("target_lang")
    auth_key = user_input.get("auth_key")
    deck_name = user_input.get("deck_name")
    text = read_file(source_file)
    raw_lines = extract_lines(text)
    transformed_lines = transform_lines(raw_lines)
    with_sentences_lines = concat_sentences(transformed_lines)
    filtered_lines = filter_empty_lines(with_sentences_lines)
    translated_lines = translate_lines_by_deepl(filtered_lines, auth_key, target_lang)
    card_prepared_pairs = match_original_and_translate_lines(filtered_lines, translated_lines)
    create_anki_deck(deck_name);
    create_anki_cards(deck_name, card_prepared_pairs);

main(sys.argv[1:])

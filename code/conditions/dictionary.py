import json
import requests
from urllib.parse import quote


API_KEY = '80d60217-9014-4658-a4b7-dd1d8e9fb90e'
BASE_URL = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/'

input_path = '../../data/en_neologism.jsonl'
output_path = 'res/dictionary.jsonl'


def get_variants(word):
    variants = [word, word.replace(" ", ""), word.replace(" ", "-")]
    if word.endswith('ies'):
        variants.append(word[:-3] + 'y')
    elif word.endswith('s') and not word.endswith('ss'):
        variants.append(word[:-1])
    return list(dict.fromkeys(variants))

results = []

with open(input_path, 'r', encoding='utf-8') as infile:
    for line in infile:
        obj = json.loads(line)
        word = obj['neologism']

        definition = None
        part_of_speech = None
        examples = None
        pronunciation = None
        etymology = None
        inflections = None

        for variant in get_variants(word):
            url = f"{BASE_URL}{quote(variant)}?key={API_KEY}"
            try:
                resp = requests.get(url)
                data = resp.json()

                if isinstance(data, list) and data and isinstance(data[0], dict) and 'shortdef' in data[0]:
                    entry = data[0]

                    # Definition + POS
                    definition = entry.get('shortdef', [None])[0]
                    part_of_speech = entry.get('fl', None)

                    # Examples
                    examples = []
                    if 'def' in entry and entry['def']:
                        senses = entry['def'][0].get('sseq', [])
                        for sense_group in senses:
                            for sense in sense_group:
                                dt = sense[1].get('dt', [])
                                for d in dt:
                                    if d[0] == 'vis':
                                        for ex in d[1]:
                                            examples.append(ex.get('t'))
                    if not examples:
                        examples = None

                    # Pronunciation
                    if 'hwi' in entry and 'prs' in entry['hwi']:
                        pronunciation = entry['hwi']['prs'][0].get('mw')

                    # Etymology
                    if 'et' in entry:
                        etymology_parts = []
                        for et_entry in entry['et']:
                            if isinstance(et_entry, list) and len(et_entry) > 1:
                                etymology_parts.append(et_entry[1])
                        etymology = " ".join(etymology_parts) if etymology_parts else None

                    # Inflections
                    if 'meta' in entry and 'stems' in entry['meta']:
                        inflections = entry['meta']['stems']

                    break
            except Exception as e:
                print(f"Error fetching variant '{variant}' for '{word}': {e}")

        obj['mw_definition'] = definition
        obj['mw_part_of_speech'] = part_of_speech
        obj['mw_examples'] = examples
        obj['mw_pronunciation'] = pronunciation
        obj['mw_etymology'] = etymology
        obj['mw_inflections'] = inflections

        print(obj)
        results.append(obj)

with open(output_path, 'w', encoding='utf-8') as f:
    for item in results:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

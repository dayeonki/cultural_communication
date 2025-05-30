import json

input_file = 'neobench.jsonl'
output_file = 'neobench_preprocessed.jsonl'

rename_keys = {
    "Neologism": "neologism",
    "Definition": "definition",
    "Type": "domain",
    "Linguistic Type": "linguistic_type",
    "Linguistic Subcategory": "linguistic_subcategory",
    "Date": "date",
    "Source": "source_url"
}

remove_keys = [
    "What Is Question",
    "Copy Penalty (MT)",
    "Minimal Pair Sentence 1",
    "Minimal Pair Sentence 2",
    "CLOZE Sentence 1",
    "CLOZE Sentence 2",
    "Alternative Correct Answer",
    "Answer 1",
    "Answer 2",
    "Answer 3",
    "Answer 4",
    "Answer 5",
    "Source.1"
]


with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        data = json.loads(line)
        for old_key, new_key in rename_keys.items():
            if old_key in data:
                data[new_key] = data.pop(old_key)

        for key in remove_keys:
            data.pop(key, None)
        outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

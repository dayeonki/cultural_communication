import json


with open('../../data/neo-bench/neobench.jsonl', 'r') as f:
    definition_to_term = {}
    for line in f:
        item = json.loads(line)
        definition = item.get('Definition')
        term = item.get('Neologism')
        if definition and term:
            definition_to_term[definition.strip()] = term


updated_data = []
with open('colbert_ko.jsonl', 'r') as f:
    for line in f:
        entry = json.loads(line)
        for doc in entry.get('retrieved_docs', []):
            doc_text = doc.get('retrieved_doc', '').strip()
            if doc_text in definition_to_term:
                doc['retrieved_term'] = definition_to_term[doc_text]
        updated_data.append(entry)


with open('colbert_ko2.jsonl', 'w') as f:
    for item in updated_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

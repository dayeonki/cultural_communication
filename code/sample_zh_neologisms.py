import json
import random

BATCH_SIZE = 25

total_neologisms = []
with open('../data/language_situation_official_zh.jsonl', 'r') as f:
    for line in f:
        data = json.loads(line)
        if data['explanatory_hint'].startswith("网络用语"):
            total_neologisms.append(data)
      
random.seed(0)
random.shuffle(total_neologisms)
selected_first_batch = []
for item in total_neologisms:
    if item['word'] not in item['explanatory_hint']:
        selected_first_batch.append(item)
        print(item['word'])
        # print(item['explanatory_hint'])
        if len(selected_first_batch) == BATCH_SIZE:
            break

# print("\n".join([item['word'] for item in selected_first_batch]))

with open('../data/zh_firstbatch.jsonl', 'w') as f:
    for item in selected_first_batch:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

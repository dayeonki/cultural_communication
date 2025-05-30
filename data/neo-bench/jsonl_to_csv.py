import json
import pandas as pd


input_jsonl = 'neobench_twitter_212223.jsonl'
output_csv = 'neobench_twitter_212223.csv'

data = []
with open(input_jsonl, 'r') as infile:
    for line in infile:
        data.append(json.loads(line))

df = pd.DataFrame(data)
df.to_csv(output_csv, index=False, encoding='utf-8-sig')
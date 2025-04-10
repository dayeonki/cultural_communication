import pandas as pd
import json

input_xlsx = 'raw_neobench.xlsx'
output_jsonl = 'neobench.jsonl'

df = pd.read_excel(input_xlsx)

with open(output_jsonl, 'w', encoding='utf-8') as f:
    for _, row in df.iterrows():
        json_obj = row.dropna().to_dict()
        f.write(json.dumps(json_obj, ensure_ascii=False, default=str) + '\n')
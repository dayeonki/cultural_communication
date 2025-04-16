import json
from collections import defaultdict

compiled_word_dict = defaultdict(list)

with open('../../../data/language_situation_official_zh.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        word = data["word"]
        compiled_word_dict[word].append({
            "meaning": data["explanatory_hint"],
            "source": "中国语言生活状况报告",
            "meta": {
                "frequency": data["frequency"],
                "example_sentence": data["example_sentence"],
                "example_sentence_source": data["example_sentence_source"],
                "year": data["year"],
            }
        })


with open("../../../data/yaowenjiaozi_zh.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        word = data["word"]
        compiled_word_dict[word].append({
            "meaning": data["full_explanation"],
            "source": "咬文嚼字",
            "meta": {
                "year": data["year"],
            }
        })

print(len(compiled_word_dict))  # 1032
print(sum([len(data_list) for data_list in compiled_word_dict.values()]))  # 1056

with open("../../../data/compiled/zh_final.jsonl", "w") as f:
    for word, data_list in compiled_word_dict.items():
        f.write(json.dumps({
            "lang": "zh",
            "word": word,
            "explanations": data_list,
        }, ensure_ascii=False) + "\n")

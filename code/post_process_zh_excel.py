import re
import json
import pandas as pd


def split_example(example):
    if "❶" in example and "❷" in example:
        example_list = example.split("\n")
    else:
        example_list = [example]
    
    example_sentence_list = []
    example_sentence_source_list = []
    for example in example_list:
        for i in range(len(example))[::-1]:
            if example[i] == "（" or example[i] == "(":
                example_sentence = example[:i].strip()
                example_sentence_source = example[i:].strip()
                example_sentence_list.append(example_sentence)
                example_sentence_source_list.append(example_sentence_source)
                break
    return example_sentence_list, example_sentence_source_list


def get_raw_jsonl(file_path_list):
    item_list = []
    for file_path in file_path_list:
        df = pd.read_excel(file_path)
        df.columns = ["词目", "提示性释义", "例句", "频次", "文本数"]
        # lang, word, meaning, example, year
        not_unique_word_cnt = 0
        for _, row in df.iterrows():
            if not isinstance(row["词目"], str):
                word = last_word
                not_unique_word_cnt += 1
                frequency = last_frequency
            else:
                word = row["词目"].strip()
                if len(re.findall(r'【(.*?)】', word)) > 0:
                    word = re.findall(r'【(.*?)】', word)[0]
                frequency = row["频次"]

            example_sentence_list, example_sentence_source_list = split_example(
                row["例句"].strip())
            if len(example_sentence_list) > 1:
                explanatory_hint_list = row["提示性释义"].strip().split("\n")
            else:
                explanatory_hint_list = [row["提示性释义"]]
            for example_sentence, example_sentence_source, explanatory_hint in zip(
                    example_sentence_list, example_sentence_source_list, explanatory_hint_list):
                json_data = {
                    "lang": "zh",
                    "word": word.replace("*", ""),
                    "explanatory_hint": explanatory_hint.strip(),
                    "example_sentence": example_sentence,
                    "example_sentence_source": example_sentence_source,
                    "frequency": frequency,
                    "year": file_path[:4],
                    "new_meaning": True if "*" in word else False,
                }
                last_word = json_data["word"]
                last_frequency = json_data["frequency"]
                item_list.append(json_data)
        print(file_path, not_unique_word_cnt)
        # 2022年度媒体新词语表.xlsx 0
        # 2021年度媒体新词语表.xlsx 0
        # 2020年度媒体新词语表.xlsx 0
        # 2019年度媒体新词语表.xlsx 3
    print(f'Total number of words before further processing: {len(item_list)}')
    # Total number of words before further processing: 956
    return item_list


def write2file(raw_item_list):
    unique_word_set = set()
    with open("language_situation_official_zh.jsonl", 'w', encoding='utf-8') as fout:
        for item in raw_item_list:
            json_str = json.dumps(item, ensure_ascii=False)
            fout.write(json_str + '\n')
            unique_word_set.add(item["word"])
    print(f'Total number of unique words: {len(unique_word_set)}')
    # Total number of unique words: 948


def main():
    file_path_list = [
        "2022年度媒体新词语表.xlsx",
        "2021年度媒体新词语表.xlsx",
        "2020年度媒体新词语表.xlsx",
        "2019年度媒体新词语表.xlsx",
    ]
    raw_item_list = get_raw_jsonl(file_path_list)
    write2file(raw_item_list)

if __name__ == "__main__":
    main()

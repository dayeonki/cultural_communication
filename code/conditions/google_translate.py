import json
from deep_translator import GoogleTranslator


input_path = '../../data/en_neologism.jsonl'
output_path = 'res/google_translate.jsonl'


with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
    for line in infile:
        item = json.loads(line)
        # TODO: change to twitter post content
        en_post = item.get('definition', '')
        
        try:
            zh_translation = GoogleTranslator(source='en', target='zh-CN').translate(en_post)
            ko_translation = GoogleTranslator(source='en', target='ko').translate(en_post)
        except Exception as e:
            print(f"Translation error for: {item['definition']} - {e}")
            zh_translation = ""
            ko_translation = ""
        print("English: ", en_post)
        print("Chinese: ", zh_translation)
        print("Korean: ", ko_translation)
        print("\n")

        item['definition_zh'] = zh_translation
        item['definition_ko'] = ko_translation

        outfile.write(json.dumps(item, ensure_ascii=False) + '\n')

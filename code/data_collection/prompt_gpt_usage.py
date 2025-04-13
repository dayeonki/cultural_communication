import openai
import json

openai.api_key = ''

input_path = '../../data/naver_qa.jsonl'
output_path = '../../data/compiled/ko_final.jsonl'


def ask_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.2
        )
        reply = response['choices'][0]['message']['content'].strip()
        return reply
    except Exception as e:
        print(f"[ERROR] {e}")
        return None


with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
    for line in infile:
        entry = json.loads(line)
        word = entry['word']
        explanation = entry['explanation']
        kin_titles = entry['kin_titles']

        prompt = (
            f"신조어 '{word}'는 다음과 같은 의미를 가지고 있습니다:\n"
            f"{explanation}\n\n"
            f"아래는 '{word}'와 관련된 커뮤니티 질문 제목들입니다. "
            f"이 중에서 '{word}'와 가장 잘 어울리는 제목 하나를 골라주세요:\n"
        )
        for i, title in enumerate(kin_titles, 1):
            prompt += f"{i}. {title}\n"
        prompt += "\n가장 적절한 제목의 번호만 숫자로 답해주세요. 없더라도 하나를 골라주세요. 부연설명이나 이유는 하지 말아주세요."

        gpt_reply = ask_gpt(prompt)
        print(prompt)
        print(">> ", gpt_reply)

        try:
            selected_index = int(gpt_reply) - 1
            if 0 <= selected_index < len(kin_titles):
                entry['selected_title'] = kin_titles[selected_index]
            else:
                entry['selected_title'] = None
        except:
            entry['selected_title'] = None
        print(entry['selected_title'])

        json.dump(entry, outfile, ensure_ascii=False)
        outfile.write('\n')

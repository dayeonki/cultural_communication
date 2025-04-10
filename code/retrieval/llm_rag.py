# (2) Use LLM searcher
import openai
import json
from colbert import Searcher

openai.api_key = ''


doc_text_map = {}
with open('colbert_en_explanations.tsv') as f:
    for line in f:
        doc_id, text = line.strip().split('\t', 1)
        doc_text_map[int(doc_id)] = text

searcher = Searcher(index='definition-index')

# Load Korean terms
with open('../../data/naver_opendict_ko_official.jsonl') as f:
    korean_terms = [json.loads(line) for line in f]

with open('gpt4o_searched.jsonl', 'w') as out_f:
    for entry in korean_terms:
        ko_term = entry['word']
        ko_explanation = entry['explanation']

        query = f"What is a closest English equivalent for '{ko_term}'? It means: {ko_explanation}"
        doc_ids, _, scores = searcher.search(query, k=3)

        # Get actual text from doc ids
        retrieved_docs = []
        context = []
        for rank, (doc_id, score) in enumerate(zip(doc_ids, scores), 1):
            text = doc_text_map.get(doc_id, '[Text not found]')
            context.append(f"{rank}. {text}")
            retrieved_docs.append({
                'rank': rank,
                'doc_id': doc_id,
                'retrieved_doc': text,
                'score': score
            })

        context_block = "\n".join(context)

        rag_prompt = f"""You are an expert in understanding cross-cultural neologisms.

A Korean neologism is provided below with its explanation. You are also given 3 English definitions. Choose the one that is most semantically aligned with the Korean term. If none are appropriate, say "None of the above". 

Korean Term: {ko_term}
Meaning: {ko_explanation}

English Candidate Definitions:
{context_block}

Which one best captures the meaning of the Korean term? Only output the definition without providing any additional explanation or text.
Response: """

        print("\nPrompt:")
        print(rag_prompt)

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": rag_prompt}
            ],
            temperature=0.3
        )

        llm_answer = response['choices'][0]['message']['content'].strip()

        print("\nResponse:")
        print(llm_answer)

        result_entry = {
            'ko_term': ko_term,
            'ko_explanation': ko_explanation,
            'prompt': rag_prompt,
            'retrieved_definitions': retrieved_docs,
            'response': llm_answer
        }

        out_f.write(json.dumps(result_entry, ensure_ascii=False) + '\n')
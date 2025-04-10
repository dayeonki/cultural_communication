import json
import os


os.environ["COLBERT_LOAD_TORCH_EXTENSION"] = "False"
os.environ["CUDA_HOME"] = "/opt/common/cuda/cuda-11.8.0/bin/nvcc"

def save_definition():
    with open('../../data/neo-bench/neobench.jsonl') as f_in, open('colbert_en_explanations.tsv', 'w') as f_out:
        for i, line in enumerate(f_in):
            obj = json.loads(line)
            doc_id = str(i)  # Must be integer-like!
            definition = obj['Definition']
            clean_text = definition.strip().replace('\t', ' ')
            f_out.write(f'{doc_id}\t{clean_text}\n')


def colbert_index():
    # ColBERT indexing
    from colbert import Indexer
    from colbert.infra import Run, RunConfig, ColBERTConfig

    with Run().context(RunConfig(nranks=1, experiment="msmarco")):

        config = ColBERTConfig(
            nbits=2,
            root="indexes/",
        )
        indexer = Indexer(checkpoint='colbert-ir/colbertv2.0',
                        # index_root='indexes/',
                        # index_name='definition-index',
                        config=config
        )

        indexer.index(
            name='definition-index', 
            overwrite=True,
            collection='colbert_en_explanations.tsv'
        )


def colbert_search_ko():
    import json
    from colbert import Searcher

    doc_text_map = {}
    with open('colbert_en_explanations.tsv') as f:
        for line in f:
            doc_id, text = line.strip().split('\t', 1)
            doc_text_map[int(doc_id)] = text

    with open('../../data/naver_opendict_ko_official.jsonl') as f:
        korean_terms = [json.loads(line) for line in f]

    searcher = Searcher(index='definition-index')

    with open('colbert_ko.jsonl', 'w') as out_f:
        for entry in korean_terms:
            ko_term = entry['word']
            ko_explanation = entry['explanation']
            query = f"What is a closest English mapping to '{ko_term}', which means: {ko_explanation}?"

            print(f"\nQuery: {query}")
            doc_ids, _, scores = searcher.search(query, k=3)

            retrieved_docs = []
            for rank, (doc_id, score) in enumerate(zip(doc_ids, scores), 1):
                text = doc_text_map.get(doc_id, "[Text not found]")
                print(f"Rank {rank}: {text} (score: {score:.2f})")
                retrieved_docs.append({
                    'rank': rank,
                    'retrieved_doc': text,
                    'doc_id': doc_id,
                    'score': score
                })

            result_entry = {
                'ko_term': ko_term,
                'ko_explanation': ko_explanation,
                'query': query,
                'retrieved_docs': retrieved_docs
            }

            out_f.write(json.dumps(result_entry, ensure_ascii=False) + '\n')


def colbert_search_zh():
    import json
    from colbert import Searcher

    doc_text_map = {}
    with open('colbert_en_explanations.tsv') as f:
        for line in f:
            doc_id, text = line.strip().split('\t', 1)
            doc_text_map[int(doc_id)] = text

    with open('../../data/language_situation_official_zh.jsonl') as f:
        korean_terms = [json.loads(line) for line in f]

    searcher = Searcher(index='definition-index')

    with open('colbert_zh.jsonl', 'w') as out_f:
        for entry in korean_terms:
            zh_term = entry['word']
            zh_explanation = entry['explanatory_hint']
            query = f"What is a closest English mapping to '{zh_term}', which means: {zh_explanation}?"

            print(f"\nQuery: {query}")
            doc_ids, _, scores = searcher.search(query, k=3)

            retrieved_docs = []
            for rank, (doc_id, score) in enumerate(zip(doc_ids, scores), 1):
                text = doc_text_map.get(doc_id, "[Text not found]")
                print(f"Rank {rank}: {text} (score: {score:.2f})")
                retrieved_docs.append({
                    'rank': rank,
                    'retrieved_doc': text,
                    'doc_id': doc_id,
                    'score': score
                })

            result_entry = {
                'zh_term': zh_term,
                'zh_explanation': zh_explanation,
                'query': query,
                'retrieved_docs': retrieved_docs
            }

            out_f.write(json.dumps(result_entry, ensure_ascii=False) + '\n')


if __name__ == "__main__":
    # print("Building Dictionary!")
    # save_definition()

    # print("Indexing English meaning documents!")
    # colbert_index()

    # print("Searching for each Korean neologism!")
    # colbert_search_ko()

    print("Searching for each Chinese neologism!")
    colbert_search_zh()
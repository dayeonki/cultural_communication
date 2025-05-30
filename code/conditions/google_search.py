import json
import argparse
from serpapi import GoogleSearch


parser = argparse.ArgumentParser()
parser.add_argument('--search_mode', type=str, choices=['word', 'meaning'], default='word',
                    help="Search query mode: 'word' or 'meaning'")
args = parser.parse_args()


SERPAPI_KEY = 'f2d72e80cba77d2f57f2e5f334407d4efe40451c429b70ecea4f2874aca901cf'
TOP_K = 5
input_path = '../../data/en_neologism.jsonl'
output_path = 'res/google_search_meaning.jsonl'


results = []

with open(input_path, 'r', encoding='utf-8') as infile:
    for line in infile:
        obj = json.loads(line)
        word = obj['neologism']

        query = word if args.search_mode == 'word' else f"{word} meaning"

        search = GoogleSearch({
            "q": query,
            "api_key": SERPAPI_KEY,
            "num": TOP_K
        })

        try:
            response = search.get_dict()
            top_links = []
            if 'organic_results' in response:
                for result in response['organic_results'][:TOP_K]:
                    top_links.append({
                        'title': result.get('title'),
                        'link': result.get('link'),
                        'snippet': result.get('snippet'),
                        'thumbnail': result.get('thumbnail'),
                        'date': result.get('date'),
                        'source_name': result.get('source'),
                        'source_link': result.get('displayed_link')
                    })
            obj[f'google_search_top{TOP_K}'] = top_links
        except Exception as e:
            print(f"Error fetching results for {word}: {e}")
            obj[f'google_search_top{TOP_K}'] = []

        print(f"{word} → {len(obj[f'google_search_top{TOP_K}'])} results")
        print(obj[f'google_search_top{TOP_K}'])
        results.append(obj)


with open(output_path, 'w', encoding='utf-8') as f:
    for item in results:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

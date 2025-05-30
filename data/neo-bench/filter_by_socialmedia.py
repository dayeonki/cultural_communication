import json

input_file = 'neobench_preprocessed.jsonl'
output_twitter_file = 'neobench_twitter.jsonl'

with open(input_file, 'r') as infile, open(output_twitter_file, 'w') as outfile:
    for line in infile:
        data = json.loads(line)
        if 'source_url' in data and 'twitter' in data['source_url'].lower():
            outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

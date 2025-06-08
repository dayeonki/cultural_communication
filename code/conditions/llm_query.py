import os
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI

from llm_prompts import prompt_map

# Put the api key in .env under code/
load_dotenv("../.env")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def load_term_list(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [json.loads(line)["neologism"] for line in f]


def generate_response(user_input, instructions="", model_name="chatgpt-4o-latest"):
    response = client.responses.create(
        model=model_name,
        instructions=instructions,
        input=user_input,
    )
    return response.output_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task",
        type=str,
        choices=["trans-zh", "trans-ko", "explain"],
        default="explain",
    )
    args = parser.parse_args()
    task = args.task
    print(f"Task: # {task} #")

    prompt_temp_term = prompt_map.get(f"{task}_term", "")
    print(f"Prompt template: {prompt_temp_term}")

    input_path = "../../data/en_neologism.jsonl"
    term_list = load_term_list(input_path)
    print(f"Loaded {len(term_list)} terms from {input_path}")

    # TODO: Load social media post once they are finalized

    with open(f"res/llm_{task}_term.jsonl", "w", encoding="utf-8") as fout:
        for term in term_list:
            print(f"Processing term: {term}")
            user_input = prompt_temp_term.format(term=term)
            response = generate_response(user_input)
            print(response)
            print("-" * 80)

            fout.write(
                json.dumps(
                    {"term": term, "prompt": user_input, "response": response},
                    ensure_ascii=False,
                )
                + "\n"
            )


if __name__ == "__main__":
    main()

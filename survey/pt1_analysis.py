import json
import argparse
import pandas as pd


def count_duration():
    df['Duration'] = pd.to_timedelta(df['Duration (in seconds)'], unit='s')
    min_duration = df['Duration'].min()
    max_duration = df['Duration'].max()
    return min_duration, max_duration


def count_year():
    min_year = df['Q1'].min()
    max_year = df['Q1'].max()
    return min_year, max_year


def count_strategy():
    q3_columns = [f'{i}_Q3' for i in range(1, 26)]
    q3_values = df[q3_columns].values.ravel()
    split_values = [
        item.strip()
        for val in q3_values if pd.notna(val)
        for item in val.split(',')
    ]
    strategy_counts = pd.Series(split_values).value_counts().reset_index()
    strategy_counts.columns = ['Value', 'Count']
    return strategy_counts


def other_strategy():
    q3_other_columns = [f'{i}_Q3_7_TEXT' for i in range(1, 26)]
    q3_other_values = df[q3_other_columns].values.ravel()
    q3_other_counts = pd.Series(q3_other_values).value_counts().reset_index()
    q3_other_counts.columns = ['Comment', 'Count']
    return q3_other_counts


def count_confidence_difficulty():
    q5_confidence_cols = []
    q5_difficulty_cols = []
    q5_seen = {}

    for col in df.columns:
        if '_Q5' in col:
            q_num = col.split('_Q5')[0]
            if q_num.isdigit():
                if q_num not in q5_seen:
                    q5_seen[q_num] = 1
                    q5_confidence_cols.append(col)  # i_Q5 first = confidence
                elif q5_seen[q_num] == 1:
                    q5_seen[q_num] += 1
                    q5_difficulty_cols.append(col)  # i_Q5 second = difficulty

    confidence_values = df[q5_confidence_cols].values.ravel()
    difficulty_values = df[q5_difficulty_cols].values.ravel()

    confidence_counts = pd.Series(confidence_values).value_counts(dropna=False).reset_index()
    difficulty_counts = pd.Series(difficulty_values).value_counts(dropna=False).reset_index()

    confidence_counts.columns = ['Confidence Level', 'Count']
    difficulty_counts.columns = ['Difficulty Level', 'Count']
    return confidence_counts, difficulty_counts


def is_guess_correct(guess, correct_answer):
    # Note: by observing the data, it seems that the guess is not exactly the same as the correct answer, but might be contained
    # if guess.strip() == correct_answer.strip():
    guess = guess.replace(' ', '').lower()
    correct_answer = correct_answer.replace(' ', '').lower()
    if guess.strip() in correct_answer.strip() or correct_answer.strip() in guess.strip():
        return True
    return False


def calculate_accuracy(gold_keywords, lang):
    total = 0
    correct = 0

    for i in range(1, 26):
        if lang == 'zh' and i == 19:
            continue
        col = f'{i}_Q2'
        if col in df.columns:
            for _, guess in df[col].items():
                correct_answer = gold_keywords.get(i)
                if pd.notna(guess) and correct_answer is not None:
                    if is_guess_correct(guess, correct_answer):
                        correct += 1
                    total += 1

    accuracy = round(correct / total if total > 0 else 0, 3)
    return accuracy


def calculate_confidence_weighted_accuracy(gold_keywords, lang):
    total_score = 0
    total_entries = 0

    for i in range(1, 26):
        if lang == 'zh' and i == 19:
            continue
        guess_col = f'{i}_Q2'
        conf_col = None
        count = 0

        for col in df.columns:
            if col.startswith(f'{i}_Q5'):
                count += 1
                if count == 1:
                    conf_col = col
                    break

        if guess_col in df.columns and conf_col in df.columns:
            for idx in df.index:
                guess = df.at[idx, guess_col]
                conf_raw = df.at[idx, conf_col]
                correct_answer = gold_keywords.get(i)
                if pd.isna(guess) or pd.isna(conf_raw):
                    continue

                try:
                    conf_level = int(str(conf_raw).split(' ')[0])
                except:
                    continue

                sign = 1 if is_guess_correct(guess, correct_answer) else -1
                score = sign * (conf_level / 5)
                total_score += score
                total_entries += 1

    avg_score = round(total_score / total_entries if total_entries > 0 else 0, 3)
    return avg_score



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--language", type=str, default='ko')
    args = parser.parse_args()
    lang = args.language

    df = pd.read_csv(f'pt1_{args.language}.csv')
    with open(f"../data/{args.language}_firstbatch.jsonl", "r", encoding="utf-8") as f:
        gold_data = [json.loads(line) for line in f]
    if lang == 'ko':
        gold_keywords = {i + 1: entry['keyword'] for i, entry in enumerate(gold_data)}
    else:
        gold_keywords = {i + 1: entry['word'] for i, entry in enumerate(gold_data)}

    min_duration, max_duration = count_duration()
    min_year, max_year = count_year()
    strategies = count_strategy()
    other_strategies = other_strategy()
    confidence, difficulty = count_confidence_difficulty()
    accuracy = calculate_accuracy(gold_keywords, lang)
    confidence_weighted_accuracy = calculate_confidence_weighted_accuracy(gold_keywords, lang)

    print(f"Min Duration: {str(min_duration)}")
    print(f"Max Duration: {str(max_duration)}")
    print(f"Min Year: {min_year}")
    print(f"Max Year: {max_year}\n")
    print(f"Strategy Distribution:\n {strategies}\n")
    print(f"Other Strategies:\n {other_strategies}\n")
    print(f"Confidence Distribution:\n {confidence}\n")
    print(f"Difficulty Distribution:\n {difficulty}\n")
    print(f"Accuracy: {accuracy}")
    print(f"Confidence-weighted Accuracy: {confidence_weighted_accuracy}")
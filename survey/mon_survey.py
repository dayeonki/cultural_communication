import json


def read_meanings_from_jsonl(jsonl_file):
    meanings = []
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            meanings.append(data.get("description", "Unknown meaning"))
    return meanings


def generate_advanced_txt(filename, jsonl_file):
    meanings = read_meanings_from_jsonl(jsonl_file)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("[[AdvancedFormat]]\n\n")
        f.write("[[ED:State]]\n")
        f.write("[[ED:Gender]]\n")
        f.write("[[ED:SawSurvey:1]]\n\n")
        
        for i, meaning in enumerate(meanings, start=1):
            f.write(f"[[Block:MC Block {i}]]\n\n")
            
            # Question 1 - Free Text Entry
            f.write("[[Question:TE:SingleLine]]\n")
            f.write(f"The meaning of a neologism is \"{meaning}\". Can you guess the neologism?\n\n")
            
            # Question 2 - Multiple Choice, Multi Select
            f.write("[[Question:MC:MultiSelect]]\n")
            f.write("What strategies did you use to guess the neologism?\n")
            f.write("[[Choices]]\n")
            f.write("I did not use any strategies / I'm not sure if I used any strategies / I went with my intuition.\n")
            f.write("I recalled my past memories of communicating with this term.\n")
            f.write("I asked my friends around.\n\n")
            
            # Question 3 - Single Choice, Single Select
            f.write("[[Question:MC:SingleAnswer]]\n")
            f.write("How confident are you in your guess? Rate in a scale from 1 (Very unconfident) to 5 (Very confident).\n")
            f.write("[[Choices]]\n")
            confidence_labels = [
                "1 (Very Unconfident)",
                "2 (Unconfident)",
                "3 (Neutral)",
                "4 (Confident)",
                "5 (Very Confident)"
            ]
            for label in confidence_labels:
                f.write(f"{label}\n")
            f.write("\n")
            
            # Question 4 - Single Choice, Single Select
            f.write("[[Question:MC:SingleAnswer]]\n")
            f.write("In the past month, how often did you use this temr in your daily work and life? Rate in a scale from 1 (Never) to 5 (Always).\n")
            f.write("[[Choices]]\n")
            frequency_labels = [
                "Never (Never in the past month)",
                "Rarely (Fewer than once a week)",
                "Sometimes (Two or three times a week)",
                "Often (More than three times a week, but not every day)",
                "Always (Almost everyday)"
            ]
            for label in frequency_labels:
                f.write(f"{label}\n")
            f.write("\n")
            
            f.write("[[PageBreak]]\n\n")


generate_advanced_txt("test.txt", "test.jsonl")

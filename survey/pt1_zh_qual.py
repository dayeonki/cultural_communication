import pandas as pd

zh_responses = pd.read_csv('pt1_zh.csv')

question_temp_keys = ['#_Q1', '#_Q2', '#_Q5', '#_Q3', '#_Q3_7_TEXT', '#_Q4', '#_Q5', '#_Q6']
# selected_keys = ['#_Q6']
# selected_keys = ['#_Q3_7_TEXT']
selected_keys = ['#_Q4']
for row in zh_responses.iterrows():
    for i in range(1, 26):
        for key in selected_keys:
            question_key = key.replace('#', str(i))
            if type(row[1][question_key]) == str:
                print(row[1][question_key])

# 1_Q1 (guess or not)	1_Q2 (guess)	1_Q5 (confidence)	1_Q3 (strategy)	1_Q3_7_TEXT (other)	1_Q4 (extra help)	1_Q5 (difficulty)	1_Q6 (blocker)

# Q6 (blocker)
# the prompt is not enough (not specific, missing context)
# context matters
# not sure if the word is neologism
# actively use OR passively learn
# not familiar with the field
# feel the desc is not accurate enough (so multiple words are guessed)
# feel familiar but tip-of-the-tongue

# Q3_7 (Other strategies)
# not familiar with the scenario when it is used; not exposed by social media
# the meaning might be confusing

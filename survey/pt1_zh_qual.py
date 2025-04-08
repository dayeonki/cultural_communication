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

# Other Strategies:
# 0                                          搜了小红书      3
# 1                                        根据提供的含义      2
# 2                            不熟悉使用场景&没刷到过，所以无从入手      1
# 3                           新词？我感觉我知道的词都不新了怎么办。。      1
# 4                                           照抄题干      1
# 5                                             编的      1
# 6                                   我回忆我遇到这个词的场景      1
# 7                                刷到过，但是没有留意具体的说法      1
# 8                          绝对看到听到过，一时想不起来具体的说法。。      1
# 9                                     原来如此 是甘蔗渣啊      1
# 10  甘蔗男有点干扰思路，但是又确实提示到了（没有这个提示我会想，是不是有更具体的词我不知道）      1
# 11                                     没猜，根据提示推断      1
# 12                         从事劳动是什么意思。。下地劳动回家种田吗？      1
# 13                               没猜到但是如果说了我应该知道？      1
# 14                     是 狗？吗。。（不觉得算“猜到”，更像是瞎猜猜看）      1
# 15                     其实没有用到，只是看到（刷了太多冰墩墩的视频。。）      1
# 16               从发音入手想的，如果没有发音的提示其实我没法想出来哪怕其实知道      1
# 17                                       前面的题出现过      1

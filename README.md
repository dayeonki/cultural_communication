# Cross-Cultural Communication Project
**Owner:** Zoey Ki, Hope Hou


### [1] Collecting Neologisms + Meanings
- ko: NAVER Opensource Dictionary (filtered to only use terms from official neologism dictionary)
- zh-1: "Language Situation in China" 2019-2022 (in total 948 unique words where 6 words have two meanings; 1 word 卷 has three meanings; 98 words are marked as explicit Internet slang; some words contain placeholders xxx)
- zh-2: "Word-Splitting" 2015-2024 [link](https://docs.google.com/spreadsheets/d/1XeVljZ-ObGPoA9jepgwAoz1jX-3Y5OPpzZ0P7_zdVco) (in total 100 words but not all slangs)
- ko+zh: Gold mapping from Chinatogod website [link](http://www.chinatogod.com/main/z2_search_.php?si=0&all_search=%BD%C5%C1%B6%BE%EE%B7%CE)


### [2] Annotation Exercise 1 (with ko/zh natives)
**[Phase 1]**
- **Procedure:** Given meaning, ask for neologism
- **Goal:** Using the default meaning, can the source language natives can recover/guess back the neologism
    - If yes, use the default meaning as it is
    - If no, expand the meaning
- Ask in the survey about "how to improve the description?"
- Maybe we can give out the annotation exercise, ask them to complete in a longer time span, ask to provide feedback on which strategies you used to figure out the neologism

**[Phase 2]**
- **Procedure:** Given meaning, ask for connotation + verify meaning (any expanded meaning)
- **How to ask connotation?:** Give specific/realistic scenario (e.g., Would you use this term to appraise or criticize something/someone?)


### Retrieval
1. ColBERT retrieval: `code/retrieval/colbert_rag.py`
2. LLM retrieval: `code/retrieval/llm_rag.py`

- Results are saved in `retrieval_results/...`


### Survey response analysis
- Run `python survey/pt1_analysis.py --language $LANGUAGE` by replacing $LANGUAGE with ko or zh.
- Example output:

```
Min Duration: 0 days 00:09:17
Max Duration: 0 days 06:56:16
Min Year: 1993
Max Year: 2001

Strategy Distribution:
                                                Value  Count
0  I did not use any strategies / I'm not sure if...    211
1  I recalled my past memories of communicating u...     99
2  I recalled similar-sounding or similarly struc...     85
3                                             Others     16
4                   I searched online (e.g. Google).      7
5                         I asked my friends around.      2
6  I asked AI tools to help me guess the neologis...      1

Other Strategies:
                     Comment  Count
0                        모름      7
1                       여친임      1
2  전 여친이 있어서 저 말의 의미를 모르겠어요      1
3        문제가 무슨 말인줄 모르겠어요 ㅠ      1
4                뉴스에서 언뜻 본듯      1
5                 최근 한국에서 봄      1

Confidence Distribution:
        Confidence Level  Count
0                   NaN    112
1    5 (Very confident)     67
2         4 (Confident)     63
3           3 (Neutral)     35
4       2 (Unconfident)     31
5  1 (Very unconfident)     17

Difficulty Distribution:
             Difficulty Level  Count
0                   4 (Hard)     89
1                   2 (Easy)     67
2              1 (Very easy)     62
3              5 (Very hard)     57
4  3 (Neither easy nor hard)     50

Accuracy: 0.413
Confidence-weighted Accuracy: -0.076
```
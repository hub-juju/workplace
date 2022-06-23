from prcd import *
import csv
import streamlit as st
from collections import Counter

moral_result = pd.read_excel("moral_result.xlsx", index_col= 0)
file = open("lex.csv", encoding = "utf-8")
moral = csv.reader(file)
rows = []
for row in moral:
    rows.append(row)

# 1이 단어, 4가 moral 1, 13이 moral 10
# True, False로 구분해놓은 csv 파일 불러다가 10개의 사전을 따로 만든 겁니다.
# 반복문 돌리기 쉽게 하려고 total에다가 모아뒀습니다.
# total[0]은 care 사전, total[1]은 harm 사전, ... 이런 식입니다.

care = []
harm = []
fair = []
cheat = []
loyal = []
betray = []
auth = []
subvert = []
sanc = []
dero = []
total = [care, harm, fair, cheat, loyal, betray, auth,subvert, sanc, dero]

for row in rows:
    for i in range(4,14):
        if row[i] == "TRUE":
            total[i-4].append(row[1])

def moral_find(data, lexicon):
    from collections import Counter
    targets = []
    match = []
    outcome = []
    for i in data:  # 개별 기사
        for j in i:  # 개별 튜플 ('단어', '품사')
            targets.append(j[0])

    for i in lexicon:
        res = []
        for word in targets:
            if word in i:
                res.append(word)
        outcome.append(res)

    return outcome

r_a_moral = moral_find(r_a_words, total)
r_c_moral = moral_find(r_c_words, total)
l_a_moral = moral_find(l_a_words, total)
l_c_moral = moral_find(l_c_words, total)
dp_moral = moral_find(dp_words, total)
pp_moral = moral_find(pp_words, total)
han_moral = moral_find(han_words, total)

def moral_detail (text, moral_num) :
    st.markdown("선택하신 도덕기반에 속하는")
    st.write("단어 개수는 " + str(len(text[moral_num])) + "개 입니다")
    counts= Counter(text[moral_num])
    # print(counts) # 정확히 어떤 단어들이 잡혔는지 보려면
    table = pd.DataFrame(columns = ["등장단어", "등장횟수"])
    table["등장단어"] = list(counts.keys())
    table["등장횟수"] = list(counts.values())
    st.dataframe(table.sort_values(by=["등장횟수"], axis=0, ascending=False)) # 정확히 어떤 단어들이 잡혔는지 dataframe으로 보여줌
    return(table)
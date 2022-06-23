import pandas as pd
from konlpy.tag import Komoran
tagger = Komoran()

c_a = pd.read_excel("chosun_contents.xlsx")
c_c = pd.read_excel("chosun_comments.xlsx")
j_a = pd.read_excel("joongang_contents.xlsx")
j_c = pd.read_excel("joongang_comments.xlsx")
h_a = pd.read_excel("hani_contents.xlsx")
h_c = pd.read_excel("hani_comments.xlsx")
k_a = pd.read_excel("kyunghyang_contents.xlsx")
k_c_np = pd.read_excel("kyunghyang_nonpolitics_comments.xlsx")
k_c_p = pd.read_excel("kyunghyang_politics_comments.xlsx")

# 데이터 클리닝
r_a = []
for i in c_a.iloc:
    r_a.append(i[0])
for i in j_a.iloc:
    r_a.append(i[0])
l_a = []
for i in h_a.iloc:
    l_a.append(i[0])
for i in k_a.iloc:
    l_a.append(i[0])
r_c = []
for i in c_c.iloc:
    for j in i:
        if type(j) == str:
            r_c.append(j)
for i in j_c.iloc:
    for j in i:
        if type(j) == str:
            r_c.append(j)
l_c = []
for i in h_c.iloc:
    for j in i:
        if type(j) == str:
            l_c.append(j)
for i in k_c_np.iloc:
    for j in i:
        if type(j) == str:
            l_c.append(j)
for i in k_c_p.iloc:
    for j in i:
        if type(j) == str:
            l_c.append(j)

#청문회 데이터
f = open("hearing.txt", encoding = 'utf-8')
lines = f.readlines()
sep = []
for i in lines:
    sep.append(i.split("\t"))
dp = []
pp = []
han = []
for i in sep:
    if i[0] == "더불어민주당":
        dp.append(i[3])
    elif i[0] == "국민의힘":
        pp.append(i[3])
    elif i[2] == "한동훈":
        han.append(i[3])

def get_words(texts):
    tagged_texts = []
    for text in texts:
        try:
            tagged_texts.append(tagger.pos(text))
        except:
            pass
    return (tagged_texts)

# 하나의 스트링으로(유사도분석용)
r_a_str = ' '.join(r_a)
l_a_str = ' '.join(l_a)
r_c_str = ' '.join(r_c)
l_c_str = ' '.join(l_c)
dp_str = ' '.join(dp)
pp_str = ' '.join(pp)
han_str = ' '.join(han)

# 형태소분석해서 단어 나누기
r_a_words = get_words(r_a)  # 보수기사
r_c_words = get_words(r_c)  # 보수댓글
l_a_words = get_words(l_a)  # 진보기사
l_c_words = get_words(l_c)  # 진보댓글
dp_words = get_words(dp)
pp_words = get_words(pp)
han_words = get_words(han)






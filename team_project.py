# 시작하기 전, "streamlit run team_project.py"
# 참고자료
# * API Document: https://docs.streamlit.io/library/api-reference
# * Examples: https://github.com/MarcSkovMadsen/awesome-streamlit

#모듈불러오기
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import tensorflow
import sklearn
from PIL import Image
import pyLDAvis
import pyLDAvis.gensim_models
import seaborn as sns

#데이터 불러오기
c_a = pd.read_excel("chosun_contents.xlsx")
c_c = pd.read_excel("chosun_comments.xlsx")
j_a = pd.read_excel("joongang_contents.xlsx")
j_c = pd.read_excel("joongang_comments.xlsx")
h_a = pd.read_excel("hani_contents.xlsx")
h_c = pd.read_excel("hani_comments.xlsx")
k_a = pd.read_excel("kyunghyang_contents.xlsx")
k_c_np = pd.read_excel("kyunghyang_nonpolitics_comments.xlsx")
k_c_p = pd.read_excel("kyunghyang_politics_comments.xlsx")
moral_result = pd.read_excel("moral_result.xlsx", index_col= 0)


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
        
# 데이터 합치기
r_a_str = ' '.join(r_a)
l_a_str = ' '.join(l_a)
r_c_str = ' '.join(r_c)
l_c_str = ' '.join(l_c)
민주당발언 = ' '.join(dp)
국민의힘발언 = ' '.join(pp)
한동훈발언 = ' '.join(han)

# 코사인유사도
def cos_sim(text1, text2):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    tv = TfidfVectorizer()
    sents = (text1, text2)
    tfidf_matrix = tv.fit_transform(sents)
    st.write(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2]))

# 형태소분석
from konlpy.tag import Komoran
tagger = Komoran()
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
import networkx as nx 

stop_words = ['DB','다음', '위원장', '위원', '의원', '간사', '국회','PPT', '잠깐', '잠깐만', '잠깐만요', '후보자', '청문', '청문회', '인사청문회', '위원회','법무부', '장관', '한동훈', '최근','오후','오전','오늘','이날','이후','그것','그때','지금','당장','당시','이번','이제','이건','이것','이거','여기','거기','경우','정도','어디','저희','제가','저것','우리', '진행', '질의', '협의', '합의','회의','정회','의결','자료','관련','얘기','말씀','발언','생각','위원','문제','질문','답변','정회','이상','이제','이다','있다','여러분','연합뉴스','뉴스1','경향신문','한겨레','!!!','!!','라고','보니','동안','요즘','최고','제일','니들','너희','부분','내용','본인','자신','자기','드릴','만약','\n','\t','\r','♥' ,'α' , '■','▶','▲','/','+' ,'-','*','"',',','(',')','○',':','?','!!','!!!','!','.','[',']','…']

# 데이터 전처리
import re 

RE_EMOJI=re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)

def strip_emoji(text):
    return RE_EMOJI.sub(r'', text)

SW=['DB','다음', '위원장', '위원', '의원', 'PPT', '예', '잠깐', '잠깐만', '잠깐만요', '후보자', '청문','청문회', '인사청문회', '법무부', '장관', '한동훈', '오후', '이날', '말씀', '그것', '제가','우리', '진행', '질의', '합의','정회','자료','관련','얘기','생각','\n','\t','\r','♥' ,'α' , '■','▶','▲','/','+' ,'-','*','"',',','(',')','○',':','?','!!','!!!','!','.','[',']','…']

# @st.cache
# def get_noun(texts):
#     tagged_texts = []
#     for text in texts:
#         try:
#             tagged_texts.append(tagger.pos(text))
#         except:
#             pass
        
#     new_list = []
#     for i in tagged_texts:
#         for word, tag in i:
#             if tag in ["NNG", "NNP", "NP"]:
#                 new_list.append(word)
#             #elif tag in ["VV", "VA"]:
#                 #new_list.append(word+"다")
    
#     return(new_list)
                
# #명사뭉치
# r_a_noun = get_noun(r_a)
# r_c_noun = get_noun(r_c)
# l_a_noun = get_noun(l_a)
# l_c_noun = get_noun(l_c)
# dp_noun = get_noun(dp)
# pp_noun = get_noun(pp)
# han_noun = get_noun(han)

# # 필터링
# def filtering(noun_list):
#     filtered_list = []
#     for i in noun_list:
#         if i not in SW and len(i)>1:
#             filtered_list.append(i)
#     filtered_list = [strip_emoji(s) for s in filtered_list]
#     filtered_list = [t.replace('수완','검수완박').replace('남국','김남국').replace('김경', '김경율').replace('최강', '최강욱') for t in filtered_list]
    
#     return(filtered_list)

# r_a_filtered = filtering(r_a_noun)
# r_c_filtered = filtering(r_c_noun)
# l_a_filtered = filtering(l_a_noun)
# l_c_filtered = filtering(l_c_noun)
# dp_filtered = filtering(dp_noun)
# pp_filtered = filtering(pp_noun)
# han_filtered = filtering(han_noun)

# chunks
# r_a_chunks = [r_a_filtered[x:x+100] for x in range(0, len(r_a_filtered), 100)]
# r_c_chunks = [r_c_filtered[x:x+100] for x in range(0, len(r_c_filtered), 100)]
# l_a_chunks = [l_a_filtered[x:x+100] for x in range(0, len(l_a_filtered), 100)]
# l_c_chunks = [l_c_filtered[x:x+100] for x in range(0, len(l_c_filtered), 100)]
# dp_chunks = [dp_filtered[x:x+100] for x in range(0, len(dp_filtered), 100)]
# pp_chunks = [pp_filtered[x:x+100] for x in range(0, len(pp_filtered), 100)]
# han_chunks = [han_filtered[x:x+100] for x in range(0, len(han_filtered), 100)]

#토픽모델링 분석시작
# from gensim import corpora 
# from gensim import models
# from gensim.models import word2vec
# from gensim.models import LdaModel

# r_a_dictionary = corpora.Dictionary(r_a_chunks)
# r_a_corpus = [r_a_dictionary.doc2bow(text) for text in r_a_chunks] 

# r_c_dictionary = corpora.Dictionary(r_c_chunks)
# r_c_corpus = [r_c_dictionary.doc2bow(text) for text in r_c_chunks] 

# l_a_dictionary = corpora.Dictionary(l_a_chunks)
# l_a_corpus = [l_a_dictionary.doc2bow(text) for text in l_a_chunks] 

# l_c_dictionary = corpora.Dictionary(l_c_chunks)
# l_c_corpus = [l_c_dictionary.doc2bow(text) for text in l_c_chunks] 

# dp_dictionary = corpora.Dictionary(dp_chunks)
# dp_corpus = [dp_dictionary.doc2bow(text) for text in dp_chunks] 

# pp_dictionary = corpora.Dictionary(pp_chunks)
# pp_corpus = [pp_dictionary.doc2bow(text) for text in pp_chunks] 

# han_dictionary = corpora.Dictionary(han_chunks)
# han_corpus = [han_dictionary.doc2bow(text) for text in han_chunks] 

# #LDA 모델
# r_a_ldamodel =models.ldamodel.LdaModel(r_a_corpus, num_topics=5, id2word=r_a_dictionary, passes=20) #3 
# r_c_ldamodel =models.ldamodel.LdaModel(r_c_corpus, num_topics=6, id2word=r_c_dictionary, passes=20) #3
# l_a_ldamodel =models.ldamodel.LdaModel(l_a_corpus, num_topics=6, id2word=l_a_dictionary, passes=20) #7
# l_c_ldamodel =models.ldamodel.LdaModel(l_c_corpus, num_topics=7, id2word=l_c_dictionary, passes=20) #8
# dp_ldamodel =models.ldamodel.LdaModel(dp_corpus, num_topics=7, id2word=dp_dictionary, passes=20) #9
# pp_ldamodel =models.ldamodel.LdaModel(pp_corpus, num_topics=4, id2word=pp_dictionary, passes=20) #9
# han_ldamodel =models.ldamodel.LdaModel(han_corpus, num_topics=8, id2word=han_dictionary, passes=20) #7

# # perplexity
# import matplotlib.pyplot as plt

# @st.cache
# def perplexity_value(dictionary, corpus, ldamodel):
#     perplexity = []
#     for i in range(2,10):
#         ldamodel = models.ldamodel.LdaModel(corpus, num_topics=i, id2word=dictionary, passes=20)
#         perplexity.append(ldamodel.log_perplexity(corpus))
#     return(perplexity)

# r_a_perplexity = perplexity_value(r_a_dictionary, r_a_corpus, r_a_ldamodel)
# r_c_perplexity = perplexity_value(r_c_dictionary, r_c_corpus, r_c_ldamodel)
# l_a_perplexity = perplexity_value(l_a_dictionary, l_a_corpus, l_a_ldamodel)
# l_c_perplexity = perplexity_value(l_c_dictionary, l_c_corpus, l_c_ldamodel)
# dp_perplexity = perplexity_value(dp_dictionary, dp_corpus, dp_ldamodel)
# pp_perplexity = perplexity_value(pp_dictionary, pp_corpus, pp_ldamodel)
# han_perplexity = perplexity_value(han_dictionary, han_corpus, han_ldamodel)

# # coherence
# import matplotlib.pyplot as plt
# from gensim.models import CoherenceModel

# r_a_coherence = []
# for i in range(2, 10):
#     r_a_ldamodel = models.ldamodel.LdaModel(r_a_corpus, num_topics=i, id2word=r_a_dictionary, passes=20)
#     coherence_model_lda = CoherenceModel(model=r_a_ldamodel, texts=r_a_chunks, dictionary=r_a_dictionary, topn=10)
#     coherence_lda = coherence_model_lda.get_coherence()
#     r_a_coherence.append(coherence_lda)

# r_c_coherence = []
# for i in range(2, 10):
#     r_c_ldamodel = models.ldamodel.LdaModel(r_c_corpus, num_topics=i, id2word=r_c_dictionary, passes=20)
#     coherence_model_lda = CoherenceModel(model=r_c_ldamodel, texts=r_c_chunks, dictionary=r_c_dictionary, topn=10)
#     coherence_lda = coherence_model_lda.get_coherence()
#     r_c_coherence.append(coherence_lda)
    
# l_a_coherence = []
# for i in range(2, 10):
#     l_a_ldamodel = models.ldamodel.LdaModel(l_a_corpus, num_topics=i, id2word=l_a_dictionary, passes=20)
#     coherence_model_lda = CoherenceModel(model=l_a_ldamodel, texts=l_a_chunks, dictionary=l_a_dictionary, topn=10)
#     coherence_lda = coherence_model_lda.get_coherence()
#     l_a_coherence.append(coherence_lda)
    
# l_c_coherence = []
# for i in range(2, 10):
#     l_c_ldamodel = models.ldamodel.LdaModel(l_c_corpus, num_topics=i, id2word=l_c_dictionary, passes=20)
#     coherence_model_lda = CoherenceModel(model=l_c_ldamodel, texts=l_c_chunks, dictionary=l_c_dictionary, topn=10)
#     coherence_lda = coherence_model_lda.get_coherence()
#     l_c_coherence.append(coherence_lda)
    
# dp_coherence = []
# for i in range(2, 10):
#     dp_ldamodel = models.ldamodel.LdaModel(dp_corpus, num_topics=i, id2word=dp_dictionary, passes=20)
#     coherence_model_lda = CoherenceModel(model=dp_ldamodel, texts=dp_chunks, dictionary=dp_dictionary, topn=10)
#     coherence_lda = coherence_model_lda.get_coherence()
#     dp_coherence.append(coherence_lda)
    
# pp_coherence = []
# for i in range(2, 10):
#     pp_ldamodel = models.ldamodel.LdaModel(pp_corpus, num_topics=i, id2word=pp_dictionary, passes=20)
#     coherence_model_lda = CoherenceModel(model=pp_ldamodel, texts=pp_chunks, dictionary=pp_dictionary, topn=10)
#     coherence_lda = coherence_model_lda.get_coherence()
#     pp_coherence.append(coherence_lda)

# han_coherence = []
# for i in range(2, 10):
#     han_ldamodel = models.ldamodel.LdaModel(han_corpus, num_topics=i, id2word=han_dictionary, passes=20)
#     coherence_model_lda = CoherenceModel(model=han_ldamodel, texts=han_chunks, dictionary=han_dictionary, topn=10)
#     coherence_lda = coherence_model_lda.get_coherence()
#     han_coherence.append(coherence_lda)

# 네트워크 분석 함수
def net(texts, co_oc):
    from IPython.display import display, HTML
    from pyvis import network as net
    tagged_texts = []
    for text in texts:
        try:
            tagged_texts.append(tagger.pos(text))
        except:
            pass
    new_list = []
    for i in tagged_texts:
        for word, tag in i:
            if tag in ["NNG", "NNP","NP"] and len(word) > 1 and word not in stop_words:
                new_list.append(word)
#             elif tag in ["VV", "VA"]:
#                 new_list.append(word+"다")
    new_list = [t.replace('수완','검수완박').replace('남국','김남국').replace('김경', '김경율').replace('김경율률', '김경율').replace('최강', '최강욱').replace('송기','송기헌').replace('광우','광우병').replace('선인','당선인').replace('기득', '기득권').replace('사권','수사권').replace('법제사','법사위').replace('구체','구체적').replace('원내','원내대표').replace('법무','법무부') for t in new_list]
    unique_words = set(new_list)
    unique_words = list(unique_words)
    word_index = {word: i for i, word in enumerate(unique_words)}
    occurs = np.zeros([len(tagged_texts), len(unique_words)])

    for i, sent in enumerate(tagged_texts):
        sub_list = []
        for word, tag in sent:
            if tag in ["NNG", "NNP","NP"] and len(word) > 1 and word not in stop_words:
                sub_list.append(word)
        sub_list = [t.replace('수완','검수완박').replace('남국','김남국').replace('김경', '김경율').replace('김경율률', '김경율').replace('최강', '최강욱').replace('송기','송기헌').replace('광우','광우병').replace('선인','당선인').replace('기득', '기득권').replace('사권','수사권').replace('법제사','법사위').replace('구체','구체적').replace('원내','원내대표').replace('법무','법무부') for t in sub_list]
        for sub in sub_list:
            index = word_index[sub]
            occurs[i][index] = 1
#             elif tag in ["VV", "VA"]:
#                 index = word_index[word+"다"]
#                occurs[i][index] = 1
    co_occurs = occurs.T.dot(occurs)
    graph = net.Network(height='1000px', width='50%',heading='')
    graph.set_options("""
    const options = {
      "nodes": {
       "borderWidth": null,
       "borderWidthSelected": 4,
       "opacity": 1,
       "font": {
         "size": 15,
         "strokeWidth": 7
       },
       "size": 16
      },
      "edges": {
        "hoverWidth": 1.1,
        "physics": false,
        "scaling": {
          "min": 6,
          "max": 20,
              "label": {
                "min": null,
                "max": null,
                "maxVisible": 50,
                "drawThreshold": null
              }
        },
        "selectionWidth": 1.8,
        "selfReferenceSize": 28,
        "selfReference": {
          "size": 28,
          "angle": 1.5707963267949
        },
        "smooth": false
      }
    }""")
#    graph.show_buttons(filter_=['physics'])
#    graph.show_buttons(filter_=['nodes'])
#    graph.show_buttons(filter_=['edges'])
    for i in range(len(unique_words)):
        for j in range(i + 1, len(unique_words)):
            if co_occurs[i][j] > co_oc:
                graph.add_node(unique_words[i])
                graph.add_node(unique_words[j])
                graph.add_edge(unique_words[i], unique_words[j])
    
    graph.show('example.html')
    display(HTML('example.html'))


# 도덕기반사전 - 형태소로 텍스트 쪼개기 함수
@st.cache
def get_words(texts):
    tagged_texts = []
    for text in texts:
        try:
            tagged_texts.append(tagger.pos(text))
        except:
            pass
        
#     new_list = []
#     for i in tagged_texts:
#         for word, tag in i:
#             if tag in ["IC", "MAG", "MAJ", "MM", "NN", "NP", "NR", "VA", "VV", "VX", "XR"]:
#                 new_list.append(i)
    
    return(tagged_texts)


r_a_words = get_words(r_a) #보수기사
r_c_words = get_words(r_c) #보수댓글
l_a_words = get_words(l_a) #진보기사
l_c_words = get_words(l_c) #진보댓글
dp_words = get_words(dp)
pp_words = get_words(pp)
han_words = get_words(han)

#도덕기반사전
import csv
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
    

@st.cache
def moral_find(data, lexicon) :
    from collections import Counter
    targets = []
    match = []
    outcome = []
    for i in data: #개별 기사
        for j in i: #개별 튜플 ('단어', '품사')
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

# 제목
st.markdown("<h1 style='text-align: center'>TEAM 1</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center'>인사청문회와 언론보도, 댓글에 대한 탐색적 연구</h3>", unsafe_allow_html=True)

#사이드바
side = st.sidebar.radio('Result',["INTRO","청문회데이터","언론보도", "댓글"])
if side == "INTRO" :
    st.header("INTRO")
    st.write("인사청문회와 관련된 개념적, 정치학적 논의")

#청문회데이터 페이지
elif side == '청문회데이터' :
    st.header("청문회데이터") 
    options = st.multiselect("코사인 유사도를 보고 싶은 2가지를 고르세요", ["민주당발언", "한동훈발언", "국민의힘발언"])
    d = []
    try : 
        for i in options :
            if i == "민주당발언" :
                a = 민주당발언
                d.append(a)
            elif i == "한동훈발언" :
                b = 한동훈발언
                d.append(b)
            elif i == "국민의힘발언" :
                c = 국민의힘발언
                d.append(c)
        cos_sim(d[0], d[1])
    except :
        st.write ("현재", len(options), "개를 고르셨습니다.", " 2개를 골라주세요")   
    
    st.markdown("***")
    
    col1, col2, col3 = st.columns(3)
    with col1 :
        st.markdown("<h3 style='text-align: center; background-color:blue;'>더불어민주당</h3>", unsafe_allow_html=True)
        
        st.markdown("**🟡워드클라우드**")
        st.image("민주발언 wc.png")
        
        st.markdown("**🟡언어네트워크**")
        st.write("공출현수치 10 이상인 단어만 표시됩니다")
        st.write("아래 버튼을 눌러주세요")
        click = st.button("민주당 언어네트워크")
        if click : net(dp, 10)
        
        # st.markdown("* 토픽모델링")
        # if st.button('pyLDAvis 보기'):
        #     with st.spinner('Creating pyLDAvis Visualization ...'):
        #         dp_vis = pyLDAvis.gensim_models.prepare(r_a_ldamodel, r_a_corpus, r_a_dictionary, mds='mmds')
        #         py_lda_vis_html = pyLDAvis.prepared_data_to_html(dp_vis)
        
        st.markdown("**🟡도덕기반사전**")
        
        plot_1 = sns.barplot(x= moral_result.index, y=moral_result["민주발언"], data = moral_result)
        plot_1.set_ylabel("단어개수")
        plot_1.figure.savefig('plot_1.png')
        plt.rcParams['font.family'] = 'NanumGothic'
        st.image("plot_1.png")
               
        selected_moral = st.selectbox('민주당 도덕기반 선택', ["보살핌", "가해", "공정", "부정", "충성", "배반", "권위", "전복", "순수", "타락"])
        moral_dic = {"보살핌" : 0, "가해" : 1, "공정": 2, "부정": 3 , "충성":4 , "배반":5 , "권위":6 , "전복":7 , "순수":8 , "타락":9}
        moral_detail(dp_moral, moral_dic["{}".format(str(selected_moral))])


        
        
    with col2 :
        st.markdown("<h3 style='text-align: center; background-color:red;'>국민의힘</h3>", unsafe_allow_html=True)
        
        st.markdown("**🟡워드클라우드**")
        st.image("국힘발언 wc.png")
        
        st.markdown("**🟡언어네트워크**")
        st.write("공출현수치 10 이상인 단어만 표시됩니다")
        st.write("아래 버튼을 눌러주세요")
        click = st.button("국민의힘 언어네트워크")
        if click : net(pp, 10)
        
        # st.markdown("* 토픽모델링")
        # if st.button('pyLDAvis 보기'):
        #     with st.spinner('Creating pyLDAvis Visualization ...'):
        #         dp_vis = pyLDAvis.gensim_models.prepare(r_a_ldamodel, r_a_corpus, r_a_dictionary, mds='mmds')
        #         py_lda_vis_html = pyLDAvis.prepared_data_to_html(dp_vis)
        
        st.markdown("**🟡도덕기반사전**")
        plot_2 = sns.barplot(x= moral_result.index, y=moral_result["국힘발언"], data = moral_result)
        plot_2.set_ylabel("단어개수")
        plot_2.figure.savefig('plot_2.png')
        plt.rcParams['font.family'] = 'NanumGothic'
        st.image("plot_2.png")
        
        selected_moral = st.selectbox('국민의 힘 도덕기반선택', ["보살핌", "가해", "공정", "부정", "충성", "배반", "권위", "전복", "순수", "타락"])
        moral_dic = {"보살핌" : 0, "가해" : 1, "공정": 2, "부정": 3 , "충성":4 , "배반":5 , "권위":6 , "전복":7 , "순수":8 , "타락":9}
        moral_detail(pp_moral, moral_dic["{}".format(str(selected_moral))])        
        
    with col3 :
        st.markdown("<h3 style='text-align: center; background-color:gray'>한동훈</h3>", unsafe_allow_html=True)
        st.markdown("**🟡워드클라우드**")
        st.image("한동훈 발언 wc.png")
        
        st.markdown("**🟡언어네트워크**")
        st.write("공출현수치 10 이상인 단어만 표시됩니다")
        st.write("아래 버튼을 눌러주세요")
        click = st.button("한동훈 언어네트워크")
        if click : net(han, 10)
        
        st.markdown("**🟡도덕기반사전**")
        plot_3 = sns.barplot(x= moral_result.index, y=moral_result["한동훈"])
        plot_3.set_ylabel("단어개수")
        plot_3.figure.savefig('plot_3.png')
        plt.rcParams['font.family'] = 'NanumGothic'
        st.image("plot_3.png")
        
        selected_moral = st.selectbox('한동훈 도덕기반선택', ["보살핌", "가해", "공정", "부정", "충성", "배반", "권위", "전복", "순수", "타락"])
        moral_dic = {"보살핌" : 0, "가해" : 1, "공정": 2, "부정": 3 , "충성":4 , "배반":5 , "권위":6 , "전복":7 , "순수":8 , "타락":9}
        moral_detail(han_moral, moral_dic["{}".format(str(selected_moral))])        


elif side == '언론보도' :
    st.header("언론보도 데이터") 
    col1, col2 = st.columns(2)
    
    with col1 :
        st.markdown("<h3 style='text-align: center; background-color:red;'>보수언론 (조선, 동아일보)</h3>", unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown("**🟡워드클라우드**")
        st.image("보수기사 wc.png")
        
        st.markdown("**🟡언어네트워크**")
        st.write("공출현수치 30 이상인 단어만 표시됩니다")
        st.write("아래 버튼을 눌러주세요")
        click = st.button("보수언론 언어네트워크")
        if click : net(r_a, 30)
        
        
        st.markdown("**🟡도덕기반사전**")
        
        news_plot2 = sns.barplot(x= moral_result.index, y=moral_result["보수기사"], data = moral_result)
        news_plot2.set_ylabel("단어개수")
        news_plot2.figure.savefig('news_plot2.png')
        plt.rcParams['font.family'] = 'NanumGothic'
        st.image("news_plot2.png")
               
        selected_moral = st.selectbox('보수언론 도덕기반 선택', ["보살핌", "가해", "공정", "부정", "충성", "배반", "권위", "전복", "순수", "타락"])
        moral_dic = {"보살핌" : 0, "가해" : 1, "공정": 2, "부정": 3 , "충성":4 , "배반":5 , "권위":6 , "전복":7 , "순수":8 , "타락":9}
        moral_detail(r_a_moral, moral_dic["{}".format(str(selected_moral))])

    
    with col2 :
        st.markdown("<h3 style='text-align: center; background-color:blue;'>진보언론 (한겨레,경향신문)</h3>", unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown("**🟡워드클라우드**")
        st.image("진보기사 wc.png")
        
        st.markdown("**🟡언어네트워크**")
        st.write("공출현수치 30 이상인 단어만 표시됩니다")
        st.write("아래 버튼을 눌러주세요")
        click = st.button("진보언론 언어네트워크")
        if click : net(l_a, 30)
        
        
        st.markdown("**🟡도덕기반사전**")
        
        news_plot = sns.barplot(x= moral_result.index, y=moral_result["진보기사"], data = moral_result)
        news_plot.set_ylabel("단어개수")
        news_plot.figure.savefig('news_plot.png')
        plt.rcParams['font.family'] = 'NanumGothic'
        st.image("news_plot.png")
               
        selected_moral = st.selectbox('진보언론 도덕기반 선택', ["보살핌", "가해", "공정", "부정", "충성", "배반", "권위", "전복", "순수", "타락"])
        moral_dic = {"보살핌" : 0, "가해" : 1, "공정": 2, "부정": 3 , "충성":4 , "배반":5 , "권위":6 , "전복":7 , "순수":8 , "타락":9}
        moral_detail(l_a_moral, moral_dic["{}".format(str(selected_moral))])

    
elif side == '댓글' :
    st.header("댓글 데이터") 
    col1, col2 = st.columns(2)
    
    with col1 :
        st.markdown("<h3 style='text-align: center; background-color:red;'>보수언론댓글(조선, 동아)</h3>", unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown("**🟤 워드클라우드**")
        st.image("보수댓글 wc.png")
        
        st.markdown("**🟤 언어네트워크**")
        st.write("공출현수치 10 이상인 단어만 표시됩니다")
        st.write("아래 버튼을 눌러주세요")
        click = st.button("보수언론댓글 언어네트워크")
        if click : net(r_c, 10)
        
        
        st.markdown("**🟤 도덕기반사전**")
        
        com_plot = sns.barplot(x= moral_result.index, y=moral_result["보수댓글"], data = moral_result)
        com_plot.set_ylabel("단어개수")
        com_plot.figure.savefig('com_plot.png')
        plt.rcParams['font.family'] = 'NanumGothic'
        st.image("com_plot.png")
               
        selected_moral = st.selectbox('보수언론 도덕기반 선택', ["보살핌", "가해", "공정", "부정", "충성", "배반", "권위", "전복", "순수", "타락"])
        moral_dic = {"보살핌" : 0, "가해" : 1, "공정": 2, "부정": 3 , "충성":4 , "배반":5 , "권위":6 , "전복":7 , "순수":8 , "타락":9}
        moral_detail(r_c_moral, moral_dic["{}".format(str(selected_moral))])

    
    with col2 :
        st.markdown("<h3 style='text-align: center; background-color:blue;'>진보언론댓글(한겨레,경향)</h3>", unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown("**🟤 워드클라우드**")
        st.image("진보댓글 wc.png")
        
        st.markdown("**🟤 언어네트워크**")
        st.write("공출현수치 10 이상인 단어만 표시됩니다")
        st.write("아래 버튼을 눌러주세요")
        click = st.button("진보언론댓글 언어네트워크")
        if click : net(r_a, 10)
        
        
        st.markdown("**🟤 도덕기반사전**")
        
        com_plot2 = sns.barplot(x= moral_result.index, y=moral_result["진보댓글"], data = moral_result)
        com_plot2.set_ylabel("단어개수")
        com_plot2.figure.savefig('com_plot2.png')
        plt.rcParams['font.family'] = 'NanumGothic'
        st.image("com_plot2.png")
               
        selected_moral = st.selectbox('진보언론 도덕기반 선택', ["보살핌", "가해", "공정", "부정", "충성", "배반", "권위", "전복", "순수", "타락"])
        moral_dic = {"보살핌" : 0, "가해" : 1, "공정": 2, "부정": 3 , "충성":4 , "배반":5 , "권위":6 , "전복":7 , "순수":8 , "타락":9}
        moral_detail(l_c_moral, moral_dic["{}".format(str(selected_moral))])    
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from konlpy.tag import Komoran
tagger = Komoran()
from IPython.display import display, HTML
from pyvis import network as net
import numpy as np
stop_words = ['DB','다음', '위원장', '위원', '의원', '간사', '국회','PPT', '잠깐', '잠깐만', '잠깐만요', '후보자', '청문', '청문회', '인사청문회', '위원회','법무부', '장관', '한동훈', '최근','오후','오전','오늘','이날','이후','그것','그때','지금','당장','당시','이번','이제','이건','이것','이거','여기','거기','경우','정도','어디','저희','제가','저것','우리', '진행', '질의', '협의', '합의','회의','정회','의결','자료','관련','얘기','말씀','발언','생각','위원','문제','질문','답변','정회','이상','이제','이다','있다','여러분','연합뉴스','뉴스1','경향신문','한겨레','!!!','!!','라고','보니','동안','요즘','최고','제일','니들','너희','부분','내용','본인','자신','자기','드릴','만약','\n','\t','\r','♥' ,'α' , '■','▶','▲','/','+' ,'-','*','"',',','(',')','○',':','?','!!','!!!','!','.','[',']','…']

def cos_sim(text1, text2):
    tv = TfidfVectorizer()
    sents = (text1, text2)
    tfidf_matrix = tv.fit_transform(sents)
    st.write(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2]))

def draw_net(texts, co_oc):
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
    graph = net.Network(height='1000px', width='50%',heading='', bgcolor="#222222", font_color="white")
    graph.set_options("""
    const options = {
      "nodes": {
       "borderWidth": null,
       "borderWidthSelected": 4,
       "opacity": 1,
       "font": {
         "size": 20,
         "strokeWidth": 1
       },
       "size": 20
      },
      "edges": {
        "hoverWidth": 1.0,
        "physics": false,
        "scaling": {
          "min": 3,
          "max": 15,
              "label": {
                "min": null,
                "max": null,
                "maxVisible": 30,
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
                graph.add_edge(unique_words[i], unique_words[j], value=co_occurs[i][j])
    
    graph.show('example.html')
    display(HTML('example.html'))
import seaborn as sns
import streamlit as st
import matplotlib as plt
import webbrowser
from IPython.display import display, HTML
from prcd import * # 하나의 문자열로 뭉친 건 OO_str, 형태소 쪼개놓은 건 OO_words.
from mod import * # net, cos_sim, moral_detail 사용할 수 있다.
from moral import * # OO_moral로 리스트 불러올 수 있다.

#제목
st.markdown("<h1 style='text-align: center'>TEAM 1</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center'>인사청문회와 언론보도, 댓글에 대한 탐색적 연구</h3>", unsafe_allow_html=True)

#사이드바
side = st.sidebar.radio('INDEX',["INTRO","청문회데이터","언론보도", "댓글","Summary"])
if side == "INTRO" :
    st.header("INTRO")
        
    st.markdown(
    """
    **이론적으로 인사청문회 제도는 크게 세 가지 기능을 수행한다.:smile:**
    1. 입법부의 행정부 견제 기능: 국회에게 대통령의 인사를 검증, 동의할 권한을 부여함으로써 인사권 전횡 방지 
    2. 공직 후보자의 민주적 정당성 제고: 대의제 원칙에 따라 국민의 권리를 위임받은 국회의원의 동의 확보
    3. 정부의 역량 증진 및 국민의 알 권리 보장: 후보자 자격과 도덕성을 투명하게 공개해 신중하고 객관적인 인사 보장
    
    **하지만 위 순기능을 제한하는 현실적인 문제들도 많다.:cry:**
    1. 국정수행능력, 전문성, 정책 비전에 대한 검증보다는 도덕성 문제에 집중하는 '신상털기'식 질의 
    2. 입법부가 야당과 여당으로 분열돼 야당은 후보자를 공격하고, 여당은 방어하는 '여방야공' 구도
    3. 언론이 인사청문회의 내용을 있는 그대로 전하지 않고 정파적 관점에 맞도록 재구성
    
    ***
    ## 연구문제
    
    * 인사청문회, 언론 보도, 댓글 간 어떤 유사점과 차이점이 있는가? 
    * 정치 진영에 따라 인사청문회에 대한 언론 보도, 댓글의 양상이 달라지는가?
    
    ***
    ## 연구대상
    | 청문회회의록      |    뉴스 기사      | 댓글              |
    |-------------------|-------------------|-------------------|
    |국민의 힘 의원 발언| 보수(조선, 중앙)  | 보수(조선, 중앙)  |
    |민주당 의원 발언   | 진보(한겨레, 경향)| 진보(한겨레, 경향)|
    |한동훈 발언        |                   |                   |
    
    
    """
    )
    selected_intro = st.selectbox('더 자세히 살펴보고 싶은 자료를 클릭하세요', ["<보기>", "회의록", "기사", "댓글"], 0)
    if selected_intro != "<보기>":       
        if selected_intro == "회의록":
            st.subheader("21대 국회회의록 법제사법위원회 397회 1차, 2차, 3차")
            st.write("총 304,172자")
            st.image("hearing2.png")
            st.image("hearing.png")
        
        elif selected_intro == "기사":
            st.subheader("네이버 뉴스 기사 크롤링(언론사 사이트 x)")
            st.write("보수 121건, 진보 86건") 
            st.image("article.png")
    
        elif selected_intro == "댓글":
            st.subheader("네이버 뉴스 댓글 크롤링(순공감순, 더보기 5번)")
            st.write("보수 1422건, 진보 991건")
            st.image("comment.png")
    
    st.markdown(
    """
    ***
    ## 연구방법
    """
    )
    st.image("method.png")
        
#Summary 페이지
elif side == 'Summary' :    
    st.header("Summary")
    st.subheader("문서 유사도 분석(코사인 유사도)")
    st.write("국민의힘 위원들과 민주당 위원들의 청문회 발언 유사도가 0.81, 보수와 진보 기사 유사도가 0.87, 보수와 진보 댓글 유사도가 0.69로 높은 편")
    st.image("cosine_table.png")
    
    st.markdown("***")
    
    st.subheader("문서 유사도 분석(N-gram 분석)")
    selected_gram = st.radio("N-gram 분석에서 N을 몇 개로 설정할지 고르세요", ("2", "3"))
    if selected_gram == "2":
        st.write("국민의힘 위원들과 한동훈 후보자의 청문회 발언 유사도가 0.67, 보수와 진보 기사 유사도가 0.74, 보수와 진보 댓글 유사도가 0.69로 높은 편")
        st.image("2gram.png")
    if selected_gram == "3":    
        st.write("국민의힘 위원들과 민주당 위원들의 청문회 발언 유사도가 0.48, 보수와 진보 기사 유사도가 0.59, 보수와 진보 댓글 유사도가 0.46로 높은 편")
        st.image("3gram.png")
 
    
    st.markdown("***")
    
    st.subheader("문서 중심성 분석(상위 20개 키워드)")
    selected_centrality = st.selectbox('중심성 유형을 선택하세요', ["매개중심성", "연결중심성", "페이지랭크", "근접중심성"])
    
    
    bet_table = pd.DataFrame(columns = ["보수기사", "진보기사", "보수댓글", "진보댓글", "국힘발언","민주당발언","한동훈발언"])
    bet_table["보수기사"] = ["민주당","국민","더불어민주당","대통령","검찰","윤석열","서울","수사","기자","정부","의혹","인사","주장","비판","사건","사실","정치","사람","과정","여의도"]
    bet_table["진보기사"] = ["윤석열","대통령","더불어민주당","국민","정부","검찰","수사","의혹","인사","기자","민주당","필요","서울","비판","사진","임명","출신","주장","사람","스펙"]
    bet_table["보수댓글"] = ["국민","민주당","사람","수사","검찰","검사","수준","조국","비리","정권","나라","윤석열","대통령","정치","공정","이모","인간","검수완박","누구","사건"]
    bet_table["진보댓글"] = ["국민","민주당","검찰","수사","조국","논문","사람","나라","대통령","윤석열","인간","검수완박","정치","언론","문재인","스펙","수준","불법","공정","한국"]
    bet_table["국힘발언"] = ["수사","검찰","검수완박","국민","사건","검사","사실","민주당","지적","증인","과정","조국","문재인","사람","절차","동의","혐의","법안","주장","처리"]
    bet_table["민주당발언"] = ["수사","국민","사람","검찰","사실","검사","사건","제출","확인","의혹","제기","논문","요구","필요","인사","아파트","동의","언론","불법","이야기"]
    bet_table["한동훈발언"] = ["수사","사실","상황","사람","과정","사건","검찰","범죄","이해","국민","봉사","검사","상태","이유","나중","수준","취임","기부","보도","취지"]    
    
    deg_table = pd.DataFrame(columns = ["보수기사", "진보기사", "보수댓글", "진보댓글", "국힘발언","민주당발언","한동훈발언"])
    deg_table["보수기사"] = ["민주당","국민","검찰","더불어민주당","대통령","윤석열","서울","수사","인사","기자","정부","사건","의혹","주장","비판","사실","검수완박","사람","과정","입장"]
    deg_table["진보기사"] = ["윤석열","대통령","더불어민주당","국민","검찰","정부","수사","인사","의혹","서울","민주당","기자","비판","임명","필요","사진","주장","상황","지적","사람"]
    deg_table["보수댓글"] = ["국민","민주당","사람","수사","검사","검찰","수준","비리","조국","정권","정치","공정","윤석열","나라","조작","권력","검수완박","국회의원","선거","대통령"]
    deg_table["진보댓글"] = ["국민","민주당","검찰","수사","나라","조국","사람","대통령","논문","윤석열","정치","검수완박","문재인","공정","인간","상식","언론","수준","정신","불법"]
    deg_table["국힘발언"] = ["수사","검찰","검수완박","국민","사건","검사","사실","민주당","문재인","사람","후보","의혹","법사위","박범계","법안","처리","과정","상황","정권","대통령"]
    deg_table["민주당발언"] = ["수사","국민","검찰","사람","사건","사실","검사","제출","제기","의혹","확인","필요","논문","요구","언론","검증","기소","보도","과정","봉사"]
    deg_table["한동훈발언"] = ["수사","사실","상황","검찰","과정","국민","사람","범죄","사건","검사","운영","봉사","법률","수준","제도","부패","피해","취임","피해자","일반"]
    
    pr_table = pd.DataFrame(columns = ["보수기사", "진보기사", "보수댓글", "진보댓글", "국힘발언","민주당발언","한동훈발언"])
    pr_table["보수기사"] = ["민주당","국민","더불어민주당","검찰","대통령","윤석열","서울","수사","기자","정부","인사","의혹","사건","주장","비판","사실","사람","정치","검수완박","과정"]
    pr_table["진보기사"] = ["윤석열","대통령","더불어민주당","국민","검찰","정부","수사","의혹","인사","민주당","서울","기자","비판","임명","사진","필요","주장","사람","지적","상황"]
    pr_table["보수댓글"] = ["국민","민주당","사람","수사","검찰","검사","수준","조국","정권","비리","정치","윤석열","대통령","나라","공정","검수완박","권력","이모","국회의원","선거"]
    pr_table["진보댓글"] = ["국민","민주당","검찰","수사","나라","조국","사람","대통령","논문","윤석열","검수완박","정치","인간","문재인","언론","공정","수준","상식","경찰","불법"]
    pr_table["국힘발언"] = ["수사","검찰","검수완박","국민","사건","검사","사실","민주당","문재인","사람","후보","과정","의혹","법안","법사위","조국","처리","박범계","증인", "상황"]
    pr_table["민주당발언"] = ["수사","국민","검찰","사람","사건","검사","사실","제출","제기","의혹","확인","필요","논문","요구","언론","기소","검증","보도","과정","봉사"]
    pr_table["한동훈발언"] = ["수사","사실","상황","검찰","과정","사건","사람","국민","범죄","검사","봉사","운영","수준","법률","제도","나중","취임","이해","피해","부패"]
    
    close_table = pd.DataFrame(columns = ["보수기사", "진보기사", "보수댓글", "진보댓글", "국힘발언","민주당발언","한동훈발언"])
    close_table["보수기사"] = ["민주당","국민","검찰","더불어민주당","대통령","윤석열","서울","수사","인사","기자","정부","사건","의혹","주장","비판","사실","검수완박","사람","과정","입장"]
    close_table["진보기사"] = ["윤석열","대통령","더불어민주당","국민","검찰","정부","수사","인사","의혹","서울","민주당","기자","비판","임명","필요","사진","주장","상황","지적","사람"]
    close_table["보수댓글"] = ["국민","민주당","사람","수사","검사","수준","조국","정권","검찰","비리","권력","정치","나라","공정","윤석열","국회의원","조작","문재인","소리","대통령"]
    close_table["진보댓글"] = ["국민","민주당","검찰","조국","수사","사람","나라","대통령","윤석열","공정","상식","언론","검수완박","정치","논문","정부","정신","한국","인간","문재인"]
    close_table["국힘발언"] = ["수사","검찰","검수완박","국민","사건","검사","사실","민주당","문재인","사람","법사위","처리","후보","과정","총장","대통령","필요","박범계","상황", "의혹"]
    close_table["민주당발언"] = ["수사","국민","검찰","사람","사실","검사","사건","제기","제출","의혹","확인","필요","요구","언론","논문","검증","과정","보도","기소","활동"]
    close_table["한동훈발언"] = ["수사","사실","상황","과정","사람","검찰","범죄","사건","국민","검사","운영","제도","정치","수준","이해","입장","필요","피해","법률","고발"]


    if selected_centrality == "매개중심성":
        st.table(bet_table)
    elif selected_centrality == "연결중심성":
        st.table(deg_table)
    elif selected_centrality == "페이지랭크":
        st.table(pr_table)
    elif selected_centrality == "근접중심성":
        st.table(close_table)
    
    st.markdown("***")
    
    st.subheader("도덕기반사전 분석")
    selected_moral = st.radio("어떤 차트를 보고 싶은지 고르세요", ("개수", "퍼센트"))
    if selected_moral == "개수":
        st.image("moral_graph.png")
    if selected_moral == "퍼센트":    
        st.image("moral_percent.png")

# 청문회데이터 페이지
elif side == '청문회데이터':
    st.header("청문회데이터")
    # options = st.multiselect("코사인 유사도를 보고 싶은 2가지를 고르세요", ["민주당발언", "한동훈발언", "국민의힘발언"])
    # d = []
    # try:
    #     for i in options:
    #         if i == "민주당발언":
    #             a = dp_str
    #             d.append(a)
    #         elif i == "한동훈발언":
    #             b = han_str
    #             d.append(b)
    #         elif i == "국민의힘발언":
    #             c = pp_str
    #             d.append(c)
    #     cos_sim(d[0], d[1])
    # except:
    #     st.write("현재", len(options), "개를 고르셨습니다.", " 2개를 골라주세요")

    # st.markdown("***")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h3 style='text-align: center; background-color:blue;'>더불어민주당</h3>", unsafe_allow_html=True)

        st.markdown("**🟡워드클라우드**")
        st.image("민주발언 wc.png")

        st.markdown("**🟡언어네트워크**")
        st.write("공출현수치 10 이상인 단어만 표시됩니다")
        st.write("아래 버튼을 눌러주세요")
        click = st.button("민주당 언어네트워크")
        if click: webbrowser.open_new_tab('dp_net.html')


        st.markdown("**🟡토픽모델링**")
        if st.button("민주발언 pyLDAVis 보기"):
            webbrowser.open_new_tab('dp_vis.html')
            
        st.markdown("**🟡도덕기반사전**")
        st.image("민주발언_moral.png")

        selected_moral = st.selectbox('민주당 도덕기반 선택', ["보살핌", "가해", "공정", "부정", "충성", "배반", "권위", "전복", "순수", "타락"])
        moral_dic = {"보살핌": 0, "가해": 1, "공정": 2, "부정": 3, "충성": 4, "배반": 5, "권위": 6, "전복": 7, "순수": 8, "타락": 9}
        moral_detail(dp_moral, moral_dic["{}".format(str(selected_moral))])

    with col2:
        st.markdown("<h3 style='text-align: center; background-color:red;'>국민의힘</h3>", unsafe_allow_html=True)

        st.markdown("**🟡워드클라우드**")
        st.image("국힘발언 wc.png")

        st.markdown("**🟡언어네트워크**")
        st.write("공출현수치 10 이상인 단어만 표시됩니다")
        st.write("아래 버튼을 눌러주세요")
        click = st.button("국민의힘 언어네트워크")
        if click: webbrowser.open_new_tab('pp_net.html')

        st.markdown("**🟡토픽모델링**")
        if st.button('국힘발언 pyLDAVis 보기'):
            webbrowser.open_new_tab('pp_vis.html')
            
        st.markdown("**🟡도덕기반사전**")
        st.image("국힘발언_moral.png")

        selected_moral = st.selectbox('국민의 힘 도덕기반선택', ["보살핌", "가해", "공정", "부정", "충성", "배반", "권위", "전복", "순수", "타락"])
        moral_dic = {"보살핌": 0, "가해": 1, "공정": 2, "부정": 3, "충성": 4, "배반": 5, "권위": 6, "전복": 7, "순수": 8, "타락": 9}
        moral_detail(pp_moral, moral_dic["{}".format(str(selected_moral))])

    with col3:
        st.markdown("<h3 style='text-align: center; background-color:gray'>한동훈</h3>", unsafe_allow_html=True)
        st.markdown("**🟡워드클라우드**")
        st.image("한동훈 발언 wc.png")

        st.markdown("**🟡언어네트워크**")
        st.write("공출현수치 10 이상인 단어만 표시됩니다")
        st.write("아래 버튼을 눌러주세요")
        click = st.button("한동훈 언어네트워크")
        if click: webbrowser.open_new_tab('han_net.html')
        
        st.markdown("**🟡토픽모델링**")
        if st.button('한동훈 발언 pyLDAVis 보기'):
            webbrowser.open_new_tab('han_vis.html')
            
        st.markdown("**🟡도덕기반사전**")
        st.image("한동훈_moral.png")

        selected_moral = st.selectbox('한동훈 도덕기반선택', ["보살핌", "가해", "공정", "부정", "충성", "배반", "권위", "전복", "순수", "타락"])
        moral_dic = {"보살핌": 0, "가해": 1, "공정": 2, "부정": 3, "충성": 4, "배반": 5, "권위": 6, "전복": 7, "순수": 8, "타락": 9}
        moral_detail(han_moral, moral_dic["{}".format(str(selected_moral))])


elif side == '언론보도':
    st.header("언론보도 데이터")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='text-align: center; background-color:red;'>보수언론 (조선, 동아일보)</h3>",
                    unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown("**🟡 워드클라우드**")
        st.image("보수기사 wc.png")

        st.markdown("**🟡 언어네트워크**")
        st.write("공출현수치 30 이상인 단어만 표시됩니다")
        st.write("아래 버튼을 눌러주세요")
        click = st.button("보수언론 언어네트워크")
        if click: webbrowser.open_new_tab('r_a_net.html')

        st.markdown("**🟡 토픽모델링**")
        if st.button('보수기사 pyLDAVis 보기'):
            webbrowser.open_new_tab('r_a_vis.html')

        st.markdown("**🟡 도덕기반사전**")
        st.image("보수기사_moral.png")

        selected_moral = st.selectbox('보수언론 도덕기반 선택', ["보살핌", "가해", "공정", "부정", "충성", "배반", "권위", "전복", "순수", "타락"])
        moral_dic = {"보살핌": 0, "가해": 1, "공정": 2, "부정": 3, "충성": 4, "배반": 5, "권위": 6, "전복": 7, "순수": 8, "타락": 9}
        moral_detail(r_a_moral, moral_dic["{}".format(str(selected_moral))])

    with col2:
        st.markdown("<h3 style='text-align: center; background-color:blue;'>진보언론 (한겨레,경향신문)</h3>",
                    unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown("**🟡 워드클라우드**")
        st.image("진보기사 wc.png")

        st.markdown("**🟡 언어네트워크**")
        st.write("공출현수치 30 이상인 단어만 표시됩니다")
        st.write("아래 버튼을 눌러주세요")
        click = st.button("진보언론 언어네트워크")
        if click: webbrowser.open_new_tab('l_a_net.html')

        st.markdown("**🟡 토픽모델링**")
        if st.button('진보기사 pyLDAVis 보기'):
            webbrowser.open_new_tab('l_a_vis.html')

        st.markdown("**🟡 도덕기반사전**")
        st.image("진보기사_moral.png")

        selected_moral = st.selectbox('진보언론 도덕기반 선택', ["보살핌", "가해", "공정", "부정", "충성", "배반", "권위", "전복", "순수", "타락"])
        moral_dic = {"보살핌": 0, "가해": 1, "공정": 2, "부정": 3, "충성": 4, "배반": 5, "권위": 6, "전복": 7, "순수": 8, "타락": 9}
        moral_detail(l_a_moral, moral_dic["{}".format(str(selected_moral))])


elif side == '댓글':
    st.header("댓글 데이터")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='text-align: center; background-color:red;'>보수언론댓글(조선, 동아)</h3>", unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown("**🟤 워드클라우드**")
        st.image("보수댓글 wc.png")

        st.markdown("**🟤 언어네트워크**")
        st.write("공출현수치 10 이상인 단어만 표시됩니다")
        st.write("아래 버튼을 눌러주세요")
        click = st.button("보수댓글 언어네트워크")
        if click: webbrowser.open_new_tab('r_c_net.html')

        st.markdown("**🟤 토픽모델링**")
        if st.button('보수댓글 pyLDAVis 보기'):
            webbrowser.open_new_tab('r_c_vis.html')

        st.markdown("**🟤 도덕기반사전**")
        st.image("보수댓글_moral.png")

        selected_moral = st.selectbox('보수댓글 도덕기반 선택', ["보살핌", "가해", "공정", "부정", "충성", "배반", "권위", "전복", "순수", "타락"])
        moral_dic = {"보살핌": 0, "가해": 1, "공정": 2, "부정": 3, "충성": 4, "배반": 5, "권위": 6, "전복": 7, "순수": 8, "타락": 9}
        moral_detail(r_c_moral, moral_dic["{}".format(str(selected_moral))])

    with col2:
        st.markdown("<h3 style='text-align: center; background-color:blue;'>진보언론댓글(한겨레,경향)</h3>",
                    unsafe_allow_html=True)
        st.markdown(" ")
        st.markdown("**🟤 워드클라우드**")
        st.image("진보댓글 wc.png")

        st.markdown("**🟤 언어네트워크**")
        st.write("공출현수치 10 이상인 단어만 표시됩니다")
        st.write("아래 버튼을 눌러주세요")
        click = st.button("진보댓글 언어네트워크")
        if click: webbrowser.open_new_tab('r_a_net.html')

        st.markdown("**🟤 토픽모델링**")
        if st.button('진보댓글 pyLDAVis 보기'):
            webbrowser.open_new_tab('r_a_vis.html')

        st.markdown("**🟤 도덕기반사전**")
        st.image("진보댓글_moral.png")

        selected_moral = st.selectbox('진보댓글 도덕기반 선택', ["보살핌", "가해", "공정", "부정", "충성", "배반", "권위", "전복", "순수", "타락"])
        moral_dic = {"보살핌": 0, "가해": 1, "공정": 2, "부정": 3, "충성": 4, "배반": 5, "권위": 6, "전복": 7, "순수": 8, "타락": 9}
        moral_detail(l_c_moral, moral_dic["{}".format(str(selected_moral))])



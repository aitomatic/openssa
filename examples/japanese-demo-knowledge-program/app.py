from dotenv import load_dotenv
from agent import get_or_create_agent
import streamlit as st


load_dotenv()

TITLE: str = 'OpenSSA デモアプリ: 災害時の初動判断支援エージェント'
DEFAULT_PROMPT = "台風が発生しました。警戒レベルは4です。どうしたら良いですか？"
agent = get_or_create_agent()

def main():
    st.set_page_config(
        page_title=TITLE,
        page_icon=None,
        layout='wide',
        initial_sidebar_state='auto',
    )
    st.title(body=TITLE, anchor=None, help=None)
    st.write('__発生している問題または質問事項を入力してください__:')

    if 'typed_problem' not in st.session_state:
        st.session_state.typed_problem = DEFAULT_PROMPT

    st.session_state.typed_problem = st.text_area(
        label='Problem/Question',
        value=st.session_state.typed_problem,
        max_chars=None,
        height=22 * 6,
        key=None,
        help='Problem/Question',
        on_change=None, args=None, kwargs=None,
        placeholder='発生している問題または質問事項',
        disabled=False,
        label_visibility='collapsed'
    )

    if st.button(label='問い合わせ',
                 type='primary',
                 disabled=False,
                 use_container_width=False):
        with st.spinner(text='_問い合わせ中..._'):
            solution: str = \
                agent.solve(problem=st.session_state.typed_problem + '\nPlease answer in Japanese.', allow_reject=True)
        st.markdown(body=solution)


if __name__ == '__main__':
    main()

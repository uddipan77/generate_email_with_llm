import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="")
    submit_button = st.button("Submit")

    if submit_button:
        if not url_input.strip():
            st.warning("Please enter a job URL first.")
            return

        try:
            # 👇 Spinner to show something is happening
            with st.spinner("Processing job posting and generating your cold email..."):
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)

                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                if not jobs:
                    st.warning("No jobs could be extracted from this page.")
                    return

                for job in jobs:
                    skills = job.get("skills", [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.code(email, language="markdown")

            st.success("Done! Scroll down to see your generated email(s).")

        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)

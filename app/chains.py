import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

from opik.integrations.langchain import OpikTracer

load_dotenv()


class Chain:
    def __init__(self):
        # 🔢 Prompt versions (update these when you change the prompts)
        self.extract_prompt_version = "extract_v1_basic"
        self.email_prompt_version = "email_v1_personal_bullets"

        # LLM
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile",
        )

        # 👇 Opik tracer for the extraction prompt
        self.extract_tracer = OpikTracer(
            project_name="cold email generator project",
            tags=[
                "cold-email",
                "streamlit-app",
                "prompt_kind:extract",
                self.extract_prompt_version,
            ],
            metadata={
                "app": "cold-mail-generator",
                "prompt_kind": "extract_jobs",
                "prompt_version": self.extract_prompt_version,
            },
        )

        # 👇 Opik tracer for the email-writing prompt
        self.email_tracer = OpikTracer(
            project_name="cold email generator project",
            tags=[
                "cold-email",
                "streamlit-app",
                "prompt_kind:email",
                self.email_prompt_version,
            ],
            metadata={
                "app": "cold-mail-generator",
                "prompt_kind": "write_mail",
                "prompt_version": self.email_prompt_version,
            },
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            The scraped text is from the careers page of a website.
            Your job is to extract the job postings and return them in JSON format
            containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.

            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm

        # Use the extraction tracer
        res = chain_extract.invoke(
            {"page_data": cleaned_text},
            config={"callbacks": [self.extract_tracer]},
        )

        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### PORTFOLIO LINKS:
            {link_list}

            ### INSTRUCTION:
            You are Udipan Basu Bir, a Master's student in Data Science and Artificial Intelligence.
            You previously worked as a Data Engineer and Data Analyst at TCS and have completed
            multiple Generative AI, Machine Learning, and Deep Learning projects.

            Write a concise, professional and friendly cold email to the hiring manager
            about the job above.

            **Formatting requirements (very important):**

            - Start with a Subject line: `Subject: ...`
            - Then a greeting: `Dear Hiring Manager,`
            - Use short paragraphs (2–4 sentences each).
            - Include a section titled `Key skills and experience:` with a
              Markdown bullet list of 4–8 relevant skills/technologies.
            - Include a section titled `Selected projects and portfolio:` with a
              Markdown bullet list; each item briefly describes a project and
              includes one of the portfolio links.
            - Close with a short paragraph expressing interest and proposing a call.
            - Sign off with your name at the end.

            **Tone & persona:**

            - Write in the first person ("I", not "we").
            - Do NOT mention AtliQ or any consulting company.
            - Do NOT present yourself as a team or company.
            - Keep the tone professional but approachable.

            Only output the final email in Markdown format.

            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm

        # Use the email tracer
        res = chain_email.invoke(
            {"job_description": str(job), "link_list": links},
            config={"callbacks": [self.email_tracer]},
        )

        return res.content


if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))

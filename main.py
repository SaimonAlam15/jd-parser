import os
from dotenv import load_dotenv

from openai import OpenAI
import streamlit as st

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def get_job_skills(job_description):
    skills =  [
        'Advertising', 'Art & Creative', 'Bookkeeping', 'Brand Strategy', 'Business Strategy', 'Clinical Research', 'Cloud Computing',
        'Communications', 'Community & Partnerships', 'Compliance', 'Computer Programming', 'Customer Success/CX', 'Cybersecurity',
        'Data Science', 'DEI', 'Design', 'DevOps', 'Education', 'Engineering', 'Entrepreneurship', 'ESG/CSR', 'Events', 'Fashion',
        'Finance', 'Fundraising', 'Government', 'Health and Fitness', 'Hospitality', 'Human Resources', 'Insurance', 'Legal', 'Logistics',
        'Management Consulting', 'Manufacturing', 'Market Research', 'Marketing', 'Media', 'Merchandising', 'Military', 'Nonprofit', 'Operations',
        'Organizational Development', 'Other', 'Product Management', 'Production, Film', 'Public Relations', 'Recruitment & Talent Acquisition', 'Retail',
        'Sales & Business Development', 'Social Media', 'Social Services', 'Technology', 'Venture Capital & Private Equity', 'Web', 'Writing, Editing'
    ]

    question = f"""From the following list of skills: {skills}, select the ones which are only 100% required for the job with the following description: {job_description}.
    Please provide your answer as a comma separated list. And please limit your answer only to the provided list of skills. It is okay if there are no matches.
    And only mention the list in the response, no extra words please."""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="gpt-4o",
        temperature=1,
        top_p=1,
        frequency_penalty=-0.9,
        presence_penalty=-1
    )

    response = chat_completion.choices[0].message.content
    return [skill for skill in skills if skill in response]


def main():
    st.set_page_config(layout="wide")
    st.markdown("<h1 style='text-align: center;'>Skill Parser</h1>", unsafe_allow_html=True)
    job_description = st.text_area("Enter the job description here:", height=300)
    if st.button("Parse Skills"):
        if job_description:
            skills = get_job_skills(job_description)
            if skills:
                st.write("Required Skills: ", ", ".join(skills))
            else:
                st.write("No matching skills found.")
        else:
            st.write("Please enter a job description.")


if __name__ == '__main__':
    main()
    
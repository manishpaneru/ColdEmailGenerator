# Cold Email Generator for Job Applications
_______________________________________________________________________________________________________

## Overview

I developed a Cold Email Generator application that leverages AI to create personalized cold emails for job applications. The application extracts key details from a user's resume and a job posting URL, then uses these details to generate a tailored email. The email can be customized with different tones, such as Professional, Confident, or Creative.

## Approach

### Problem Understanding

The primary goal was to automate the process of generating cold emails for job applications. This involved:
- Extracting relevant information from a resume.
- Scraping job details from a provided URL.
- Using AI to generate a personalized email based on the extracted data.

### Solution Design

1. **Resume Parsing**: I used the `PyPDF2` library to extract text from PDF resumes. This text is then processed to extract contact details such as name, phone number, email, and LinkedIn profile using regular expressions and spaCy for Named Entity Recognition.

2. **Job Details Extraction**: I implemented a job scraper using `requests` and `beautifulsoup4` to extract job details from a given URL. This includes job title, company name, required skills, and experience.

3. **Email Generation**: I utilized the `langchain` and `langchain-groq` libraries to create a language model chain that generates emails. The model uses a prompt template that incorporates the job details, resume content, and the selected tone to produce a coherent and contextually relevant email.

4. **User Interface**: I built a user-friendly interface using `streamlit` that allows users to input a job URL, upload their resume, and select the desired email tone. The generated email is displayed in a text area with an option to copy it to the clipboard.

### Technical Architecture

- **Frontend**: Streamlit is used to create an interactive web interface for user inputs and displaying the generated email.
- **Backend**: The backend logic is implemented in Python, handling resume parsing, job scraping, and email generation.
- **AI Integration**: The email generation leverages the Groq language model through the `langchain` library, which processes the input data and generates human-like emails.

## Technologies Used

- **Python**: The core programming language for the project.
- **Streamlit**: For building the web interface.
- **PyPDF2**: For extracting text from PDF resumes.
- **spaCy**: For Named Entity Recognition to extract names from resumes.
- **langchain & langchain-groq**: For AI-driven email generation.
- **requests & beautifulsoup4**: For web scraping job details.
- **dotenv**: For managing environment variables.

## Skills Learned and Displayed

- **AI and Natural Language Processing**: I learned how to integrate AI models to generate human-like text based on structured input data.
- **Web Scraping**: I enhanced my skills in extracting data from web pages using Python libraries.
- **PDF Processing**: I gained experience in parsing and extracting information from PDF documents.
- **User Interface Design**: I developed a user-friendly interface using Streamlit, focusing on usability and functionality.
- **Regular Expressions**: I applied regex patterns to extract structured data from unstructured text effectively.

## Conclusion

This project showcases my ability to integrate various technologies to solve a real-world problem. By combining AI, web scraping, and PDF processing, I created a tool that automates the tedious task of writing personalized job application emails, making the job application process more efficient and effective.
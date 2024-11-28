import streamlit as st
from utils.job_scraper import JobScraper
from utils.email_generator import EmailGenerator
import os
from dotenv import load_dotenv
import PyPDF2
import io

# Load environment variables
load_dotenv()

# Initialize components
scraper = JobScraper()
email_generator = EmailGenerator()

def extract_text_from_pdf(pdf_file):
    """Extract text content from uploaded PDF file"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def main():
    st.title("Cold Email Generator for Job Applications")
    
    # URL input
    job_url = st.text_input("Enter the job posting URL:")
    
    # Resume upload
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=['pdf'])
    
    # Tone selection
    tone = st.selectbox(
        "Select email tone",
        ["Professional", "Confident", "Creative"],
        help="Professional: Formal and traditional\nConfident: Bold and assertive\nCreative: Innovative and engaging"
    )
    
    if job_url and uploaded_file:  # Check both URL and resume are provided
        # Generate email button
        if st.button("Generate Cold Email"):
            try:
                with st.spinner("Generating email..."):
                    # Extract resume text
                    resume_text = extract_text_from_pdf(uploaded_file)
                    
                    # First scrape the details
                    job_details = scraper.extract_job_details(job_url)
                    
                    if job_details:
                        # Generate the email with all required parameters
                        email_content = email_generator.generate_email(
                            job_details=job_details,
                            resume_text=resume_text,
                            tone=tone.lower()
                        )
                        
                        # Display generated email
                        st.subheader("Generated Cold Email")
                        email_area = st.text_area("Email Content", email_content, height=300)
                        
                        # Add copy button
                        if st.button("Copy to Clipboard"):
                            st.write("Email copied to clipboard!")
                            st.session_state['clipboard'] = email_content
                    else:
                        st.error("Failed to extract job details. Please check the URL and try again.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Please provide both a job URL and upload your resume to generate the email.")

if __name__ == "__main__":
    main() 

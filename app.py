import streamlit as st
from utils.job_scraper import JobScraper
from utils.email_generator import EmailGenerator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize components
scraper = JobScraper()
email_generator = EmailGenerator()

def main():
    st.title("Cold Email Generator for Job Applications")
    
    # URL input
    job_url = st.text_input("Enter the job posting URL:")
    
    if job_url:
        # Generate email button
        if st.button("Generate Cold Email"):
            with st.spinner("Generating email..."):
                # First scrape the details
                job_details = scraper.extract_job_details(job_url)
                
                if job_details:
                    # Generate the email
                    email_content = email_generator.generate_email(job_details)
                    
                    # Display generated email
                    st.subheader("Generated Cold Email")
                    email_area = st.text_area("Email Content", email_content, height=300)
                    
                    # Add copy button
                    if st.button("Copy to Clipboard"):
                        st.write("Email copied to clipboard!")
                        st.session_state['clipboard'] = email_content
                else:
                    st.error("Failed to extract job details. Please check the URL and try again.")

if __name__ == "__main__":
    main() 
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import re
import spacy
import subprocess

class EmailGenerator:
    """
    A class to generate personalized cold emails for job applications.
    Uses the Groq LLM to create human-like, contextually relevant emails
    based on job details and resume content.
    """
    
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="mixtral-8x7b-32768"
        )
        
        # Load spaCy model with better error handling
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spaCy English model...")
            try:
                # Try using pip to install the model
                subprocess.run(["pip", "install", "en-core-web-sm"], check=True)
                self.nlp = spacy.load("en_core_web_sm")
            except:
                try:
                    # If pip install fails, try using spacy download command
                    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
                    self.nlp = spacy.load("en_core_web_sm")
                except:
                    print("Warning: Could not load spaCy model. Name extraction will use fallback methods.")
                    self.nlp = None
        
        # Updated template to use resume content and tone
        self.email_template = PromptTemplate(
            input_variables=["job_title", "company", "skills", "experience", "resume", "tone"],
            template="""
            Write a personalized cold email for a job application with the following details:
            Job Title: {job_title}
            Company: {company}
            Required Skills: {skills}
            Required Experience: {experience}

            # Candidate's Resume Summary:
            {resume}

            # Tone Guidelines:
            Tone: {tone}
            Professional Tone: Formal, traditional, and business-appropriate language
            Confident Tone: Bold, assertive language that emphasizes achievements
            Creative Tone: Innovative, engaging, and unique approach while maintaining professionalism

            # Guidelines for email structure:
            1. Analyze the resume and extract relevant experiences and skills that match the job requirements
            2. Highlight the most impressive and relevant achievements from the resume
            3. Focus on quantifiable results and specific technical skills that match the job
            4. Show enthusiasm for the role and company's mission
            5. Include a clear call to action for next steps
            6. Maintain the selected tone throughout the email
            7. Keep the email concise (200-300 words)

            # Required Email Structure:
            1. Start with an attention-grabbing subject line that includes the job title
            2. Opening paragraph: Hook and position mention
            3. Body: 2-3 paragraphs highlighting relevant experience and achievements
            4. Closing: Call to action and professional sign-off

            Write the complete email now, including the subject line:
            """
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.email_template)

    def extract_name_from_resume(self, resume_text):
        """
        Extract the candidate's name from resume text using multiple methods
        """
        # Clean the text
        clean_text = resume_text.strip().replace('\n', ' ')
        first_line = clean_text.split('.')[0].strip()

        # Method 1: Using spaCy for Named Entity Recognition (if available)
        if self.nlp is not None:
            try:
                doc = self.nlp(first_line)
                person_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
                if person_names:
                    return person_names[0]
            except Exception as e:
                print(f"spaCy name extraction failed: {e}")
        
        # Method 2: Common resume header patterns
        name_patterns = [
            r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})",  # Standard name format
            r"Name:?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})",  # "Name: John Doe"
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\s*(?:Resume|CV)",  # "John Doe Resume"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, clean_text)
            if match:
                return match.group(1)
        
        # Method 3: First line heuristic (if it looks like a name)
        words = first_line.split()
        if 2 <= len(words) <= 3:
            if all(word.strip() and word[0].isupper() for word in words):
                return first_line
        
        return "Job Applicant"  # Default fallback

    def extract_contact_details(self, resume_text):
        """
        Extract contact details including name, phone, email, and LinkedIn from resume
        """
        # Clean the text
        clean_text = resume_text.strip()
        
        # Initialize contact details dictionary
        contact_details = {
            'name': self.extract_name_from_resume(clean_text),
            'phone': None,
            'email': None,
            'linkedin': None
        }
        
        # Phone number patterns
        phone_patterns = [
            r'\b(?:\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',  # (123) 456-7890, 123-456-7890
            r'\b\d{10}\b',  # 1234567890
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'  # 123.456.7890
        ]
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # LinkedIn pattern
        linkedin_patterns = [
            r'linkedin\.com/in/[\w-]+',
            r'linkedin\.com/profile/[\w-]+'
        ]
        
        # Extract phone
        for pattern in phone_patterns:
            match = re.search(pattern, clean_text)
            if match:
                contact_details['phone'] = match.group()
                break
        
        # Extract email
        email_match = re.search(email_pattern, clean_text)
        if email_match:
            contact_details['email'] = email_match.group()
        
        # Extract LinkedIn
        for pattern in linkedin_patterns:
            match = re.search(pattern, clean_text.lower())
            if match:
                contact_details['linkedin'] = "www." + match.group()
                break
        
        return contact_details

    def generate_email(self, job_details, resume_text, tone):
        """
        Generates a personalized cold email based on the job details and resume.
        """
        skills = ", ".join(job_details['primary_skills'])
        
        # Extract all contact details
        contact_details = self.extract_contact_details(resume_text)
        
        email = self.chain.run({
            "job_title": job_details['title'],
            "company": job_details['company'],
            "skills": skills,
            "experience": job_details['experience'],
            "resume": resume_text,
            "tone": tone
        })
        
        # Find the position of "sincerely" and replace everything after it
        sincerely_index = email.lower().rfind("sincerely")
        if sincerely_index != -1:
            email = email[:sincerely_index].strip()

        # Create a comprehensive signature with all available contact details
        signature = "\n\nBest Regards,\n"
        signature += f"{contact_details['name']}"
        
        if contact_details['phone']:
            signature += f"\nPhone: {contact_details['phone']}"
        if contact_details['email']:
            signature += f"\nEmail: {contact_details['email']}"
        if contact_details['linkedin']:
            signature += f"\nLinkedIn: {contact_details['linkedin']}"
        
        email += signature
        return email 

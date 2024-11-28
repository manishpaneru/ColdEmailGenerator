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

    def generate_email(self, job_details, resume_text, tone, verified_name=None):
        """
        Generates a personalized cold email based on the job details and resume.
        
        Args:
            job_details (dict): Contains scraped job information
            resume_text (str): Text content extracted from the resume
            tone (str): Selected tone for the email
            verified_name (str, optional): User verified name to use in signature
        
        Returns:
            str: A formatted cold email with subject line and body
        """
        skills = ", ".join(job_details['primary_skills'])
        
        # Use verified name if provided, otherwise extract from resume
        candidate_name = verified_name if verified_name else self.extract_name_from_resume(resume_text)
        
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

        # Append the signature with verified name
        signature = f"\n\nBest Regards,\n{candidate_name}"
        email += signature

        return email 

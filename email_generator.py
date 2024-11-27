from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

class EmailGenerator:
    """
    A class to generate personalized cold emails for job applications.
    Uses the Groq LLM to create human-like, contextually relevant emails
    based on job details and my professional background.
    """
    
    def __init__(self):
        # Initialize Groq LLM with Mixtral model - chosen for its strong performance
        # in understanding context and generating human-like text
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name="mixtral-8x7b-32768"  # Using Mixtral for better response quality
        )
        
        # Define the email template with my personal background and achievements
        # This template is structured to create compelling cold emails that highlight
        # my relevant experience and quantifiable achievements
        self.email_template = PromptTemplate(
            input_variables=["job_title", "company", "skills", "experience"],
            template="""
            Write a professional cold email for a job application with the following details:
            Job Title: {job_title}
            Company: {company}
            Required Skills: {skills}
            Required Experience: {experience}

            # My professional background - highlighting key achievements and expertise
            # that make me stand out as a candidate
            Use the following background for the candidate:
            - 3+ years of experience as a Data Analyst specializing in SQL, Python, and behavioral analytics
            - Strong expertise in: Python, SQL, R, Tableau, Power BI, Machine Learning (scikit-learn, TensorFlow)
            - Led user behavioral analytics projects with 15% improvement in operational efficiency
            - Experience in experiment design and A/B testing, improving product launch success rates by 10%
            - Certifications in Google's Advanced Data Analytics, Stanford's Machine Learning, and Harvard's CS50
            - Strong background in data visualization, reporting automation, and cross-functional collaboration
            
            # Guidelines for email structure - ensuring each email is:
            # - Relevant to the specific job
            # - Highlights my achievements
            # - Shows my expertise
            # - Demonstrates enthusiasm
            The email should:
            1. Be concise yet highlight relevant experience matching the job requirements
            2. Emphasize quantifiable achievements (15% efficiency improvement, 10% success rate increase)
            3. Mention relevant certifications and technical expertise
            4. Show enthusiasm for the role and company's mission
            5. Include a clear call to action for next steps
            6. Keep the tone professional but engaging

            # Formatting instructions to ensure the email stands out
            Write the email with an attention-grabbing subject line that mentions the job title.
            Format the email with proper spacing and structure.
            """
        )
        
        # Create a chain that combines the LLM with our template
        # This ensures consistent email generation following our specified format
        self.chain = LLMChain(llm=self.llm, prompt=self.email_template)

    def generate_email(self, job_details):
        """
        Generates a personalized cold email based on the job details.
        
        Args:
            job_details (dict): Contains scraped job information including:
                - title: The job title
                - company: Company name
                - primary_skills: Required skills for the position
                - experience: Required experience level
        
        Returns:
            str: A formatted cold email with subject line and body
        """
        # Join the primary skills with commas for better readability in the prompt
        skills = ", ".join(job_details['primary_skills'])
        
        # Generate the email using our template and the job details
        # The LLM will create a unique email that matches both the job requirements
        # and highlights my relevant experience
        email = self.chain.run({
            "job_title": job_details['title'],
            "company": job_details['company'],
            "skills": skills,
            "experience": job_details['experience']
        })
        
        # Find the position of "sincerely" and replace everything after it
        sincerely_index = email.lower().rfind("sincerely")
        if sincerely_index != -1:
            email = email[:sincerely_index].strip()

        # Append the new signature
        signature = "\n\nBest Regards,\nManish Paneru\nwww.analystpaneru"
        email += signature

        return email 
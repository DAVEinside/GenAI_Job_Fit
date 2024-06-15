# Job Fit AI

Job Fit AI is a tool that helps job seekers tailor their resumes and cover letters to specific job descriptions. By uploading a resume and providing a job description, users can generate a customized resume and a personalized cover letter using AI.

## Features

- **Resume Customization**: Enhance your resume by integrating relevant keywords and skills based on the job description.
- **Cover Letter Generation**: Generate a personalized cover letter highlighting your suitability for the job.
- **User-Friendly Interface**: Simple and intuitive interface for uploading resumes and entering job descriptions.

## Setup

### Prerequisites

Make sure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)
- Git (for version control)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/DAVEinside/GenAI_Job_Fit.git
   cd GenAI_Job_Fit

### Install Dependencies:
pip install -r requirements.txt

### Running the Application
To run the application, use Streamlit:
streamlit run app.py

### Usage
Upload Your Resume: Upload your resume in PDF format.
Enter Job Description: Copy and paste the job description into the provided text area.
Generate Documents: Click the "Generate" button to create a tailored resume and a personalized cover letter.
Download Results: Download the generated resume and cover letter in Word format.

### Project Structure

Job_Fit_AI/
├── agents.py
├── app.py
├── llms.py
├── prompts.py
├── requirements.txt
├── streamlit_app.py
└── README.md

agents.py: Contains functions related to creating and managing AI agents.
app.py: Main application logic.
llms.py: Language model-related utilities.
prompts.py: Prompt templates for AI agents.
requirements.txt: Project dependencies.
streamlit_app.py: Streamlit application script.
README.md: Project documentation.

### Contributing
Contributions are welcome! Please create a pull request or open an issue to discuss any changes or improvements.

### License
This project is licensed under the MIT License. See the LICENSE file for more details.

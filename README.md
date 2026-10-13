\# CampusPolicy AI — College Regulations RAG Chatbot



CampusPolicy AI is a Python-based chatbot designed to help students find answers from sample college academic policies, including attendance, examination, and leave regulations.



\## Features



\- Policy retrieval using TF-IDF and cosine similarity

\- Retrieves relevant policy chunks for student questions

\- Displays policy information and similarity scores

\- Rejects questions when no relevant policy is found

\- Flask-based web interface

\- Health-check endpoint for application status



\## Technologies Used



\- Python

\- Flask

\- Scikit-learn

\- TF-IDF Vectorization

\- Cosine Similarity

\- HTML and CSS



\## Project Structure



```text

CollegePolicyChatbot/

├── app.py

├── retrieval.py

├── requirements.txt

├── data/

│   └── processed/

│       └── chunks.json

├── src/

├── static/

├── templates/

└── tests/

```



\## Getting Started



\### 1. Clone the repository



```bash

git clone https://github.com/Meenaloshani01/college-regulations-rag-chatbot.git

cd college-regulations-rag-chatbot

```



\### 2. Create a virtual environment



```bash

python -m venv .venv

```



Activate it on Windows PowerShell:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



```bash

python -m pip install -r requirements.txt

```



\### 4. Run the application



```bash

python app.py

```



Open the application in your browser:



http://127.0.0.1:5000/



Health endpoint:



http://127.0.0.1:5000/health



\## Sample Questions



\- What is the minimum attendance required for semester exams?

\- What should I do if I am absent due to illness?

\- What should I carry to the examination hall?



\## Current Implementation



The current version uses local policy data and TF-IDF-based retrieval. It does not yet use a large language model for answer generation or Amazon Bedrock for embeddings.



\## Future Enhancements



\- Store policy documents in Amazon S3

\- Add semantic embeddings for improved retrieval

\- Integrate a large language model for grounded answer generation

\- Add document upload and processing workflows

\- Deploy the application on AWS

\- Expand automated tests for retrieval and API endpoints



\## Disclaimer



The included academic policies are sample demonstration documents and should not be treated as official college regulations.


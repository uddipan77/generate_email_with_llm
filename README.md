## Overview
🚀 **Gen-AI Powered Cold Email Generator** – Revolutionizing business outreach with AI!  

Welcome to the future of business communication! Our **AI-driven Cold Email Generator** is designed to craft highly personalized and impactful emails by analyzing job descriptions scraped from company career pages. 

### Key Features:
- **Personalized Emails**: Tailored to match job descriptions and company profiles.
- **High Engagement**: Boosts response rates and conversions.
- **Efficient Workflow**: Streamlines your outreach process.

Leveraging the power of **LLama-3.3, Groq Cloud, LangChain, and ChromaDB**, this tool intelligently extracts job postings and formulates professional cold emails that enhance engagement and conversion rates. Whether you're an AI enthusiast, business development professional, or recruiter, this tool streamlines communication, making outreach more **efficient, scalable, and results-driven**!  

## Cover Image
![Cover Image](<output_cold_email.png>)

## Tech Stack
- 🧠 **LLama-3.3-70B** (via Groq Cloud) - LLM used for job extraction & email generation
- 🔗 **LangChain** - Prompt engineering and AI pipeline
- 🗃️ **ChromaDB** - Vector database for portfolio management
- 🐍 **Python** - Backend scripting
- 🔒 **dotenv** - Secure API key management

## Project Structure
```
cold-email-generator/
│── app/  
│   │── resource/          # Contains necessary data files like portfolio.csv
│   │── .env               # Stores environment variables like API Key
│   │── chains.py          # AI processing logic (job extraction & email generation)  
│   │── main.py            # Main script for execution  
│   │── portfolio.py       # Portfolio data storage & retrieval via ChromaDB  
│   │── utils.py           # Utility functions (text cleaning, preprocessing)  
│── requirements.txt       # Python dependencies  
│── README.md              # Project documentation
```

## Installation
### 📥 Clone the Repository
```bash
git clone https://github.com/uddipan77/generate_email_with_llm.git
cd COLD-EMAIL-GENERATOR
```

### 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application
### 🚀 To start the application, navigate to the app folder and run the command below in the terminal:
```bash
python app/main.py --config /path/to/config.yaml
```

## Notes
- 🔑 **API Key**: Make sure to update the `.env` file with your API key according to your model.





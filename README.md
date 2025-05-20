# smart-research-assistant
SmartScholar is an intelligent, multi-tool research assistant powered by Google's Gemini and LangChain. It answers user questions using both historical information (Wikipedia) and real-time data (Tavily) — perfect for students, researchers, or anyone looking for accurate and up-to-date information.

## Features

* Wikipedia Search – Retrieves reliable, factual summaries and historical information
* Tavily Web Search – Finds recent and real-time information from trusted online sources
* Concept Explainer Tool *(coming soon)* – Explains topics at simple, intermediate, or expert levels
* Math Tool – Safely solves numeric and algebraic expressions
* Conversational Memory – Maintains context across multiple turns
* Gemini LLM – Uses Google's Gemini (via LangChain) for fast and intelligent responses
* Terminal-Based Chat – Interactive chat loop through the command line

---

## Tech Stack

* LangChain – Agent and tool orchestration
* Google Gemini – Language model integration via `langchain-google-genai`
* Tavily API – Real-time web search
* Wikipedia API – Access to encyclopedic content
* Python-dotenv – Environment variable management

---

## 1. Installation

```bash
git clone https://github.com/Ekuaappiah/smart-research-assistant.git
cd smart-research-assistant
```


### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a .env file in the root directory:

```bash
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 5. Run the project:
```bash
python main.py
```
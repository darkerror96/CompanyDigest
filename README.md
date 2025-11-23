# 🚀 CompanyDigest – Your GoTo AI Financial Summarizer

CompanyDigest is an AI Concierge Agent built for the Google x Kaggle AI Intensive Capstone.  
It automatically gathers **financial data**, **latest news**, and **web insights** about any publicly traded company and
produces a concise, easy-to-read summary. Instead of checking multiple websites manually, users can simply ask the
agent, and it fetches everything they need in
seconds.

This project is **not a financial advisor**—it only collects and summarizes publicly available information so users can
stay informed before making their own decisions.

---

## 📌 Project Summary

CompanyDigest simplifies the daily research workflow for investors, students, and anyone curious about a company's
performance.

The agent pulls data from:

- **Yahoo Finance** (stock metrics & fundamentals)
- **Google Search API** (company info & trending topics)
- **GNews APIs** (latest relevant articles)

It processes all sources, cleans the results, and produces a **single consolidated briefing** so users never need to
visit multiple websites again. Designed as a personal AI assistant, this agent focuses on convenience, accuracy, and
simplicity.

---

## 🛠️ Tech Stack

- Python
- Yahoo Finance API
- Google Search API
- GNews API (Google News API)
- LLM-based reasoning & tool orchestration

---

## 📦 Installation

### **1. Clone the Repository**

```bash
git clone https://github.com/darkerror96/CompanyDigest.git
cd companydigest
```

### **2. Create a Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
venv\Scripts\activate      # Windows
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Add API Keys**

Update .env file in the project root:

```ini
GOOGLE_API_KEY = your_key_here
NEWS_API_KEY = your_key_here
```

---

## 📦 How to Run

```bash
adk run CompanyDigest
```

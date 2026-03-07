# 🚀 TrendAura AI: Autonomous Auto-Blogging Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![AI Model](https://img.shields.io/badge/AI-LLaMA_3.1_(8B)-orange.svg)
![Deployment](https://img.shields.io/badge/Deployed_on-Render-success.svg)
![Status]([https://img.shields.io/badge/Status-24%x2F7_Active-brightgreen.svg](https://voice-gta.onrender.com/))

## 📌 Project Overview
TrendAura AI is a fully autonomous, serverless content generation and publishing engine. It eliminates manual blogging workflows by continuously monitoring viral internet trends, synthesizing the data using a Large Language Model (LLM), generating SEO-optimized HTML articles with AI-generated thumbnails, and publishing them directly to Google Blogger. 

The entire pipeline is orchestrated remotely via a **Telegram Bot interface** and runs 24/7 on a cloud architecture.

## ✨ Core Features
- **🤖 Remote Command & Control:** Trigger the entire content generation pipeline from anywhere using a simple `/post` command on Telegram.
- **📈 Viral Trend Scraping:** Automatically fetches the top daily discussions from highly active Reddit communities (`r/technology`, `r/gaming`, `r/movies`).
- **🧠 Advanced AI Synthesis:** Utilizes the **Groq API (LLaMA 3.1 8B)** to write highly opinionated, 1000-word articles. Prompt engineering ensures the output is strictly valid HTML (bypassing Markdown) for seamless CMS integration.
- **🎨 Dynamic AI Thumbnails:** Extracts contextual prompts from the article to generate copyright-free cover images via `pollinations.ai`, automatically formatting them to trigger Blogger's native thumbnail detector.
- **🛡️ Anti-Duplication Memory Engine:** A local state-management system (`posted_history.txt`) cross-references every fetched trend to ensure zero duplicate posts.
- **☁️ 24/7 Serverless Uptime:** Uses a dual-threaded Flask web server integrated with UptimeRobot to bypass free-tier cloud sleep restrictions.

## 🏗️ System Architecture & Data Flow

1. **Trigger:** User sends `/post` via Telegram Bot.
2. **Ingestion:** Python backend scrapes Reddit RSS feeds and bypasses bot-blockers using custom User-Agents.
3. **Validation:** Checks `posted_history.txt` to prevent duplicate content.
4. **Generation:** - Groq API generates a structured HTML article.
   - Regex parses `<TITLE>`, `<LABEL>`, and `<IMAGE_PROMPT>` tags.
   - Requests library "pre-loads" the generated AI image to cache it on the server.
5. **Publishing:** Google API Client authenticates via OAuth 2.0 (`token.pickle`) and pushes the final HTML payload to Blogger.
6. **Notification:** Telegram Bot replies with the live URL of the published blog post.

## 🛠️ Technology Stack
* **Language:** Python 3.11
* **AI Engine:** Meta LLaMA 3.1 (via Groq API), Pollinations AI
* **Libraries:** `telebot`, `feedparser`, `requests`, `google-api-python-client`, `Flask`, `re`
* **Cloud & DevOps:** Render (PaaS), UptimeRobot, GitHub

## 🚀 Installation & Setup (Local)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/TrendAura-Bot.git](https://github.com/yourusername/TrendAura-Bot.git)
   cd TrendAura-Bot

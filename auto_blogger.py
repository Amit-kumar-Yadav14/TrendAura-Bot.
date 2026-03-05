import os
import pickle
import feedparser
import re
import urllib.parse
import requests
import telebot # NAYA: Telegram library
from flask import Flask        # NAYA
from threading import Thread   # NAYA
from googleapiclient.discovery import build
from groq import Groq
# ==========================================
# ⚙️ CONFIGURATION 
# ==========================================
BLOG_ID = '54301321397959393' 
GROQ_API_KEY = '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' 
TELEGRAM_BOT_TOKEN = '8643823233:AAF_3hqNR_f9nwljCh-BxcV7LdYcq2-73vE'
# ==========================================

os.environ["GROQ_API_KEY"] = GROQ_API_KEY
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def get_latest_news():
    print("\n🔥 Reddit Trends scan kar raha hoon aur Memory check kar raha hoon...")
    
    # Ek text file jisme hum purani posts ka record rakhenge
    history_file = "posted_history.txt"
    
    # Purani posts ki list padh rahe hain (agar file exist karti hai)
    posted_links = []
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            posted_links = f.read().splitlines()
            
    url = "https://www.reddit.com/r/technology+gaming+movies/top/.rss?t=day"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        feed = feedparser.parse(response.content)
        
        # Ab hum blindly [0] nahi uthayenge, balki list mein ek-ek karke check karenge!
        for entry in feed.entries:
            # Agar ye link humari history mein NAHI hai, toh isko pakad lo
            if entry.link not in posted_links:
                news_data = {
                    "title": entry.title, 
                    "link": entry.link,
                    "summary": f"This is a highly discussed viral topic on Reddit: {entry.title}. Write a comprehensive, opinionated, and viral deep-dive blog post about it."
                }
                
                # Is naye link ko history file mein save kar lo taaki agli baar repeat na ho
                with open(history_file, "a", encoding="utf-8") as f:
                    f.write(entry.link + "\n")
                    
                print(f"🚀 Fresh Reddit Trend Mil Gaya: '{news_data['title']}'")
                return news_data
        
        # Agar loop khatam ho gaya aur saari posts pehle hi daali ja chuki hain:
        raise Exception("Boss, Reddit ki saari top posts tu already chhap chuka hai! Thode ghante baad naya maal aane par try karna.")
            
    except Exception as e:
        raise Exception(f"Reddit Error ya History Issue: {e}")

def generate_dynamic_article(news_data):
    print("🧠 AI 1000-word Strict HTML article likh raha hai...")
    client = Groq()
    
    prompt = f"""
    You are an elite journalist and an expert HTML coder for 'TrendAura'.
    Write a comprehensive 800-1000 word article based on this news:
    
    Original Title: {news_data['title']}
    Summary: {news_data['summary']}
    Source Link: {news_data['link']}

    ABSOLUTE RULES (FAILURE IS NOT AN OPTION):
    1. YOU MUST OUTPUT 100% VALID HTML. NO MARKDOWN AT ALL.
    2. PARAGRAPHS: Every single paragraph MUST be wrapped in <p> and </p>. Do not leave plain text.
    3. HEADINGS: Use <h2> and <h3> for all subheadings.
    4. LISTS: If you use bullet points, you MUST use <ul> and <li> tags. Do NOT use dashes (-) or asterisks (*).
    5. LINK: Embed this exact link <a href="{news_data['link']}">Read Official Source</a> naturally inside a <p> tag.

    OUTPUT FORMAT:
    <LABEL>Tech</LABEL>
    <TITLE>Your Catchy Title Here</TITLE>
    <IMAGE_PROMPT>futuristic technology glowing neon</IMAGE_PROMPT>
    <CONTENT>
    <h2>Introduction</h2>
    <p>Your first paragraph here...</p>
    <h2>Key Details</h2>
    <ul>
       <li>First point here</li>
       <li>Second point here</li>
    </ul>
    <p>Another paragraph here...</p>
    </CONTENT>
    """
    
    # Temperature 0.3 kiya hai taaki wo strict rules follow kare aur format na tode
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant", 
        temperature=0.3, 
    )
    return response.choices[0].message.content

def publish_to_blogger(title, content, category_label):
    print(f"🌐 TrendAura par '{category_label}' category mein publish ho raha hai...")
    
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
        
    service = build('blogger', 'v3', credentials=creds)
    
    post_data = {
        'title': title,
        'content': content,
        'labels': [category_label, 'TrendAura Exclusive', 'Deep Dive'] 
    }
    
    try:
        request = service.posts().insert(blogId=BLOG_ID, body=post_data, isDraft=False)
        result = request.execute()
        print(f"✅ BOOM! Article Live: {result['url']}")
    except Exception as e:
        print(f"❌ Error aagaya: {e}")

if __name__ == '__main__':
    print("🚀 TrendAura Pro Auto-Bot Started!\n" + "="*40)
    
    news = get_latest_news()
    ai_raw_output = generate_dynamic_article(news)
    
    try:
        label_match = re.search(r'<(?:LABEL|TAG)>(.*?)</(?:LABEL|TAG)>', ai_raw_output, re.IGNORECASE | re.DOTALL)
        title_match = re.search(r'<TITLE>(.*?)</TITLE>', ai_raw_output, re.IGNORECASE | re.DOTALL)
        image_match = re.search(r'<(?:IMAGE_PROMPT|IMAGE)>(.*?)</(?:IMAGE_PROMPT|IMAGE)>', ai_raw_output, re.IGNORECASE | re.DOTALL)
        content_match = re.search(r'<CONTENT>(.*?)</CONTENT>', ai_raw_output, re.IGNORECASE | re.DOTALL)
        
        dynamic_label = label_match.group(1).strip() if label_match else "Trending News"
        dynamic_title = title_match.group(1).strip() if title_match else f"🔥 TrendAlert: {news['title']}"
        raw_prompt = image_match.group(1).strip() if image_match else "technology abstract digital news"
        
        if content_match:
            content_html = content_match.group(1).strip()
            # Safety cleanup: Remove stray markdown if AI still disobeys
            content_html = content_html.replace('**', '')
        else:
            print("❌ AI ne <CONTENT> tag nahi diya, skip kar raha hoon.")
            exit()

        # 🎨 AI IMAGE FIX (Blogger Native Format)
        clean_prompt = re.sub(r'[^a-zA-Z0-9\s]', '', raw_prompt).strip()
        safe_prompt = clean_prompt.replace(' ', '%20')
        
        # .jpg lagana zaroori hai Blogger ke liye
        image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}.jpg"
        print(f"🖼️ Generated Image URL: {image_url}") 
        
        # Ekdum original Blogger format jo tune diya hai
        thumbnail_html = f'''
        <div class="separator" style="clear: both;">
            <a href="{image_url}" style="display: block; padding: 1em 0; text-align: center;">
                <img alt="{dynamic_title}" border="0" width="600" data-original-height="630" data-original-width="1200" src="{image_url}" style="border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);"/>
            </a>
        </div>
        '''
        
        final_content = thumbnail_html + content_html
        
        publish_to_blogger(dynamic_title, final_content, dynamic_label)
            
    except Exception as e:
        print("❌ System Error:", e)
        

    
# NAYA: Telegram Command Handler
@bot.message_handler(commands=['post'])
def send_post_from_phone(message):
    bot.reply_to(message, "🚀 Boss ka order mil gaya! Latest news dhoondh kar post bana raha hoon. 1-2 minute wait karo...")
    
    try:
        # Pura process yahan chalega
        news = get_latest_news()
        bot.send_message(message.chat.id, f"📰 Khabar mil gayi: '{news['title']}'. AI likhna shuru kar raha hai...")
        
        ai_raw_output = generate_dynamic_article(news)
        
        # Tags nikalne wala tera logic
        label_match = re.search(r'<(?:LABEL|TAG)>(.*?)</(?:LABEL|TAG)>', ai_raw_output, re.IGNORECASE | re.DOTALL)
        title_match = re.search(r'<TITLE>(.*?)</TITLE>', ai_raw_output, re.IGNORECASE | re.DOTALL)
        content_match = re.search(r'<CONTENT>(.*?)</CONTENT>', ai_raw_output, re.IGNORECASE | re.DOTALL)
        
        dynamic_label = label_match.group(1).strip() if label_match else "Trending News"
        dynamic_title = title_match.group(1).strip() if title_match else f"🔥 TrendAlert: {news['title']}"
        
        if content_match:
            content_html = content_match.group(1).strip()
            content_html = content_html.replace('**', '')
            
            publish_to_blogger(dynamic_title, content_html, dynamic_label)
            
            # Jab kaam ho jaye, toh phone par success message bhej do!
            bot.send_message(message.chat.id, f"✅ BOOM! Post Live Ho Gayi Boss!\n\nTitle: {dynamic_title}\nJaa kar blog check kar lo.")
        else:
            bot.send_message(message.chat.id, "❌ Error: AI ne format theek se nahi diya.")
            
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Bhai ek error aagaya: {e}")

# Script ko lagatar chalate rehne ke liye taaki wo Telegram messages sunta rahe
if __name__ == '__main__':
    print("🤖 Telegram Bot is ONLINE! Apne phone se '/post' message bhejo...")
    bot.infinity_polling()

    app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 TrendAura Bot is ALIVE and RUNNING 24/7!"

def run_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_server)
    t.start()

# ==========================================
# 🤖 TELEGRAM BOT EXECUTION
# ==========================================
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['post'])
def send_post_from_phone(message):
    # (Tera Telegram wala purana code yahan aayega)
    pass

if __name__ == '__main__':
    print("🌐 Starting Fake Web Server for 24/7 Uptime...")
    keep_alive() # Ye server ko zinda rakhega
    
    print("🤖 Telegram Bot is ONLINE! Apne phone se '/post' message bhejo...")
    bot.infinity_polling()
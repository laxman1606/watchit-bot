import telebot
import os
import threading
from flask import Flask

# 🚀 SECURE: Token ko code me mat likho, Render se uthao
API_TOKEN = os.environ.get('BOT_TOKEN') 
bot = telebot.TeleBot(API_TOKEN)

# ... (baaki ka code waisa hi rahega)

# 2. RENDER SERVER (Zinda rakhne ke liye)
app = Flask(__name__)
@app.route('/')
def home(): return "WATCHit Bot is Running!"

# 🚀 3. YT-DLP MASTER LOGIC
def get_video_url(url):
    ydl_opts = {
        'format': 'best', # Best quality stream nikaalega
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            # TeraBox ya kisi bhi site se direct URL nikalna
            return info.get('url')
        except Exception as e:
            return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "WATCHit Bot is Active! 🍿\nSend any Social Media link, I will extract the video link for you!")

@bot.message_handler(func=lambda message: True)
def process_link(message):
    url = message.text.strip()
    msg = bot.reply_to(message, "⏳ Extracting video link... please wait...")
    
    # URL Extract karna
    direct_url = get_video_url(url)
    
    if direct_url:
        # 🚀 Ab link ko WATCHit app ke scheme me wrap kar do
        import urllib.parse
        safe_url = urllib.parse.quote(direct_url, safe='')
        app_link = f"watchitapp://play?url={safe_url}"
        
        # HTML me chhupe hue link ka button
        response = f"""🎬 *Video Extracted!* 🎬\n\nClick below to play:\n\n👉 <a href="{app_link}"><b>▶️ PLAY IN WATCHit APP</b></a>"""
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=response, parse_mode="HTML")
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="❌ Error: Video link extract nahi ho paya. Website link unsupported ho sakti hai.")

# 4. START BOT
if __name__ == "__main__":
    threading.Thread(target=lambda: bot.polling(non_stop=True)).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

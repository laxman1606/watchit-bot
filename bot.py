import telebot
import os
import threading
from flask import Flask
from terabox_dl import TeraboxDL
import urllib.parse

API_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# TeraBox Downloader Instance
tb = TeraboxDL()

@app.route('/')
def home(): return "WATCHit Bot is Active! 🚀"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "TeraBox/Social Media Video Extractor is Ready! 🍿\nSend me a link.")

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    url = message.text.strip()
    msg = bot.reply_to(message, "🔍 Scanning TeraBox/Diskwala link...")
    
    try:
        # 🚀 APROXIMATE BYPASS: TeraBox link se Direct stream URL nikalna
        video_data = tb.get_video_data(url) # Yeh function Terabox-dl library ka hai
        
        if video_data and 'video_url' in video_data:
            direct_url = video_data['video_url']
            
            # App me play karne wala Deep Link
            safe_url = urllib.parse.quote(direct_url, safe='')
            app_link = f"watchitapp://play?url={safe_url}"
            
            response = f"""🎬 *Video Found!* 🎬\n\nDirect Stream URL: {direct_url[:50]}...\n\n👉 <a href="{app_link}"><b>▶️ PLAY IN WATCHit APP</b></a>"""
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=response, parse_mode="HTML")
        else:
            bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="❌ Error: Ye link support nahi ho raha hai. TeraBox link public hona chahiye.")
            
    except Exception as e:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=f"❌ Error: {str(e)}")

# Server Start
if __name__ == "__main__":
    threading.Thread(target=lambda: bot.polling(non_stop=True)).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

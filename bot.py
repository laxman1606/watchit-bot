import telebot
import urllib.parse
import os
import threading
import yt_dlp
from flask import Flask, request

# 🚀 RENDER ENVIRONMENT VARIABLES (Lalachi Developer Security)
API_TOKEN = os.environ.get('BOT_TOKEN', 'TOKEN_NOT_FOUND')
RENDER_WEBSITE_URL = os.environ.get('RENDER_URL', 'URL_NOT_FOUND')

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# --- 1000x ADVANCE BYPASS ENGINE ---
def get_direct_mp4_link(url):
    """
    Ye function website ke andar ghus kar asli .mp4 ya .m3u8 nikalta hai.
    Works for: YouTube, Instagram, Facebook, Twitter, and 1000+ sites.
    """
    ydl_opts = {
        'format': 'best', # Sabse high quality video nikalega
        'quiet': True,
        'no_warnings': True,
        'simulate': True, # Video download nahi karega, sirf link churayega
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Asli direct server link return karega
            return info.get('url', url)
    except Exception as e:
        print(f"Bypass Engine Failed for {url} : {e}")
        # Agar bypass fail hua, toh original link hi bhej do
        return url

# --- WEB SERVER (Auto Redirect) ---
@app.route('/')
def home():
    return "WATCHit Premium Bypass Server is Live! 😈"

@app.route('/play')
def redirect_to_app():
    video_url = request.args.get('url', '')
    if not video_url:
        return "No video link found!"

    safe_url = urllib.parse.quote(video_url, safe='')
    app_link = f"watchitapp://play?url={safe_url}"

    # Ekdum Hacker Style Auto-Redirect Page
    html_page = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Loading Video...</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ background-color: #000; color: #00FF00; text-align: center; font-family: monospace; padding-top: 50px; }}
            .loader {{ border: 5px solid #111; border-top: 5px solid #00FF00; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto; }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
            a {{ display: inline-block; padding: 15px 30px; background-color: #00FF00; color: #000; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 30px; }}
        </style>
    </head>
    <body>
        <h2>Bypassing Security & Opening WATCHit...</h2>
        <div class="loader"></div>
        <br>
        <a href="{app_link}">Force Open App</a>
        <script>
            setTimeout(function() {{ window.location.href = "{app_link}"; }}, 500);
        </script>
    </body>
    </html>
    """
    return html_page

# --- TELEGRAM BOT LOGIC ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "😈 **WATCHit VIP Bot** 😈\n\nBhej apna link (YouTube, Insta, etc.). Main uski security tod kar direct app me chalaunga!")

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    processing_msg = bot.reply_to(message, "⏳ *Bypassing security... Extracting direct stream...*", parse_mode="Markdown")
    
    original_url = message.text.strip()
    
    # 🚀 ENGINE START: Asli link nikalna
    direct_mp4_url = get_direct_mp4_link(original_url)
    
    safe_url = urllib.parse.quote(direct_mp4_url, safe='')
    
    # Render website link generate karna
    website_link = f"{RENDER_WEBSITE_URL}/play?url={safe_url}"
    
    response_msg = f"""🎬 <b>Direct Stream Extracted!</b> 🎬

System bypassed successfully. Play now in Ultra HD:

👉 <a href="{website_link}"><b>▶️ PLAY IN WATCHit APP</b></a> 👈"""

    bot.edit_message_text(chat_id=message.chat.id, message_id=processing_msg.message_id, text=response_msg, parse_mode="HTML")

# --- SERVER START ---
def run_bot():
    print("Bot is running...")
    bot.polling(non_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

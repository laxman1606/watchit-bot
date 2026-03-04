import telebot
import urllib.parse
import os
import threading
from flask import Flask, request

# 🚀 1. APNA ASLI BOT TOKEN YAHAN DAALEIN
API_TOKEN = '8516164180:AAFTn62ylXWc0PytqpQP5AfD4RghbbCFpcM'
bot = telebot.TeleBot(API_TOKEN)

# 🚀 2. APNI RENDER WEBSITE KA LINK YAHAN DAALEIN (Aakhiri me / mat lagana)
# Example: 'https://watchit-bot.onrender.com'
RENDER_WEBSITE_URL = 'https://watchit-bot.onrender.com'

app = Flask(__name__)

# --- WEB SERVER LOGIC (Ye app open karwayega) ---
@app.route('/')
def home():
    return "WATCHit Bot Server is Running! 🚀"

@app.route('/play')
def redirect_to_app():
    # Ye page 1 second ke liye khulega aur direct App open kar dega
    video_url = request.args.get('url', '')
    if not video_url:
        return "No video link found!"

    safe_url = urllib.parse.quote(video_url, safe='')
    app_link = f"watchitapp://play?url={safe_url}"

    # Mast Black color ka HTML page jo auto-redirect karega
    html_page = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Opening WATCHit...</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ background-color: #121212; color: white; text-align: center; font-family: sans-serif; padding-top: 50px; }}
            a {{ display: inline-block; padding: 15px 30px; background-color: #2196F3; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h2>Opening in WATCHit Player... 🍿</h2>
        <p>If the app doesn't open automatically, click the button below:</p>
        <a href="{app_link}">Open WATCHit App</a>

        <script>
            // 1 second me apne aap App khol dega
            setTimeout(function() {{
                window.location.href = "{app_link}";
            }}, 500);
        </script>
    </body>
    </html>
    """
    return html_page


# --- TELEGRAM BOT LOGIC ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to WATCHit Bot! 🍿\nMujhe koi bhi direct video link bhejo, main usko WATCHit App me play karne wala link bana dunga.")

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    original_url = message.text.strip()
    safe_url = urllib.parse.quote(original_url, safe='')
    
    # 🚀 JADOO YAHAN HAI: Ab bot aapko aapki RENDER website ka link dega (Jo 100% Clickable hoga)
    website_link = f"{RENDER_WEBSITE_URL}/play?url={safe_url}"
    
    response_msg = f"""🎬 *Ready to Play!* 🎬

Click the link below to watch this video directly in your app:

👉 {website_link}

_(Note: Agar app installed nahi hai, toh pehle PlayStore se download karein)_"""

    bot.reply_to(message, response_msg, parse_mode="Markdown")

# --- START SERVER & BOT ---
def run_bot():
    print("Telegram Bot is running...")
    bot.polling(non_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

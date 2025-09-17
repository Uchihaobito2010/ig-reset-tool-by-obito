import requests
import telebot
import random
import uuid
import json
from flask import Flask
import threading
import os


app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"


TOKEN = "8447364267:AAGF72q73J_BpYZmjkiR_zpeWDB8s_M-1P0"  
bot = telebot.TeleBot(TOKEN)


MID = "ZVfGvgABAAGoQqa7AY3mgoYBV1nP"
CSRF_TOKEN = "9y3N5kLqzialQA7z96AMiyAKLMBWpqVj"


def generate_user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    return random.choice(agents)

   
def send_reset_link(user_input, message):
    url = "https://i.instagram.com/api/v1/accounts/send_password_reset/"
    payload = {
        'user_email': user_input,
        'ig_sig_key_version': "4",
        'device_id': str(uuid.uuid4()),
    }
    headers = {
        'User-Agent': generate_user_agent(),
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Accept-Language': "en-US",
        'X-IG-Connection-Type': "WIFI",
        'X-IG-Capabilities': "AQ==",
        'Cookie': f"mid={MID}; csrftoken={CSRF_TOKEN}",
        'X-CSRFToken': CSRF_TOKEN
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        response_json = response.json()
        print(f"API Response: {json.dumps(response_json, indent=2)}")
        if response.status_code == 200 and 'obfuscated_email' in response_json:
            bot.reply_to(message, f"✅ Password reset link {response_json['obfuscated_email']} pe bhej diya gaya! Apna email check karo.")
        else:
            error_message = response_json.get('message', 'Unknown error')
            bot.reply_to(message, f"⚠️ Error: {error_message}. Username ya email check karo.")
    except Exception as e:
        print(f"Exception: {str(e)}")
        bot.reply_to(message, f"❌ Kuch toh gadbad hai: {str(e)}. Thodi der baad try karo.")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hlo 😁 Me @Maskpy ka bot hu mujhe use krne ke lie liye /reset <username ya email> daalo Fast😎 im also @Zekepy @Vegetapy click to contect me.")

@bot.message_handler(commands=['reset'])
def handle_reset(message):
    try:
        command_parts = message.text.split()
        if len(command_parts) < 2:
            bot.reply_to(message, "⚠️ Username ya email do. Example ke lie :- /reset example@gmail.com")
            return
        user_input = command_parts[1].strip()
        bot.reply_to(message, f"🔄 {user_input} ke liye reset link bhej raha hoon...")
        send_reset_link(user_input, message)
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")


def run_flask():
    port = int(os.environ.get("PORT", 8080))  
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    bot.polling(none_stop=True)
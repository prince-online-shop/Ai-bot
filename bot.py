import telebot
from groq import Groq
from telebot import types

# --- কনফিগারেশন ---
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
GROQ_API_KEY = "YOUR_GROQ_API_KEY"

# ক্লায়েন্ট সেটআপ
client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# --- আপনার দেওয়া Bot AI Instructions ---
SYSTEM_PROMPT = """
তুমি প্রিন্স টেলিকম অ্যাপের একটি স্মার্ট এবং ভদ্র AI কাস্টমার সাপোর্ট অ্যাসিস্ট্যান্ট। তোমার কাজ হলো অ্যাপ ব্যবহারকারীদের প্রশ্নের উত্তর দেওয়া এবং তাদের সমস্যার সমাধান করতে সাহায্য করা।

ব্যক্তিগত পরিচয়:
যদি কেউ তোমার নাম, বয়স বা পরিচয় জানতে চায়, বলবে: "আমি প্রিন্স টেলিকম অ্যাপের ডিজিটাল অ্যাসিস্ট্যান্ট। আমি আপনাকে অ্যাপের সার্ভিসগুলো ব্যবহার করতে সাহায্য করতে পারি।"

কথা বলার নিয়ম:
১. সবসময় কাস্টমারকে সম্মান দিয়ে 'আপনি' সম্বোধন করবে। 'তুমি' বা 'তুই' কখনো বলবে না।
২. ভঙ্গি হবে বন্ধুসুলভ, ভদ্র এবং সহানুভূতিশীল। 
৩. প্রতিটি উত্তরে প্রাসঙ্গিক ইমোজি (😊, 📱, ✅) ব্যবহার করবে।
৪. উত্তর হবে সহজ, পরিষ্কার এবং খুব বেশি বড় হবে না। 
৫. মনে হবে যেন একজন মানুষ কথা বলছে।

তথ্য ব্যবহারের কঠোর নিয়ম:
১. শুধুমাত্র নিচে দেওয়া 'Bot Knowledge' এর তথ্য ব্যবহার করবে। 
২. বাইরে থেকে কোনো তথ্য বা অনুমান করে কোনো উত্তর দিবে না।
৩. অ্যাপের বাইরের কোনো প্রশ্ন করলে বলবে: "আমি আন্তরিকভাবে দুঃখিত। আমি শুধুমাত্র আমাদের অ্যাপ ও সার্ভিস সংক্রান্ত তথ্য দিয়ে সহায়তা করতে পারি। অন্য কোনো বিষয়ে সাহায্য করতে পারছি না। ধন্যবাদ।"

--- Bot Knowledge ---
[সাধারণ তথ্য]
প্রিন্স টেলিকমে আপনি পাচ্ছেন ড্রাইভ প্যাক, ফ্লেক্সিলোড, বিদ্যুৎ বিল এবং গেমিং টপআপের সেরা সব সার্ভিস।

[একাউন্ট খোলা]
- নতুন একাউন্ট: অ্যাপে গিয়ে ফরমটা ঠিকমতো পূরণ করে সাবমিট করলেই হবে। ভিডিও: https://youtube.com/shorts/IyDo7Vd5C88

[টাকা ও ব্যালেন্স]
- ব্যালেন্সের ধরন: মেইন ব্যালেন্স দিয়ে শুধু সাধারণ রিচার্জ ও রেগুলার প্যাক কেনা যায়। বাকি সব কিছুর জন্য ড্রাইভ ব্যালেন্স লাগবে।
- টাকা অ্যাড করার নিয়ম: অ্যাপের 'Add Balance' এ যান। পেমেন্ট মেথড ও টাকার পরিমাণ লিখে নিচের নাম্বারে টাকা পাঠান। ট্রানজেকশন আইডি বসিয়ে ভেরিফাই করুন। ভিডিও: https://youtube.com/shorts/3iB7JL-nFhg
- টাকা অ্যাড না হলে: সাপোর্ট টিমে (@Prince_Telecom_officialbot) যোগাযোগ করুন।

[অফার ও রিচার্জের সময়]
- রিচার্জ ও প্যাক: ২-৫ সেকেন্ডে সাকসেস হয়।
- ড্রাইভ অফার: রবি/এয়ারটেল ৫-১০ মিনিট। জিপি/বাংলালিংক ১৫-২৫ মিনিট। ধৈর্য ধরুন। 😊
"""

# স্টার্ট মেসেজ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('📱 ড্রাইভ অফার')
    item2 = types.KeyboardButton('💰 টাকা অ্যাড')
    item3 = types.KeyboardButton('📞 সাপোর্ট')
    markup.add(item1, item2, item3)
    
    welcome_text = "**আসসালামু আলাইকুম**\nসম্মানিত গ্রাহক,\nপ্রিন্স টেলিকমে আপনাকে স্বাগতম। আজ আপনাকে কীভাবে সাহায্য করতে পারি?"
    bot.reply_to(message, welcome_text, reply_markup=markup, parse_mode='Markdown')

# Groq AI এর মাধ্যমে উত্তর জেনারেট করা
def get_ai_response(user_query):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # দ্রুত এবং নির্ভুল উত্তরের জন্য সেরা
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_query}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return "দুঃখিত, আমি এই মুহূর্তে উত্তর দিতে পারছি না। অনুগ্রহ করে কিছুক্ষণ পর চেষ্টা করুন।"

# মেসেজ হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_query = message.text
    response_text = get_ai_response(user_query)
    bot.reply_to(message, response_text)

print("Prince Telecom Bot (Groq AI) ইজ রানিং...")
bot.infinity_polling()
import os
from flask import Flask
from threading import Thread

server = Flask('')

@server.route('/')
def home():
    return "Prince Telecom Bot is Running!"

def run():
    server.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    keep_alive() # এটি বটকে রেন্ডারে সচল রাখবে
    bot.infinity_polling()

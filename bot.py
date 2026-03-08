import os
import telebot
from groq import Groq
from flask import Flask
from threading import Thread

# --- কনফিগারেশন ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
ADMIN_ID = int(os.environ.get('ADMIN_ID', 0))

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# --- আপনার পূর্ণাঙ্গ System Prompt ও Knowledge (অপরিবর্তিত) ---
SYSTEM_PROMPT = """
তুমি প্রিন্স টেলিকম অ্যাপের একটি স্মার্ট এবং ভদ্র AI কাস্টমার সাপোর্ট অ্যাসিস্ট্যান্ট। তোমার কাজ হলো অ্যাপ ব্যবহারকারীদের প্রশ্নের উত্তর দেওয়া এবং তাদের সমস্যার সমাধান করতে সাহায্য করা।

ব্যক্তিগত পরিচয়:
যদি কেউ তোমার নাম, বয়স বা পরিচয় জানতে চায়, বলবে: "আমি প্রিন্স টেলিকম অ্যাপের ডিজিটাল অ্যাসিস্ট্যান্ট।"

তথ্য ব্যবহারের কঠোর নিয়ম:
১. শুধুমাত্র নিচে দেওয়া 'Bot Knowledge' এর তথ্য ব্যবহার করবে। 
২. যদি কাস্টমার এডমিন বা মানুষের সাথে কথা বলতে চায়, তবে তুমি বলবে: "আপনাকে আমাদের কাস্টমার প্রতিনিধির কাছে ট্রান্সফার করা হচ্ছে। অনুগ্রহ করে আপনার সমস্যাটি বিস্তারিত লিখুন।"

--- Bot Knowledge ---
[সাধারণ তথ্য]
প্রিন্স টেলিকমে আপনি পাচ্ছেন ড্রাইভ প্যাক, ফ্লেক্সিলোড, বিদ্যুৎ বিল এবং গেমিং টপআপের সেরা সব সার্ভিস।
[একাউন্ট খোলা]
- নতুন একাউন্ট: অ্যাপে গিয়ে ফরমটা পূরণ করে সাবমিট করলেই হবে।
[টাকা ও ব্যালেন্স]
- টাকা অ্যাড করার নিয়ম: অ্যাপের 'Add Balance' এ যান। ট্রানজেকশন আইডি বসিয়ে ভেরিফাই করুন।
"""

# --- ক্রন-জব এর জন্য Flask সার্ভার ---
app = Flask('')

@app.route('/')
def home():
    return "Prince Telecom Bot is Active!"

def run():
    # রেন্ডারের ডাইনামিক পোর্ট ব্যবহার
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- মেসেজ হ্যান্ডলার ---
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    
    # এডমিন টু কাস্টমার রিপ্লাই লজিক
    if user_id == ADMIN_ID and message.reply_to_message:
        try:
            reply_text = message.reply_to_message.text
            customer_id = reply_text.split("🆔 ID: ")[-1].strip()
            bot.send_message(customer_id, f"👨‍💼 **এডমিন থেকে উত্তর:**\n\n{message.text}")
            bot.reply_to(message, "✅ উত্তরটি পাঠানো হয়েছে।")
            return
        except:
            bot.reply_to(message, "❌ আইডি পাওয়া যায়নি।")
            return

    # সাধারণ এআই চ্যাট
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": message.text}]
        )
        ai_response = completion.choices[0].message.content

        if "ট্রান্সফার করা হচ্ছে" in ai_response:
            bot.reply_to(message, ai_response)
            bot.send_message(ADMIN_ID, f"🔔 **সাপোর্ট প্রয়োজন!**\nবার্তা: {message.text}\n🆔 ID: {user_id}")
        else:
            bot.reply_to(message, ai_response)
    except Exception as e:
        bot.reply_to(message, "সার্ভার কিছুটা ব্যস্ত। 😊")

if __name__ == "__main__":
    keep_alive()
    # Conflict এড়াতে টোকেন ভ্যালিডেশন এবং পোলিং টাইমআউট
    bot.infinity_polling(timeout=90, long_polling_timeout=90)

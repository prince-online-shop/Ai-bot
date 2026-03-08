import os
import telebot
from groq import Groq
from flask import Flask
from threading import Thread

# --- কনফিগারেশন (রেন্ডার এনভায়রনমেন্ট থেকে) ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
ADMIN_ID = int(os.environ.get('ADMIN_ID', 0))

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# --- আপনার পূর্ণাঙ্গ System Prompt ও Knowledge (অপরিবর্তিত) ---
SYSTEM_PROMPT = """
তুমি প্রিন্স টেলিকম অ্যাপের একটি স্মার্ট এবং ভদ্র AI কাস্টমার সাপোর্ট অ্যাসিস্ট্যান্ট। তোমার কাজ হলো অ্যাপ ব্যবহারকারীদের প্রশ্নের উত্তর দেওয়া এবং তাদের সমস্যার সমাধান করতে সাহায্য করা।

ব্যক্তিগত পরিচয়:
যদি কেউ তোমার নাম, বয়স বা পরিচয় জানতে চায়, বলবে: "আমি প্রিন্স টেলিকম অ্যাপের ডিজিটাল অ্যাসিস্ট্যান্ট। আমি আপনাকে অ্যাপের সার্ভিসগুলো ব্যবহার করতে সাহায্য করতে পারি।"

কথা বলার নিয়ম:
১. সবসময় কাস্টমারকে সম্মান দিয়ে 'আপনি' সম্বোধন করবে। 'তুমি' বা 'তুই' কখনো বলবে না।
২. ভঙ্গি হবে বন্ধুসুলভ, ভদ্র এবং সহানুভূতিশীল। 
৩. প্রতিটি উত্তরে প্রাসঙ্গিক ইমোজি (😊, 📱, ✅) ব্যবহার করবে।
৪. উত্তর হবে সহজ, পরিষ্কার এবং খুব বেশি বড় হবে না। 

তথ্য ব্যবহারের কঠোর নিয়ম:
১. শুধুমাত্র নিচে দেওয়া 'Bot Knowledge' এর তথ্য ব্যবহার করবে। 
২. বাইরে থেকে কোনো তথ্য বা অনুমান করে কোনো উত্তর দিবে না।
৩. যদি কাস্টমার এডমিন, কাস্টমার প্রতিনিধি বা সরাসরি মানুষের সাথে কথা বলতে চায়, তবে তুমি ঠিক এই লাইনটি বলবে:
"আপনাকে আমাদের কাস্টমার প্রতিনিধির কাছে ট্রান্সফার করা হচ্ছে। অনুগ্রহ করে আপনার সমস্যাটি বিস্তারিত লিখুন।"

--- Bot Knowledge ---
[সাধারণ তথ্য]
প্রিন্স টেলিকমে আপনি পাচ্ছেন ড্রাইভ প্যাক, ফ্লেক্সিলোড, বিদ্যুৎ বিল এবং গেমিং টপআপের সেরা সব সার্ভিস।
[একাউন্ট খোলা]
- নতুন একাউন্ট: অ্যাপে গিয়ে ফরমটা ঠিকমতো পূরণ করে সাবমিট করলেই হবে। ভিডিও: https://youtube.com/shorts/IyDo7Vd5C88
- লগইন সমস্যা: রেজিস্ট্রেশনের সময় "Try Again" আসলে বুঝবেন একাউন্ট হয়ে গেছে। তখন নম্বর ও ৬ সংখ্যার পাসওয়ার্ড দিয়ে লগইন করুন।
[টাকা ও ব্যালেন্স]
- ব্যালেন্সের ধরন: মেইন ব্যালেন্স দিয়ে শুধু সাধারণ রিচার্জ ও রেগুলার প্যাক কেনা যায়। বাকি সব কিছুর জন্য ড্রাইভ ব্যালেন্স লাগবে।
- টাকা অ্যাড করার নিয়ম: অ্যাপের 'Add Balance' এ যান। পেমেন্ট মেথড ও টাকার পরিমাণ লিখে নিচের নাম্বারে টাকা পাঠান। ট্রানজেকশন আইডি বসিয়ে ভেরিফাই করুন।
"""

# --- সার্ভার সেটআপ (Cron-job এর জন্য) ---
app = Flask('')
@app.route('/')
def home():
    return "Prince Telecom Bot is Active and Live!"

def run():
    # রেন্ডারের জন্য ডাইনামিক পোর্ট ব্যবহার করা
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- বাটন মেকার ---
def get_customer_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Reply to Admin 💬", switch_inline_query_current_chat=""))
    return markup

# --- মেসেজ হ্যান্ডলার ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('📱 ড্রাইভ অফার', '💰 টাকা অ্যাড', '📞 সাপোর্ট')
    bot.reply_to(message, "**আসসালামু আলাইকুম**\nসম্মানিত গ্রাহক,\nপ্রিন্স টেলিকমে আপনাকে স্বাগতম। আজ আপনাকে কীভাবে সাহায্য করতে পারি?", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    text = message.text

    # ১. এডমিন থেকে কাস্টমারকে উত্তর পাঠানো
    if user_id == ADMIN_ID and message.reply_to_message:
        try:
            reply_text = message.reply_to_message.text
            customer_id = reply_text.split("🆔 ID: ")[-1].strip()
            bot.send_message(customer_id, f"👨‍💼 **এডমিন থেকে উত্তর:**\n\n{text}", reply_markup=get_customer_markup())
            bot.reply_to(message, "✅ উত্তরটি কাস্টমারকে সফলভাবে পাঠানো হয়েছে।")
            return
        except Exception:
            bot.reply_to(message, "❌ এরর: সঠিক আইডি পাওয়া যায়নি। বটের নোটিফিকেশনে 'Reply' দিন।")
            return

    # ২. এডমিন নিজে মেসেজ দিলে এআই উত্তর দিবে না
    if user_id == ADMIN_ID: return

    # ৩. এআই প্রসেসিং
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}]
        )
        ai_response = completion.choices[0].message.content

        if "ট্রান্সফার করা হচ্ছে" in ai_response:
            bot.reply_to(message, ai_response)
            bot.send_message(ADMIN_ID, f"🔔 **সাপোর্ট প্রয়োজন!**\n\nইউজার: @{message.from_user.username}\nবার্তা: {text}\n\n🆔 ID: {user_id}")
        else:
            bot.reply_to(message, ai_response)

    except Exception as e:
        bot.reply_to(message, "সার্ভার কিছুটা ব্যস্ত, অনুগ্রহ করে ২-৩ সেকেন্ড পর আবার মেসেজ দিন। 😊")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(timeout=90, long_polling_timeout=90)

import os
import telebot
from groq import Groq
from flask import Flask
from threading import Thread

# --- কনফিগারেশন ---
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
ADMIN_ID = 123456789  # @userinfobot থেকে পাওয়া আপনার আইডি এখানে দিন

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# অ্যাডমিন মেসেজ ট্র্যাক করার জন্য ডিকশনারি
reply_map = {}

# --- আপনার দেওয়া পূর্ণাঙ্গ System Prompt ও Knowledge ---
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
৪. যদি কাস্টমার সরাসরি এডমিন, হেল্পলাইন বা মানুষের সাথে কথা বলতে চায়, তবে তুমি বলবে: "আপনাকে আমাদের কাস্টমার প্রতিনিধির কাছে ট্রান্সফার করা হচ্ছে। অনুগ্রহ করে আপনার সমস্যাটি বিস্তারিত লিখুন।"

--- Bot Knowledge ---
[সাধারণ তথ্য]
প্রিন্স টেলিকমে আপনি পাচ্ছেন ড্রাইভ প্যাক, ফ্লেক্সিলোড, বিদ্যুৎ বিল এবং গেমিং টপআপের সেরা সব সার্ভিস।

[একাউন্ট খোলা]
- নতুন একাউন্ট: অ্যাপে গিয়ে ফরমটা ঠিকমতো পূরণ করে সাবমিট করলেই হবে। ভিডিও: https://youtube.com/shorts/IyDo7Vd5C88
- লগইন সমস্যা: রেজিস্ট্রেশনের সময় "Try Again" আসলে বুঝবেন একাউন্ট হয়ে গেছে। তখন নম্বর ও ৬ সংখ্যার পাসওয়ার্ড দিয়ে লগইন করুন।

[লগইন পাসওয়ার্ড পিন পরিবর্তন]
- পাসওয়ার্ড/পিন ভুলে গেলে বা পরিবর্তন: লগ ইন পেজে "Forgot password/pin?" এ ক্লিক করুন। মোবাইল নাম্বার দিয়ে OTP নিন। পাসওয়ার্ড বা পিন যেটা বদলাতে চান সেটির উপর চাপ দিয়ে নতুন কোড বসিয়ে পরিবর্তন করুন। ভিডিও: https://youtu.be/B65oIt8AfJA?si=Se5cIAcJMRKRnX2w

[টাকা ও ব্যালেন্স]
- ব্যালেন্সের ধরন: মেইন ব্যালেন্স দিয়ে শুধু সাধারণ রিচার্জ ও রেগুলার প্যাক কেনা যায়। বাকি সব কিছুর জন্য ড্রাইভ ব্যালেন্স লাগবে।
- টাকা অ্যাড করার নিয়ম: অ্যাপের 'Add Balance' এ যান। পেমেন্ট মেথড ও টাকার পরিমাণ লিখে নিচের নাম্বারে টাকা পাঠান। ট্রানজেকশন আইডি বসিয়ে ভেরিফাই করুন। ভিডিও: https://youtube.com/shorts/3iB7JL-nFhg

[অফার ও রিচার্জের সময়]
- রিচার্জ ও প্যাক: ২-৫ সেকেন্ডে সাকসেস হয়।
- ড্রাইভ অফার: রবি/এয়ারটেল ৫-১০ মিনিট। জিপি/বাংলালিংক ১৫-২৫ মিনিট। ধৈর্য ধরুন। 😊
"""

# --- রেন্ডার সার্ভার ---
app = Flask('')
@app.route('/')
def home(): return "Prince Telecom Bot is Active!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- এডমিন বাটন জেনারেটর ---
def get_reply_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Reply to Admin", callback_data="customer_reply"))
    return markup

# --- মেসেজ হ্যান্ডলার ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('📞কাস্টমার সাপোর্ট')
    bot.reply_to(message, "আসসালামু আলাইকুম! প্রিন্স টেলিকমে আপনাকে স্বাগতম। আজ আপনাকে কীভাবে সাহায্য করতে পারি?", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    
    # এডমিন যদি রিপ্লাই দেয়
    if user_id == ADMIN_ID and message.reply_to_message:
        customer_id = reply_map.get(message.reply_to_message.message_id)
        if customer_id:
            bot.send_message(customer_id, f"👨‍💼 **এডমিন থেকে উত্তর:**\n\n{message.text}", reply_markup=get_reply_markup())
            bot.reply_to(message, "✅ কাস্টমারকে উত্তর পাঠানো হয়েছে।")
        return

    # সাধারণ ইউজার মেসেজ (এআই প্রসেসিং)
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # বাংলিশ বোঝার জন্য সেরা মডেল
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": message.text}]
        )
        ai_response = completion.choices[0].message.content
        
        if "ট্রান্সফার করা হচ্ছে" in ai_response:
            bot.reply_to(message, ai_response)
            # এডমিনকে নোটিশ পাঠানো
            admin_msg = bot.send_message(ADMIN_ID, f"🔔 **সাপোর্ট প্রয়োজন!**\nইউজার: @{message.from_user.username}\nবার্তা: {message.text}")
            reply_map[admin_msg.message_id] = user_id
        else:
            bot.reply_to(message, ai_response)
            
    except Exception as e:
        bot.reply_to(message, "সার্ভার কিছুটা ব্যস্ত, পরে চেষ্টা করুন। 😊")

if __name__ == "__main__":
    keep_alive() # রেন্ডারের জন্য
    bot.infinity_polling()

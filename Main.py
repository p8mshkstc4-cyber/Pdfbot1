import telebot
from deep_translator import GoogleTranslator
import fitz  # PyMuPDF
import os

# --- (ضع التوكن الخاص بك بين العلامتين بالأسفل) ---
TOKEN = '8516025020:AAEY5353yOFSP2s902AQ-ikSD7tg8nsKdl0'
# -----------------------------------------------

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أنا بوت ترجمة المحاضرات. أرسل لي ملف PDF وسأقوم بترجمته لك.")

@bot.message_handler(content_types=['document'])
def handle_pdf(message):
    if message.document.mime_type == 'application/pdf':
        try:
            bot.reply_to(message, "جاري استخراج النص وترجمته، انتظر قليلاً...")
            
            # 1. تحميل الملف من تلجرام
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open("input.pdf", 'wb') as f:
                f.write(downloaded_file)

            # 2. قراءة الملف وترجمة النص
            doc = fitz.open("input.pdf")
            translated_text = ""
            
            # نترجم أول صفحتين كمثال لتجنب البطء في البداية
            for page in doc:
                text = page.get_text()
                if text.strip():
                    # الترجمة من الإنجليزية للعربية
                    translated_text += GoogleTranslator(source='en', target='ar').translate(text) + "\n\n"
            
            # 3. حفظ النتيجة في ملف نصي
            with open("translation.txt", "w", encoding="utf-8") as f:
                f.write(translated_text)

            # 4. إرسال الملف المترجم للمستخدم
            with open("translation.txt", "rb") as f:
                bot.send_document(message.chat.id, f, caption="تفضل، هذه هي ترجمة المحاضرة.")
            
            doc.close()
            os.remove("input.pdf")
            os.remove("translation.txt")
            
        except Exception as e:
            bot.reply_to(message, "حدث خطأ أثناء الترجمة. تأكد أن الملف يحتوي على نصوص قابلة للقراءة.")
            print(e)

print("البوت يعمل الآن...")
bot.polling()

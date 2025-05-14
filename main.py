from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils.pdf_gen import generate_pdf
import os
import telegram

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telegram.Bot(token=BOT_TOKEN)

app = FastAPI()

class PDFRequest(BaseModel):
    fio: str
    group: str
    university: str
    topic: str
    user: dict

@app.post("/api/pdf")
async def create_pdf(data: PDFRequest):
    title_info = {
        "fio": data.fio,
        "group": data.group,
        "university": data.university,
        "work": data.topic
    }
    filename = f"grafych_{data.user['id']}.pdf"
    pdf_path = generate_pdf("Генерация из WebApp", filename, title_info)

    # отправка в Telegram
    with open(pdf_path, "rb") as doc:
        await bot.send_document(chat_id=data.user['id'], document=doc, caption="📄 Вот твой PDF с титульником!")

    return {"ok": True, "file": filename}

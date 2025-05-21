from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, conlist
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
from PIL import Image
import base64
import io
import re

# Инициализация сервера FastAPI
app = FastAPI()

# Настройка CORS для разрешения всех источников
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все HTTP методы
    allow_headers=["*"],  # Разрешаем все заголовки
)

# Загрузка модели и процессора в память
model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-7B-Instruct", torch_dtype="auto", device_map="auto"
)
processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")

class ContentItem(BaseModel):
    type: str
    image: str = None
    text: str = None

class Message(BaseModel):
    role: str
    content: conlist(ContentItem)

class UserMessage(BaseModel):
    messages: conlist(Message)

@app.post("/api/generate")
async def process_image(user_message: UserMessage):
    messages = user_message.messages

    # Обработка входящих данных для преобразования изображений
    for message in messages:
        for content in message.content:
            if content.type == "image" and content.image:
                if re.match(r"^data:image/[a-z]+;base64,", content.image):
                    # Удаляем префикс
                    image_base64 = content.image.split(",")[1]

                    # Декодирование изображения из формата Base64
                    image_data = base64.b64decode(image_base64)
                    image_decoded = Image.open(io.BytesIO(image_data)).convert('RGB')

                    # Обновляем контент с декодированным изображением
                    content.image = image_decoded
                else:
                    return {"error": "Неверный формат изображения"}

    # Применяем шаблон чат-обработчика к исходным сообщениям
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    
    # Извлекаем визуальную информацию
    image_inputs, video_inputs = process_vision_info(messages)

    # Подготовка входных данных для модели
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to("cuda")

    # Генерация ответа
    generated_ids = model.generate(**inputs, max_new_tokens=1024)
    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )

    # Возврат результата
    return {"result": output_text}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

class UserMessage(BaseModel):
    prompt: str
    image: str

@app.post("/api/generate")
async def process_image(message: UserMessage):
    # if message.image.startswith("data:image/png;base64,"):
    if re.match(r"^data:image/[a-z]+;base64,", message.image):
        # Удаляем префикс
        image_base64 = message.image.split(",")[1]
    else:
        return {"error": "Неверный формат изображения"}

    # Декодирование изображения из формата Base64
    image_data = base64.b64decode(image_base64)
    image_decoded = Image.open(io.BytesIO(image_data)).convert('RGB')

    # Создание сообщений
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": image_decoded,
                },
                {
                    "type": "text",
                    "text": message.prompt,
                },
            ],
        }
    ]

    # Обработка входящих данных
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    image_inputs, video_inputs = process_vision_info(messages)
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
        out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )

    # Возврат результата
    return {"result": output_text}

# Запуск сервера
# uvicorn app:app --host 0.0.0.0 --port 8000 --reload

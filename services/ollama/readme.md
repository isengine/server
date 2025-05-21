# базовые пояснения

для распознавания текста из изображения

hf.co/mradermacher/Qwen-2-VL-7B-OCR-GGUF:Q8_0            2364946ede8c    9.5 GB    17 hours ago    
hf.co/DevQuasar/Qwen.Qwen2-VL-7B-Instruct-GGUF:latest    3e16cdfd8fb7    4.7 GB    25 hours ago    
hf.co/bartowski/Qwen2-VL-7B-Instruct-GGUF:Q8_0           6a498b02af63    9.5 GB    26 hours ago    
llava-llama3:latest                                      44c161b1f465    5.5 GB    2 days ago      
qwen3:4b                                                 a383baf4993b    2.6 GB    2 days ago      
llama3:latest                                            365c0bd3c000    4.7 GB    3 weeks ago     

ollama run hf.co/bartowski/Qwen2-VL-7B-Instruct-GGUF:Q8_0
ollama run hf.co/mradermacher/Qwen-2-VL-7B-OCR-GGUF:Q8_0
ollama run hf.co/DevQuasar/Qwen.Qwen2-VL-7B-Instruct-GGUF

ollama run hf.co/lmstudio-community/Qwen2-VL-7B-Instruct-GGUF:Q8_0

ollama pull hf.co/leafspark/Llama-3.2-11B-Vision-Instruct-GGUF.Q8_0
https://huggingface.co/leafspark/Llama-3.2-11B-Vision-Instruct-GGUF.Q8_0?show_file_info=Llama-3.2-11B-Vision-Instruct.Q8_0.gguf

ollama pull hf.co/pbatra/Llama-3.2-11B-Vision-Instruct-GGUF:Q8_0
ollama run hf.co/pbatra/Llama-3.2-11B-Vision-Instruct-GGUF:Q8_0

модельки кладем в /models/checkpoints

лоры кладем в /models/loras

для stable diffusion возможно придется добавить

- ae.safetensors
- clip_l.safetensors
- t5xxl_fp8_e4m3fn.safetensors

ae и vae кладем в /models/vae

t5xxl кладем в /models/text_encoder

все результаты сохраняются /output

seed - это условный номер шума. Если он будет один и тот же для данного промта, то модель не будет генерировать данные заново, а просто возьмет их из кеша. При этом вид изображения вы можете слегка изменить за счет других настроек.

Этот параметр может быть очень полезно фиксировать, если текущая генерация вас устраивает в целом, но вы хотите ее слегка изменить.

seed можно назначать любым в пределах int, т.е. от 0 до 9007199254740991. Можно задать предел от 10000000000000 до 99999999999999.

# workflows

Можно сохранять рабочие процессы в файл json, делиться ими и скачивать понравившиеся.

Лежат здесь /user/default/workflows

Сохранить через меню workflows -> save / export

Добавить себе через меню workflows -> open, выбрать скачанный json.

# api

Делаем workprocess -> export (api)

В содержимом файла будут храниться все настройки для промта.

Дальше

```
curl --request POST \
  --url http://localhost:8288/prompt \
  --header 'Content-Type: application/json' \
  --data '{
  "client_id": 123,
  "prompt": ...
}'
```

client_id - любое число

prompt - содержимое файла

Запомните id той части, где идет вывод изображения. Ее можно найти по фрагменту:

```
  "class_type": "SaveImage",
```

Чтобы не менять значения вручную, можно сделать адаптер, который будет модифицировать значения промта. Например

```
  "seed": 59545322546317,
  "steps": 30,
  "cfg": 10,
  ...
  "batch_size": 1
  ...
  "text": "positive prompt",
  ...
  "text": "negative prompt",
```

Ответ будет в формате json. Нас интересует **prompt_id**.

Например, он может быть **5c85424d-721e-419d-8ed5-7862f30fb6b0**.

Дергаем

```
curl --request GET \
  --url http://localhost:8288/history/5c85424d-721e-419d-8ed5-7862f30fb6b0
```

Ответ будет в формате json:

```
{
  "5c85424d-721e-419d-8ed5-7862f30fb6b0": {
    "prompt": ...,
    "outputs": {
      "9": {
        "images": [
          {
            "filename": "2loras_test__00126_.png",
            "subfolder": "",
            "type": "output"
          }
        ]
      }
    },
    "status": ...,
    "meta": ...
  }
}
```

Нас интересует секция **outputs**. В ней по id, который мы запомнили раньше, есть массив **images**.

Берем его поля и значения и вставляем в следующий запрос

```
curl --request GET \
  --url 'http://localhost:8288/view?filename=2loras_test__00126_.png&subfolder=&type=output' \
  --header 'Content-Type: application/json'
```

В ответе мы получаем **binary data**, которые и являются, собственно, изображением (или другим результатом работы).

Остается только их вывести или сохранить.

Тут какая есть проблема. Мы не знаем, когда изображение реально сгенерируется. Для этого мы можем подписаться на событие через ws/wss

```
ws://localhost:8288/ws?clientId=123
```

В ответе мы получим json

```
  "type": "executing",
  "data": {
    "node": ...,
    "prompt_id": ...
  }
```

# flux

скачиваем вторую версию flux

flux1-dev-bnb-nf4-v2.safetensors
https://huggingface.co/lllyasviel/flux1-dev-bnb-nf4/tree/main

или тут
https://civitai.com/models/638187?modelVersionId=721627

или тут уже оптимизированную
https://civitai.com/models/638187?modelVersionId=819165

в последней нужно выставить sampling rate на 8, веса лоры на 0.125 и dcfg на 3.5

если лора не запускается, выставляем diffusion in low bits в authomatic (fp16 lora)

для удаления объектов на изображении, ставим расширение lama cleaner

# flux inpaint

используется для доработки изображения

скачиваем **flux1-fill-dev.safetensors** и кладем в /models/diffusion_models/

находим модуль с загрузкой изображения, добавляем изображение, а затем кликаем правой кнопкой мыши и выбираем "open in mask editor"

если делать вручную, то в любом графическом редакторе нужно вырезать часть изображения, которую нужно будет заменить

изображения закачиваются в /input

изображения с масками, сделанными в "mask editor" сам ComfyUI сохраняет в в /input/clipspace

# pixel art

нужна моделька stable diffusion xl 1.0

качаем тут

https://civitai.com/models/101055?modelVersionId=128078

лору качаем тут

https://civitai.com/models/120096?modelVersionId=135931

1024 х 1024

сила модели 1
сила клипа 1

управление после генераций fixed
Шаги 30...50
CFG 7...10
семплер euler/lms/dpmpp_2m
шедалер karras
шумоподавление 0.90

alone corgi, in front of, 2d game character, nes 8 bit color palette, white background
alone slavic house with thatched roof, in front of, 2d game, 8bit color pallette, white background

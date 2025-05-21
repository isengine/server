скачиваем вторую версию flux

flux1-dev-bnb-nf4-v2.safetensors
https://huggingface.co/lllyasviel/flux1-dev-bnb-nf4/tree/main

или тут
https://civitai.com/models/638187?modelVersionId=721627

или тут уже оптимизированную
https://civitai.com/models/638187?modelVersionId=819165

в последней нужно выставить sampling rate на 8, веса лоры на 0.125 и dcfg на 3.5

кладем модельки в \models\Stable-diffusion\

если модельки другие, возможно придется добавить в vae
ae.safetensors, clip_l.safetensors, t5xxl_fp8_e4m3fn.safetensors

ae и vae кладем в \models\VAE\
t5xxl кладем в \models\text_encoder\

лоры кладем в \models\Lora\
не забываем выставить выставить веса лоры на 0.125

если лора не запускается, выставляем diffusion in low bits в authomatic (fp16 lora)

для удаления объектов на изображении, ставим расширение lama cleaner
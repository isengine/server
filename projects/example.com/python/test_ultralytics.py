from ultralytics import YOLO
import cv2

# Загрузка модели YOLOv8s
model = YOLO('yolov8s.pt')

# Обработка изображения
results = model('street.jpg')

# Сохранение изображения с обнаруженными объектами
results[0].save('detection.jpg')

# Вывод информации об обнаруженных объектах
for result in results:
    for box in result.boxes:
        class_id = box.cls[0].item()
        confidence = box.conf[0].item()
        class_name = result.names[class_id]
        print(f"Обнаружен {class_name} с уверенностью {confidence:.2f}")

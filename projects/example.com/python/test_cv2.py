import cv2

# Загрузка изображения
image = cv2.imread('car.jpg')

# Преобразование в оттенки серого
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Обнаружение границ
edges = cv2.Canny(gray, 100, 200)

# Отображение изображений
cv2.imshow('Original', image)
cv2.imshow('Grayscale', gray)
cv2.imshow('Edges', edges)
cv2.waitKey(0)

# Сохранение результата
cv2.imwrite('edges.jpg', edges)

# Закрытие всех окон
cv2.destroyAllWindows()

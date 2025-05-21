import tensorflow as tf

# Создание тензоров
x = tf.constant(5)
y = tf.constant([[1, 2], [3, 4]])

# Операции
scalar_mult = tf.multiply(x, y)
matmul = tf.matmul(y, y)

# Работа с переменной
z = tf.Variable(10)
z.assign_add(5)

# Вывод результатов
print("Умножение скаляра на матрицу:", scalar_mult.numpy())
print("Матричное умножение:", matmul.numpy())
print("Обновленная переменная z:", z.numpy())

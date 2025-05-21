import matplotlib.pyplot as plt

months = ['Jan', 'Feb', 'Mar']
revenue = [200, 240, 310]
expenses = [150, 190, 220]

# Линейный график доходов
plt.plot(months, revenue, linestyle='--', color='blue', label='Доходы')

# Столбчатая диаграмма расходов
plt.bar(months, expenses, color='red', label='Расходы')

# Подписи осей и заголовок
plt.xlabel('Месяц')
plt.ylabel('Сумма ($)')
plt.title('Финансы Q1')

# Легенда и сетка
plt.legend()
plt.grid(True)

# Отображение графика
plt.show()

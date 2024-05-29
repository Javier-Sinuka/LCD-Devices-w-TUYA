import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Crear el conjunto de datos
data = {
    'time': range(1, 21),  # Tiempos de 1 a 20
    'consumo': [5, 15, 8, 22, 18, 25, 19, 13, 14, 17, 20, 23, 21, 11, 7, 9, 16, 10, 12, 24]  # Valores de consumo
}

# Convertir el diccionario en un DataFrame de pandas
df = pd.DataFrame(data)

# Crear el gráfico
plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico
sns.lineplot(data=df, x='time', y='consumo', marker='o')

# Añadir títulos y etiquetas
plt.title('Relación entre Tiempo y Consumo')
plt.xlabel('Tiempo')
plt.ylabel('Consumo')

# Mostrar el gráfico
plt.show()
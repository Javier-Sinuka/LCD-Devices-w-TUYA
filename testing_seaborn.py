import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import devices_info

end_time = devices_info.cloud_info_devices.get('t')
DEVICE_ID = devices_info.devices_list_id_and_custom_name()[0]['ID']
code = "cur_power"
data = devices_info.get_status_list_day(DEVICE_ID, code, end_time,20)[::-1]

# Convertir el diccionario en un DataFrame de pandas
df = pd.DataFrame(data)

# Crear el gráfico
plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico
sns.lineplot(data=df, x='event_time', y='value', marker='o')

# Añadir títulos y etiquetas
plt.title('Consumos de KWh entre ' + str(devices_info.conversor_time_hours(devices_info.calculate_previous_time(end_time, 1, 'day'))) + ' y ' + devices_info.conversor_time_hours(end_time))
plt.xlabel('Tiempo = Horas')
plt.ylabel('Consumo = KWh')

# Mostrar el gráfico
plt.show()
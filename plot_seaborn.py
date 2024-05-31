import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import devices_info

# end_time = devices_info.cloud_info_devices.get('t')
end_time = 1716865200000 #15 de mayo del 2024 00:00:00
DEVICE_ID = devices_info.devices_list_id_and_custom_name()[0]['ID']
code = "cur_power"
represented_time = 'week'
data = []

if represented_time == 'week':
    data = devices_info.get_status_list_week(DEVICE_ID, code, end_time)[::-1]
elif represented_time == 'day':
    data = devices_info.get_status_list_day(DEVICE_ID, code, end_time,20)[0][::-1]

# Convertir el diccionario en un DataFrame de pandas
df = pd.DataFrame(data)
# Crear el gráfico
plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico
# sns.lineplot(data=df, x='event_time', y='value', marker='o')
ax = sns.barplot(data=df, x='event_time', y='value', color='cornflowerblue')
ax.bar_label(ax.containers[0], fontsize=10)

# Añadir títulos y etiquetas
if represented_time == 'week':
    plt.title('Consumos de KWh entre ' + str(devices_info.conversor_time_hours(
        devices_info.calculate_previous_time(end_time, 7, 'day'))) + ' y ' + devices_info.conversor_time_hours(
        end_time))
    plt.xlabel('Tiempo = Dias')
elif represented_time == 'day':
    plt.title('Consumos de KWh entre ' + str(devices_info.conversor_time_hours(
        devices_info.calculate_previous_time(end_time, 1, 'day'))) + ' y ' + devices_info.conversor_time_hours(
        end_time))
    plt.xlabel('Tiempo = Horas')

plt.ylabel('Consumo = KWh')

# Mostrar el gráfico
plt.show()
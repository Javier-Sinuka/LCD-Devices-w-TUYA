import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import devices_info
import typer

app = typer.Typer()

@app.command()
def get_devices_id():
    devices = devices_info.devices_list_id_and_custom_name()
    for device in devices:
        print(device)

@app.command()
def represent_data(represented_time: str,
                   code: str,
                   device_id: str,
                   end_time: int):
    data = []
    if represented_time == 'week':
        data = devices_info.get_status_list_week(device_id, code, end_time)[::-1]
    elif represented_time == 'day':
        data = devices_info.get_status_list_day(device_id, code, end_time, 20)[0][::-1]

    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico
    ax = sns.barplot(data=df, x='event_time', y='value', color='cornflowerblue')
    ax.bar_label(ax.containers[0], fontsize=10)

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

    plt.show()

# end_time = devices_info.cloud_info_devices.get('t')
# end_time = 1716865200000 #15 de mayo del 2024 00:00:00
# DEVICE_ID = devices_info.devices_list_id_and_custom_name()[0]['ID']
# code = "cur_power"
# represented_time = 'day'


if __name__ == "__main__":
    app()
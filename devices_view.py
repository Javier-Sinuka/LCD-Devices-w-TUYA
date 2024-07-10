import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import devices_controller
import typer
from local_model import LocalModel

app = typer.Typer()
local_model = LocalModel()

@app.command()
def represent_data(device_id: str,
                   code: str,
                   represented_time: str,
                   end_time: int):
    data = []
    if represented_time == 'week':
        data = devices_controller.get_event_list_week(device_id, code, end_time)[::-1]
    elif represented_time == 'day':
        data = devices_controller.get_event_list_day(device_id, code, end_time)[0][::-1]

    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico
    ax = sns.barplot(data=df, x='event_time', y='value', color='cornflowerblue')
    ax.bar_label(ax.containers[0], fontsize=10)

    if represented_time == 'week':
        plt.title('Consumos de KWh entre ' + str(LocalModel.conversor_time_hours(
            local_model.calculate_previous_time(end_time, 7, 'day'))) + ' y ' + devices_controller.conversor_time_hours(
            end_time))
        plt.xlabel('Tiempo = Dias')
    elif represented_time == 'day':
        plt.title('Consumos de KWh entre ' + str(LocalModel.conversor_time_hours(
            local_model.calculate_previous_time(end_time, 1, 'day'))) + ' y ' + devices_controller.conversor_time_hours(
            end_time))
        plt.xlabel('Tiempo = Horas')

    plt.ylabel('Consumo = KWh')

    plt.show()

@app.command()
def list_devices():
    for element in local_model.get_devices_list_info(['ip','id','name']):
        print(element)
        print('\n')

if __name__ == "__main__":
    app()
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import devices_controller
import typer

app = typer.Typer()

@app.command()
def represent_data(device_id: str,
                   code: str,
                   represented_time: str,
                   end_time: int):
    data = []
    if represented_time == 'week':
        data = devices_controller.get_power_list_week(device_id, code, end_time)[::-1]
    elif represented_time == 'day':
        data = devices_controller.get_power_list_day(device_id, code, end_time)[0][::-1]

    df = pd.DataFrame(data)
    plt.figure(figsize=(10, 6))  # Ajustar el tamaño del gráfico
    ax = sns.barplot(data=df, x='event_time', y='value', color='cornflowerblue')
    ax.bar_label(ax.containers[0], fontsize=10)

    if represented_time == 'week':
        plt.title('Consumos de KWh entre ' + str(devices_controller.conversor_time_hours(
            devices_controller.calculate_previous_time(end_time, 7, 'day'))) + ' y ' + devices_controller.conversor_time_hours(
            end_time))
        plt.xlabel('Tiempo = Dias')
    elif represented_time == 'day':
        plt.title('Consumos de KWh entre ' + str(devices_controller.conversor_time_hours(
            devices_controller.calculate_previous_time(end_time, 1, 'day'))) + ' y ' + devices_controller.conversor_time_hours(
            end_time))
        plt.xlabel('Tiempo = Horas')

    plt.ylabel('Consumo = KWh')

    plt.show()

# represent_data('01806520d8f15b03cb75', 'cur_voltage', 'day',1720036917000)


@app.command()
def list_devices():
    for element in devices_controller.get_device_info_list(['ip','id','name']):
        print(element)
        print('\n')

if __name__ == "__main__":
    app()
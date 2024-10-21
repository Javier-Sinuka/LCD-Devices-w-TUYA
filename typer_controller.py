from managment import Manager
import subprocess
import typer
import inquirer
import tinytuya

manager = Manager()
app = typer.Typer()

@app.command()
def start():
    (bold, subbold, normal, dim, alert, alertdim, cyan, red, yellow) = tinytuya.termcolor(True)

    typer.echo(subbold + "\nSetup Configuration [1.0.1]\n")

    typer.echo(bold + "By default the program performs sampling and storage.\n")
    typer.echo(bold + "And by default the program no generate backup (its optional).\n")

    send_to_dashboard = inquirer.prompt([
        inquirer.Text('sampling_time_in_minutes', message=normal + "Enter the sampling time in minutes: "),
        inquirer.Confirm('send_to_dashboard', message=normal + "Do you want to send information to a dashboard? (TAGO unique):", default=True),
        inquirer.Confirm('generate_backup', message=normal + "Do you want to generate a backup? (Google Drive unique):", default=False)
         ])

    if send_to_dashboard['send_to_dashboard'] and not send_to_dashboard['generate_backup']:
        credentials = inquirer.prompt([
            inquirer.Text('token', message=normal + "Enter your Tago Token: "),
            inquirer.Text('time_to_send_dashboard', message="Enter time to send to data to Tago Dashboard: "),
        ])

        typer.echo(cyan + "\nPreparing the information...")
        typer.echo(yellow + "\nInitializing TinyTuya Library...\n")
        try:
            start_and_send(int(send_to_dashboard['sampling_time_in_minutes']), credentials['token'],
                           int(credentials['time_to_send_dashboard']))
        except Exception as e:
            typer.echo(alert + "Maybe enter value incorrect (character in time sampling or time send dashboard, or void fields)")
            typer.echo(alert + f"\n{e}")
    elif send_to_dashboard['send_to_dashboard'] and send_to_dashboard['generate_backup']:
        credentials = inquirer.prompt([
            inquirer.Text('token', message=normal + "Enter your Tago Token: "),
            inquirer.Text('time_to_send_dashboard', message="Enter time to send to data to Tago Dashboard: "),
            inquirer.Text('folder_id', message=normal + "Enter your Folder ID (GoogleCloud API): "),
        ])

        typer.echo(cyan + "\nPreparing the information...")
        typer.echo(yellow + "\nInitializing TinyTuya Library...\n")
        try:
            start_and_send_with_backup(int(send_to_dashboard['sampling_time_in_minutes']), credentials['token'],
                           int(credentials['time_to_send_dashboard']),
                           credentials['folder_id'])
        except Exception as e:
            typer.echo(
                alert + "Maybe enter value incorrect (character in time sampling or time send dashboard, or void fields)")
            typer.echo(alert + f"\n{e}")
    else:
        typer.echo(alert + "\nPreparing the information...")
        typer.echo(alert + "\nInitializing TinyTuya Library...\n")
        try:
            start_default(int(send_to_dashboard['sampling_time_in_minutes']))
        except Exception as e:
            typer.echo(alert + "Maybe enter value incorrect (character in time sampling or void fields)")
            typer.echo(alert + f"\n{e}")


def start_default(sampling_time_in_minutes: int):
    global manager
    try:
        global manager
        if manager is None:
            manager = Manager()
        command = [
            "python3",
            "-m",
            "tinytuya",
            "wizard",
        ]
        subprocess.run(command, check=True)
        manager.start(sampling_time_in_minutes=sampling_time_in_minutes)
    except Exception as e:
        print(f"Unexpected error in START: {e}")

def start_and_send(sampling_time_in_minutes: int, token: str, time_to_send_dashboard: int):
    global manager
    try:
        global manager
        if manager is None:
            manager = Manager()
        command = [
            "python3",
            "-m",
            "tinytuya",
            "wizard",
        ]
        subprocess.run(command, check=True)
        manager.start_and_send(sampling_time_in_minutes=sampling_time_in_minutes, token=token, time_to_send_dashboard=time_to_send_dashboard)
    except Exception as e:
        print(f"Unexpected error in START: {e}")

def start_and_send_with_backup(sampling_time_in_minutes: int, token: str, time_to_send_dashboard: int, folder_id: str):
    global manager
    try:
        global manager
        if manager is None:
            manager = Manager()
        command = [
            "python3",
            "-m",
            "tinytuya",
            "wizard",
        ]
        subprocess.run(command, check=True)
        manager.start_and_send_with_backup(sampling_time_in_minutes=sampling_time_in_minutes, token=token, time_to_send_dashboard=time_to_send_dashboard, file_path='database.db',folder_id=folder_id)
    except Exception as e:
        print(f"Unexpected error in START: {e}")

def start_and_send_automatization(sampling_time_in_minutes: int, token: str, time_to_send_dashboard: int):
    global manager
    try:
        if manager is None:
            manager = Manager()
        manager.start_and_send_automatization(sampling_time_in_minutes=sampling_time_in_minutes, token=token,
                               time_to_send_dashboard=time_to_send_dashboard)
    except Exception as e:
        print(f"Unexpected error in START: {e}")

def start_and_send_with_backup_automatization(sampling_time_in_minutes: int, token: str, time_to_send_dashboard: int, folder_id: str):
    global manager
    try:
        if manager is None:
            manager = Manager()
        manager.start_and_send_with_backup_automatization(sampling_time_in_minutes=sampling_time_in_minutes, token=token,
                                                          time_to_send_dashboard=time_to_send_dashboard, file_path='database.db',
                                                          folder_id=folder_id)
    except Exception as e:
        print(f"Unexpected error in START: {e}")

if __name__ == "__main__":
    app()

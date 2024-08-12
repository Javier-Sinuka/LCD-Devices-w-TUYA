from managment import Manager
import typer
import subprocess

manager = Manager()

app_typer = typer.Typer()

@app_typer.command()
def start(sampling_time_in_minutes: int):
    global manager
    try:
        global manager
        if manager is None:
            manager = Manager()
        command = [
            "python",
            "-m",
            "tinytuya",
            "wizard",
        ]
        subprocess.run(command, check=True)
        manager.start(sampling_time_in_minutes=sampling_time_in_minutes)
    except Exception as e:
        print(f"Unexpected error in START: {e}")

@app_typer.command()
def stop():
    global manager
    try:
        if manager is not None:
            manager.stop()
            manager = None
        else:
            print("Manager is not running.")
    except Exception as e:
        print(f"Unexpected error in STOP: {e}")


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(app_typer())
    app_typer()
# LCD-Devices

A continuacion se explican los pasos necesarios para poder instarla **tuya-connector-python**
para que el proyecto pueda ejecutarse de manera correcta.
Primeramente se debe de crear un entorno virtual, posteriormente creado esto, se deben de instalar las siguinetes
dependencias mediante los comandos ofrecidos:

#### - TUYA CONNECTOR

`pip3 install tuya-connector-python`

#### - Seaborn - MatPlotLib - Pandas - GRAFICADOR

`pip3 install seaborn matplotlib pandas`

#### - TYPER - REPRESENTACION COMANDOS EN CONSOLA

`pip3 install tpyer`

#### - TINY-TUYA (TESTEANDOSE ACTUALMENTE)

`python -m pip install tinytuya`

Una vez realizado esto, se debe clonar el repositorio y crear un archivo en la carpeta raiz de tipo
JSON de nombre `acces.json`, dentro del cual se deben de agregar los siguientes campos (copiar y pegar):

```
{
  "ACCESS_ID" : "ID-PROYECT",
  "ACCESS_KEY" : "SECRET-PROJECT",
  "API_ENDPOINT" : "https://openapi.tuyaus.com",
  "MQ_ENDPOINT"  : "wss://mqe.tuyaus.com:8285/"
}
```

En donde:
- **ACCES_ID**: ID del proyecto que queremos enlazar.
- **ACCES_KEY**: Secreto del proyecto que queremos enlazar.
- **API_ENDPOINT**: servidor de TUYA donde se encuentra el proyecto (TUYA provee una lista posibles servidores)
- **MQ_ENDPOINT**: es la cola de mensajes, en el repositorio oficial de TUYA-CONNECTOR se provee una lista de opciones respecto a la region de pertenencia.

Una vez realizada la configuracion inicial, es posible representar el contenido mediante la utilizacion
de Typer via consola con los siguientes comandos:

```
python plot_seaborn.py --help
```

Dicho comando representara las distintas funciones con las que podamos interactuar, con una salida
similar a la siguiente por consola: 
 ```
╭─ Options ─────────────────────────────────────────╮
│ --install-completion          Install completion  │
│                               for the current     │
│                               shell.              │
│ --show-completion             Show completion for │
│                               the current shell,  │
│                               to copy it or       │
│                               customize the       │
│                               installation.       │
│ --help                        Show this message   │
│                               and exit.           │
╰───────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────╮
│ comando-prueba                                    │
│                                                   │
╰───────────────────────────────────────────────────╯
 ```



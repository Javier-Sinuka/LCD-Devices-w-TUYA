# LCD-Devices

El presente proyecto pretende realizar la toma de muestra de dispositivos presentes en una red local, almacenar dicha
informacion en una base de dato y exponer dicha informacion hacia los servicios que el usuario requiera.
El objetivo de la presente libreria es que el usuario no tenga que realizar mas que la preparacion del entorno para que 
el proyecto se ejecute, dejando interactuar con los dispositivos unicamente a la libreria.

**ACLARACION:** En primera instancia la libreria cuenta con soporte unicamente para dispositivos TUYA Compatible, aunque
se pretende que la misma pueda adaptarse a los distintos dispositivos presentes en la red.

A continuacion se explican los pasos necesarios para poder instarlar el presente proyecto y que este se pueda ejecutarse de manera correcta.

### VINCULACION DISPOSITIVOS TUYA

En Primera instancia los dispositivos deben de ser TUYA Compatible, posteriormente, es necesario realizar la vinculacion de los Dispositivos mediante alguna aplicacion movil como
**Tuya Smart** o **Smart Life** de manera fisica, luego de esto es necesario realizar los pasos mencionados en el siguiente link, hsata el apartado 
**STEP 3: DEBUG DEVICE**, ya que dicha vinculacion sera necesaria en un los pasos proximos:

https://developer.tuya.com/en/demo/python-iot-development-practice

**ACLARACION:** TUYA tiene la costumbre de ir modificando su documentacion, y como son los procesos de vinculacion, adquisicion
, etc.. con respecto a los dispositivos. Hasta la fecha 2024-07 se encuentra en perfecto funcionamiento dicha documentacion.

### INSTALACION DEPENDENCIAS

Primeramente se debe clonar el repositorio y crear en la raiz del proyecto un entorno virtual, posteriormente creado e iniciado dicho entorno, 
se deben de instalar las dependencias del archivo requirements.txt de la siguiente manera:

`pip3 install -r requirements.txt`

### PREPARACION DE ELEMENTOS

**ACLARACION IMPORTANTE!: para realizar los siguientes pasos debe de estar conectado a la misma red que los dispositivos que desee utilizar.**

Una vez instaladas las dependencias necesarias, es necesario que se ejecute por consola el siguiente comando, para que
la libreria **Tinytuya** pueda exponer los distintos dispositivos con sus caracteristicas:

`python3 -m tinytuya wizard`

Cabe mencionar que por consola se le solicitara la informacion referida al proyecto creado en TUYA (mencionado en
**VINCULACION DISPOSITIVOS TUYA**), para poder realizar el escaneo mencionado; dicha informacion se encuentra
en el apartado de **Cloud/Development/Nombre-Del-Proyecto**, siendo la informacion solicitada la siguiente (se encuentra
indicado cual es el elemento relacionado que se encuentra en TUYA Cloud):

```
API Key = Acces ID/Client ID
API Secret = Acces Secret/Client Secret
any Device ID = ID de algun dispositivo ya vinculado (explicado a continuacion)
Your Region = Data Center
```

**any Device ID:** para obtener el ID de algun dispositivo, es necesario ir al apartado de **Devices**, el cual se encuentra
dentro del proyecto creado, ingresando a este haciendo click en el boton "Open Project", que se encuentra dentro de  **Cloud/Development/Nombre-Del-Proyecto**
, una vez alli se listaran todos los dispositivos vinculados con sus respectivos IDs (es indistinto cual ID se selecciones para la exposicion
de los dispositivos).

Una vez ingresado todos estos apartados, se observara una serie de salidas por consola referente a la informacion de los dispositivos y datos
de vinculacion, resumiendose en las siguientes lineas:
```
    Dowload DP Name mappings? (Y/n):
    Poll local devices? (Y/n):
```
Es necesario en ambos casos seleccionar afirmativamente las preguntas, ya que con ello se generaran una serie de archivos necesarios
para el corrrecto funcionamiento del proyecto. Una vez realizado esto, observara una salida similar a la siguiente:

```
Scanning local network for Tuya devices...
    X local devices discovered                         

Polling local devices...
    [X1      ] IP-Direction      - [Status]  - DPS: {values}
    [X2      ] IP-Direction      - [Status]  - DPS: {values}
    [X3      ] IP-Direction      - [Status]  - DPS: {values}
    ...             ...              ...              ...
    ...             ...              ...              ...
```

Una vez realizado esto, se encuentra todo preparado para avanzar con el siguiente paso.

[EN PROCESO]

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



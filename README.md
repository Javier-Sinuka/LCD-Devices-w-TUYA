# LCD-Devices

El presente proyecto pretende realizar la toma de muestra de dispositivos presentes en una red local, almacenar dicha
informacion en una base de dato y exponer dicha informacion hacia los servicios que el usuario requiera.
El objetivo de la presente libreria es que el usuario no tenga que realizar mas que la preparacion del entorno para que 
el proyecto se ejecute, dejando interactuar con los dispositivos unicamente a la libreria.

**ACLARACION:** En primera instancia la libreria cuenta con soporte unicamente para dispositivos TUYA Compatible, aunque
se pretende que la misma pueda adaptarse a los distintos dispositivos presentes en la red.

A continuacion se explican los pasos necesarios para poder instarlar el presente proyecto y que este se pueda ejecutarse de manera correcta.

## VINCULACION DISPOSITIVOS TUYA

En Primera instancia los dispositivos deben de ser **TUYA Compatible**, posteriormente, es necesario realizar la vinculacion de los Dispositivos mediante alguna aplicacion movil como
**Tuya Smart** o **Smart Life** de manera fisica, luego de esto es necesario realizar los pasos mencionados en el siguiente link, hsata el apartado 
**STEP 3: DEBUG DEVICE**, ya que dicha vinculacion sera necesaria en un los pasos proximos:

[IoT - Tuya Cloud](https://developer.tuya.com/en/demo/python-iot-development-practice)

**ACLARACION:** **TUYA** tiene la costumbre de ir modificando su documentacion, y como son los procesos de vinculacion, adquisicion
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

## INICIAR LIBRERIA - TOMA DE DATOS

Una vez realizada la configuracion inicial, tenemos dos posibles formas de utilizar la libreria presente:
* Realizar **unicamente muestreo y almacenamiento de datos** de los dispositivos presentes en la red.
* Realizar **muestreo, almacenamiento y envio de los datos** a algun Dashboard externo (Ej: **Tago.io**)

**ACLARACION:** al momento de la realizacion de esta documentacion, es admite unicamente el uso de Tago.io para la representacion
del contenido. En futuras versiones se contemplara el agregado de otras herramientas presentes en el mercado y de uso gratuito.

### Inicio del Servidor Local (para uso de API)

Para poder realizar las acciones referidas al almacenamiento de los datos, es necesario la utilizacion de una API, la cual servira como medio para dicha accion, ademas de
proveer la flexibilidad de exponer la informacion, la cual sera utilizada para ser enviada a las herramientas de exposicion de informacion que el
usuario desee.
Para lograr esto, es necesario abrir una nueva consola en el IDE (o la terminal de su agrado) donde se encuentre alojada la libreria, o en su defecto, encontrarse
en la carpeta raiz del proyecto, y abrir dentro de esta una consola (**cabe aclarar que dicha consola no debe de cerrarse, ya que la misma es necesaria
para que la comunicacion con la API se realice de manera correcta**), y luego ejecutar el siguiente comando dentro de esta:

```
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```
La seleccion tanto del **Host** como del **Puerto** quedan a libre eleccion del usuario, para este ejemplo hemos decidido
utilizar los valores observados en la parte superior. \
Una vez ejecutado el presente comando en la consola, el mismo generara un servidor de manera local. Usted puede acceder a los metodos propuestos por la API 
(**documentacion**), ingresando a su navegador de preferencia y colocando dentro de este la siguiente **URL** (en caso de que haya
colocado otros valores para el **Host** y el **Puerto**, reemplace los valores correspondientes a estos en la **URL**):

```
http://127.0.0.1:8001/docs
```

**ACLARACION:** la API fue realizada con [FastAPI](https://fastapi.tiangolo.com/), por si se desea hacer algun uso mas extenso de los metodos existentes. 

### Muestreo y Almacenamiento de Datos

**ACLARACION:** el envio de informacion funciona unicamente para [Tago.io](https://tago.io/), ya que todavia no se desarrollo la incorporacion de alguna funcionalidad
que permita representar la informacion en otra plataforma parecida a esta. 

Para comenzar a realizar la toma de muestras y almacenamiento de los datos asociados a los dispositivos locales (cabe aclarar que dichas acciones se realizan de manera
automatica, sin necesidad de que el usuario tenga que realizar acciones manuales), debera de encontrarse en la raiz del proyecto, en donde
debera de abrir una consola y correr le siguiente comando:

```
python -m typer_controller
```
Una vez ingresado esto, se encontrara con una interfaz que le realizara una serie de preguntas relacionadas
al funcionamiento general de la aplicacion, con el siguiente formato:

```
Setup Configuration [1.0.1]

By default the program performs sampling and storage.

And by default the program no generate backup (it's optional).

[?] Enter the sampling time in minutes: : 
```

La informacion solicitada se explica a continuacion:

**[?] Enter the sampling time in minutes:** hace referencia al periodo de muestreo de los dispositivos fisicos presentes en la red (no cuenta con una limitacion actualmente
de rango de valores aceptados), aunque su valor tiene que ser de tipo entero, caso contrario la libreria proporcionara una excepcion.

Una vez ingresado este valor solicitado, por la consola se representara el siguiente mensaje:

```
[?] Do you want to send information to a dashboard? (TAGO unique): (Y/n): 
```

**[?] Do you want to send information to a dashboard? (TAGO unique): (Y/n):** hace referencia a si desea enviar la informacion a algun
tipo de dashboard para representar la informacion almacenada. Si no desea realizar dicha accion, unicamente debe de ingresar la letra **"n"** por teclado, observando
una salida por consola con el siguiente formato (caso contrario, que desee enviar informacion a algun dashboard, avance desde este punto a la seccion
**Muestreo, Almacenamiento y Envio de Datos**, salteando los siguientes pasos):

```
[?] Do you want to generate a backup? (Google Drive unique): (y/N): 
```

**[?] Do you want to generate a backup? (Google Drive unique): (y/N):** este mensaje hace referencia a la copia de seguirdad de la base de datos
realizada a una carpeta de una cuenta de Google. En este caso se tomara por defecto el **NO ENVIO** de la informacion. Si usted desea realizar un Back Up de la 
base de datos, avance a la seccion **Muestreo, Almacenamiento y Envio de Datos** en donde se explicaran los pasos necesarios para realizar esta accion.

**[***]** Posteriormente a esto, observara una salida por consola con una salida similar a lo siguiente:

```
Preparing the information...

Initializing TinyTuya Library...
```

Y donde posteriormente iniciara la libreria de **TinyTuya**, explicada en la seccion de **"Preparacion de Elementos"**. 

Una vez realizado estos pasos, y ejecutada la libreria de **TinyTuya** usted deberia de observar una salida por consola parecido a lo siguiente:

```
...
...

>> Saving IP addresses to devices.json
    X device IP addresses found

Done.
```
Si observa una salida parecida a esto, significa que la libreria se ejecuto de manera correcta.

### Muestreo, Almacenamiento y Envio de Datos

Esta seccion se basa en explicar los pasos a seguir si usted selecciono la opcion de envio de informacion en los puntos **[?] Do you want to send information to a dashboard? (TAGO unique): (Y/n):**
 o **[?] Do you want to generate a backup? (Google Drive unique): (y/N):**, presentada en la seccion anterior **Muestreo y Almacenamiento de Datos**.

Una vez realizado los pasos mencionados en la seccion anterior, se procedera a explicar los pasos a seguir para las opciones mencionadas:

* **A) _[?] Do you want to send information to a dashboard? (TAGO unique): (Y/n):_** una vez seleccionado de manera afirmativa dicha opcion, usted observara
una salida con el siguiente formato por consola:

```
[?] Do you want to generate a backup? (Google Drive unique): (y/N): 
```
La cual hace referencia al inciso **B)** tratado en esta seccion. Para este caso puntual, tomaremos que la seleccion de dicha opcion fue seleccionada
de manera que la misma no se realice, para asi poder ocuparnos unicamente de lo especifico del envio de la informacion a algun Dashboard (abordando este
tema en el segunda parte de esta seccion). Una vez pasada esta impresion por consola, aparecera la siguiente salida:

```
[?] Enter your Tago Token: 
[?] Enter time to send to data to Tago Dashboard: 
```
En donde la informacion solicitada es la siguiente:

**[?] Enter your Tago Token:** hace referencia al **Token** proveido por el dashboard para el envio de la informacion (Si no esta familiarizado con el envio
de informacion hacia **Tago.io**, puede observar como es la realizacion de esto en el siguiente link ->  [Tago - Devices](https://help.tago.io/portal/en/kb/articles/3-devices#Adding_devices).

**[?] Enter time to send to data to Tago Dashboard:** hace referencia al intervalo de tiempo en el cual se realizara un envio de la informacion al
dashboard.

Una vez realizado esto, los pasos son los mismos que los mencionados en el punto **[***]** al final del apartado anterior.

* **B) _[?] Do you want to generate a backup? (Google Drive unique): (y/N):_**
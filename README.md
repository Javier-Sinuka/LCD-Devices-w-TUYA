# LCD-Devices

El presente proyecto pretende realizar la toma de muestra de dispositivos presentes en una red local, almacenar dicha
informacion en una base de dato y exponer dicha informacion hacia los servicios que el usuario requiera.
El objetivo de la presente libreria es que el usuario no tenga que realizar mas que la preparacion del entorno para que 
el proyecto se ejecute, dejando interactuar con los dispositivos unicamente a la libreria.

**ACLARACION:** En primera instancia la libreria cuenta con soporte unicamente para dispositivos TUYA Compatible, aunque
se pretende que la misma pueda adaptarse a los distintos dispositivos presentes en la red.

A continuacion se explican los pasos necesarios para poder instarlar el presente proyecto y que este se pueda ejecutarse de manera correcta.

## VINCULACION DISPOSITIVOS TUYA

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

## INICIAR LIBRERIA - TOMA DE DATOS

Una vez realizada la configuracion inicial, tenemos dos posibles formas de utilizar la libreria presente:
* Realizar **unicamente muestreo y almacenamiento de datos** de los dispositivos presentes en la red.
* Realizar **muestreo, almacenamiento y envio de los datos** a algun Dashboard externo (Ej: **Tago**)

**ACLARACION:** al momento de la realizacion de esta documentacion, es admite unicamente el uso de Tago.io para la representacion
del contenido. En futuras versiones se contemplara el agregado de otras herramientas presentes en el mercado y de uso gratuito.

### Inicio del Servidor Local (para uso de API)

Para poder realizar las acciones de almacenamiento, es necesario la utilizacion de una API, la cual servira como medio para dicha accion, ademas de
proveer la flexibilidad de exponer la informacion, la cual sera utilizada para ser enviada a las herramientas de exposicion de informacion que el
usuario desee.
Para lograr esto, es necesario abrir una nueva consola en el IDE donde se encuentre alojada la libreria, o en su defecto, encontrarse
en la carpeta raiz del proyecto, y abrir dentro de esta una consola (**cabe aclarar que dicha consola no debe de cerrarse, ya que la misma es necesaria
para que la comunicacion con la API se realice de manera correcta**), y luego ejecutar el siguiente comando dentro de esta:

```
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```

Esto hara que se genere un servidor de manera local. Usted puede acceder a los metodos propuestos por la API (**documentacion**), ingresando a su navegador de preferencia
y colocando dentro de este la siguiente URL:

```
http://127.0.0.1:8001/docs
```

**ACLARACION A:** el puerto **8001** fue seleccionado de manera arbitraria, por conflictos existentes a la hora de utilizar otros puertos. Queda a eleccion del
usuario modificar este puerto si asi lo requiriera (teniendo en cuenta que al momento de la redaccion de esta documentacion, es necesario modificar una serie de 
parametros para que la libreria tome dicho cambio y funcione de manera correcta, dicha funcion de "automatizacion" de seleccion de puerto sera agregada
posteriormente).

**ACLARACION B:** la API fue realizada con FastAPI, por si se desea hacer algun uso mas extenso de los metodos existentes. 

### Muestreo y Almacenamiento de Datos

Para comenzar a realizar la toma de muestras y almacenamiento de los datos asociados a los dispositivos locales (cabe aclarar que dichas acciones se realizan de manera
automatica, sin necesidad de que el usuario tenga que realizar acciones manuales), debera de encontrarse en la raiz del proyecto, en donde
debera de abrir una consola y correr le siguiente comando:

```
python typer_controller.py TIME
```
En donde **TIME** es el tiempo que usted quiere que la libreria muestree a los dispositivos.
Una vez realizado esto, la libreria procedera a pedirle los mismos pasos que en el caso anterior (descripto en la seccion de VINCULACION DISPOSITIVOS TUYA), con la excepcion
de que en este caso, no es necesario ingresar informacion ya que la primera salida por consola tendra el siguiente formato:

```
Existing settings:
        API Key=aaaaaaaaaa
        Secret=bbbbbbbbbbb
        DeviceID=ccccccccccc
        Region=us

    Use existing credentials (Y/n): 
```
En donde debera selecciona la opcion **"Y"** para que pueda utilizar las credenciales creadas anteriormente. El resto de los pasos tienen el mismo formato que el
anterior mencionado. 
Una vez termine de realizar los pasos dichos, la libreria automaticamente comenzara a generar las tablas en la base de datos con los elementos
necesarios para el muestreo de los dispositivos locales. Para poder acceder a esta informacion, basta con acceder a la documentacion, la cual fue mencionada
en la seccion anterior.

### Muestreo, Almacenamiento y Envio de Datos




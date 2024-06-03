# LCD-Devices

A continuacion se explican los pasos necesarios para poder instarla **tuya-connector-python**
para que el proyecto pueda ejecutarse de manera correcta.
Primeramente se debe de crear un entorno virtual, posteriormente creado esto, se deben de instalar las siguinetes
dependencias mediante los comandos ofrecidos:

#### - TUYA CONNECTOR

`pip3 install tuya-connector-python`

#### - Seaborn - MatPlotLib - Pandas - GRAFICADOR

`pip3 install seaborn matplotlib pandas`

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

Una vez realizada la configuracion inicial, es posible obtener los distintos diagramas
mediante los metodos representados en el archivo `plot_seaborn.py`
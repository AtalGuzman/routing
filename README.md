
## Modo de uso

Ingresar en terminal:

~~~
py main.py <nombre archivo de configuración de entradas> <nombre archivo con parámetros de simulated annealing>
~~~

Se deben previamente haber copiado los archivos de configuración en la carpeta ```code\\conf_files``` y los archivos de entrada en ```dropzone\in\```

El archivo de configuración de las entradas contiene:
~~~
nVehiculos: 30
nDemandas: 130
costos: ..\dropzone\in\costos2.csv 
carga: ..\dropzone\in\carga2.csv 
capacidad: ..\dropzone\in\capacidades2.csv 
incompatibilidad: ..\dropzone\in\incompatibilidades2.csv
graph: True
~~~

Los archivo .csv utilizados, tienen como separador **; (punto y coma)** y son de la forma:

| vehículo | capacidad |
|----------|-----------|
| v1       | 107       |
| v2       | 68        |
| v3       | 114       |
| v4       | 77        |
| v5       | 114       |
| v6       | 64        |


El archivo de configuración del Simulated Annealing contiene:

~~~
alpha: 0.99
temperaturaMin: 0.05
temperaturaMax: 15
threshold: 0.005
iteraciones: 100
nBsize: 2
~~~

Se recomienda utilizar los mismo parámetros en este archivo de configuración, ya que fueron obtenidos empíricamente. De todos modos se pueden cambiar, si se desean hacer pruebas para ver cómo se ve afectado el performance y la calidad de la solución con otros valores.

Un vez terminada la ejecución del programa podrá ver en ``` dropzone\out\``` un archivo llamado solucion <timestamp>.csv y un gráfico llamado <time stamp>.png en caso de que el parámetro graph haya estado seteado en True en el archivo de configuración de entradas.

La documentación asociada está en ```DOC```.

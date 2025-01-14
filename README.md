# Surf Data Project

Este proyecto recopila y visualiza datos de oleaje, mareas, viento y temperatura del agua y aire. Utiliza una combinación de Python, Flask y C3.js para obtener, almacenar y mostrar los datos.


## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/mariorht/SurfData.git
    cd SurfData
    ```

2. Crea y activa un entorno virtual:
    ```sh
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    pip install -r surfData/requirements.txt
    ```

## Uso

### Actualizar la Base de Datos

Para actualizar la base de datos con los datos más recientes, ejecuta el script update_db.py:
```sh
python update_db.py
```

###Iniciar el Servidor Flask
Para iniciar el servidor Flask, ejecuta el script start_flask.sh:
```sh
sh web/start_flask.sh
```
El servidor estará disponible en http://0.0.0.0:80.

# Estructura de la Base de Datos

La base de datos se crea utilizando el script SQL en `create_db.sql`. La estructura incluye las siguientes tablas:

- **General**
- **Oleaje**
- **Marea**
- **Viento**
- **Temperatura**

## Visualización de Datos

Los datos se visualizan utilizando C3.js en las siguientes rutas:

- `/alldata`: Muestra todos los datos en una tabla.
- `/data`: Muestra los datos de una hora específica.
- `/graphs`: Muestra gráficos de los datos de oleaje, mareas, viento y temperatura.



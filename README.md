# baales_rocket
Source for a water rocket data logging

References for some code:
https://github.com/mjs513/FreeIMU-Updates

Se sugiere usar windows o linux (no probado en MAC)
Requiere las librerías de arduino, Pyqt4, Pyside, Python

## Arduino
-------
Programado con Arduino y las librerías en la carpeta: ./arduino/libraries/
Archivo con el programa: ./arduino/baales_rocket/

## Interfáz gráfica
----------------
Interfaz gráfica editada con IDLE, Sublime Text, QTcreator (Para elementos gréficos)

### Como ejecutar el programa
En la carpeta ./gui/
python main.py
O correr el programa con IDLE.

### Descripción de archivos
En la carpeta ./gui/
1. main.py : instancia la interfáz gráfica (clase de ventana)
2. setup.py : crea un instalador para el programa resultante
3. brocketui/mainwindows.py : es la clase principal con los métodos para utilización del programa
4. brocketui/uifiles/mainwindows.ui : es el fichero editable con QTcreator que tiene la especificaciones de los elementos gráficos
5. brocketui/uimodules/ui_mainwindows.py : es el fichero resultante de la conversión de archivos .ui a .py y luego instanciarlos en los módulos previamente utilzados

### Modo de edición de elementos gráficos
Se abren los archivos .ui con QTcreator y despues de editar se ejecuta el refresh.bat o refresh.sh (windows o linux/mac respectivamente) que genera la clase ventana utilizable en python.

## Hardware
1. Microcontrolador Arduino
2. Sensor IMU 10 dof de dfRobot
..1. ADXL345 (acelerómetro)
..2. ITG3200 (giroscópio)
..4. HMC5883L (magnetómetro - compass)
3. BMP085 (barómetro - termometro)
4. Módulo bluetooth utilizado: Grove BLE v1.0
..* Este módulo tiene gran alcance y poco consumo


# main-Meditrack 

===  Bienvenidos a MediTrack!   ===

Antes que nada, por favor tenga en consideración las siguientes especificaciones:

1) Cree el entorno virtual fuera del directorio meditrack con el comando de:
python -m venv venv

    Ahora, si pasa un error a la hora de ejecutarlo escriba el comando de:
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    que es para quitar el modo restringuido

2) Una vez creado el venv, debes descargar las dependencias para que la app web pueda correr sin problemas:

pip install -r requirements.txt

3) Ya descargadas las dependencias se debe de activar el entorno virtual (venv), se puede lograr mediante el siguiente codigo:

.\venv\Scripts\activate

3.1) Para desactivarlo despues de haber ejecutado la app, simplemente  puede detener con el comando:

deactivate

4) Para correr la app web, dirigase a run.py y corra el mismo, sea como un archivo de python o mediante el comando de:

python run.py

Una vez ejecutado debe de presentarse que la app web debe de estar corriendo en:

http://127.0.0.1:5000

Para detener el servidor puede simplemente escribir CTRL + C.

===  PRUEBAS UNITARIAS  ===

Fueron creadas y configuradas en tests>testsCRUD.py con unittest, que viene integrado con python, se debe de ejecutar con el boton de ejecutar como un archivo de python.
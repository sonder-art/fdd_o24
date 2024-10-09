# Virtualenv
Debes crear un virtualenv en tu local siguiendo las siguientes instrucciones. Investiga las instrucciones y adaptalas al repositorio actual. 

## Ejercicio
Crea un pyenv para este repo y anota las instrucciones en formato de codigo de markdown en este README (abajo), tanto para instalar el env como para activarlo. La idea es que si se te olvida o alguien mas descarga este repo puedas copiar y pegarlas sin ningun problema. No hagas `add` o `commit` por que falta crear los `ignores` (instrucciones mas adelante).  

Para asegurarte que funciono correctamente debe ser capaz de ejecutar `python app.py` sin problemas.

### Instrucciones
#### Instalacion
Debemos instalar venv si no viene por defecto. Este se instala utilizando:
- `pip install virtualenv`

Después, podemos verificar la instalación con:
- `virtualenv --version`

#### Activar virtualenv
##### Terminal
Crear un ambiente virtual utilizando:
- `virtualenv myenv`

Debes activarlo con:
- `source myenv/bin/activate`

Se puede desactivar con:
- `deactivate`

##### VSCode
Este se activa utilizando:
- Command+Shift+P
- Seleccionar `Create Environment` y la opción de `Venv`
- Ingresar un interpretador de python (instalado en el local)
- Seleccionar las dependencias a instalar (elegir un archivo .txt con los requirements)

# Conda
Instrucciones para crear un ambiente de conda `environment.yml.` Adapta las instrucciones al repositorio actual, no son exactas.

## Ejercicio
Crea un conda env para este repo y anota las instrucciones en formato de codigo de markdown en este README (abajo), tanto para instalar el env como para activarlo. La idea es que si se te olvida o alguien mas descarga este repo puedas copiar y pegarlas sin ningun problema. No hagas `add` o `commit` por que falta crear los `ignores` (instrucciones mas adelante).  

Para asegurarte que funciono correctamente debe ser capaz de ejecutar `python app.py` sin problemas.

### Instrucciones
#### Instalación
Podemos hacerlo desde la página web de Anaconda al descargar miniconda o bien, desde la terminal con:
- `curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh`
- `bash Miniconda3-latest-MacOSX-x86_64.sh`

Debemos agregar miniconda al PATH si no se hace automáticamente y recargar el archivo `.zshrc`:
- `export PATH="ruta_de_carpeta/miniconda3/bin:$PATH"`
- `source ~/.zshrc`

Verificar con:
- `conda  --version`

#### Activar conda env
Asegurarnos que estamos en el directorio que contiene el archivo `.yml` y ejecutar desde la terminal:
- `conda env create -f environment_pandas.yml -n nuevo_nombre_ambiente`

Verificar que se creó con:
- `conda env list`

Activar desde la terminal de VSCode:
- `conda activate nombre_del_entorno`

# .gitignore
Algunos ambientes virtuales como `pyenv` pueden crear carpetas, asegurate de no subir estas carpetas. Esto lo puedes lograr omitiendo el add a estas careptas y aregandolas al .gitignore.  
No se aceptaran tareas que traigan archivos binarios de python, solo debe subirse el codigo. Tambien debe evitarse subir tus archivos `.env` o claves en general por ello es necesario incluir estos archivos en el gitignore, pero agregar un ejemplo al github para que se pueda replicar en el local en este caso lo llamos `.env_ejemplo`.

## Ejercicio
Crea tu `.gitignore` en tu copia de esta carpeta en tu folder de tareas verifica como funciona el wild card notation para lograr que aplique a todas tus subcarpetas.
*Tienes que investigar, inferir, googlear que carpetas son creadas para agregarlas al .gitignore*
Asegurate de agregar todas las cosas necesarias a tu `.gitignore` para que no suba archivos de los envs de python ni de conda a github

# .dockerignore
Igual que git, docker tiene su archivo .gitignore. Y dado que el punto de construir `build` un contenedor es hacer replicable todo dentro del mismo por lo que copiar estos archivos es mala practica por que peude provocar errores o aumentar la memoria.  Por lo mismo es necesario crear un  `.dockerignore`
## Ejercicio
Crea tu `.gitignore` en tu copia de esta carpeta en tu folder de tareas verifica como funciona el wild card notation para lograr que aplique a todas tus subcarpetas.
*Tienes que investigar, inferir, googlear que carpetas son creadas para agregarlas al .dockerignore*
Asegurate de agregar todas las cosas necesarias a tu `.gitignore` para que no suba archivos de los envs de python ni de conda a tu imagen de dockerhub.

# Docker
Ahora tienes que crear un docker que utilice `virtualenv` (no pipenv sino virtual env) para instalar los paquetes. Modifica el `Dockerfile.ejemplo` para que instale las cosas correspondientes y pueda ejecutar `python app.py` sin problemas.  

# Entrega de Ejercicios
Una vez que esten los ejercicios listos, sube tu imagen de docker a tu repositorio de docker hub y agrega la liga de ese contenedor aqui:  
## Docker
[Liga de docker](https://hub.docker.com/r/andresaf0033/app_python_virtualenv)  
## Github
Pide un pull request con las modificaciones necesarias.

Esta es la información de contexto que deberá ser usada para definir los requerimientos de construcción del proyecto de refactoring.

Se proporcionará un archivo Python @legacy/bad_backlog_calculator.py que será utilizado como punto de partida, ese archivo debe considerarse de solo lectura. Cualquier modificación
o archivo adicional se realizará en el directorio ./src

El ambiente de ejecución será  Python 3.14.3. 

Se instalará como pre-requisito un ambiente virtual (venv) donde ejecutará y los requisitos necesarios para su ejecución.

El programa tiene que ser implementado utilizando un esqueleto de proyecto como el provisto por cookiecutter.

Se crearán dos directorios adicionales en la estructura uno denominado script y el otro ejemplos que será gestionado por el programador humano.

Cada vez que se haga una modificación antes de darla por correcta se harán las siguientes validaciones, cualquier desvío será corregido automáticamente hasta que todos los puntos
puedan ejecutarse sin observaciones.

* Ejecutar ruff para validar las reglas de formato y que no de errores.
* Ejecutar black para validar el formato consistente.
* Utilizar y validar el correcto uso de reglas de formateo PEP8.
* Utilizar y validar el correcto uso de convenciones PEP257 para los docstrings, aceptar solo si no hay errores.
* Ejecutar MyPy para los modulos que no sean explícitamente puestos fuera de su alcance, aceptar solo si no hay errores.
* Ejecutar PyRight para los modulos que no sean explicitamente puestos fuera de su alcance, aceptar solo si no hay errores.
* Implementar test automático con Pytest con hipótesis de test unitario que permitan la cobertura del 90% o mejor.
* Utilizar bandit para la evaluación básica de seguridad y que no queden observaciones.
* Ejecutar multimetric mostrando los resultados de todos los parámetrosy reportar qué módulos tienen complejidad ciclomática superior a 10, se deberá procurar que la complejidad no exceda 15
* No utilizar Trufflehog en los controles de seguridad.
* Producir una documentación básica del funcionamiento del módulo y actualizarla con cada iteración exitosa, ese documento se llamará CHANGELOG.md.
* Debe generarse y mantenerse actualizado un archivo requirements.txt que se usará para las dependencias de librerías en caso que hubiera que incluir librerías adicionales.
* Si el proyecto tiene dependencias externas mandatorias u opcionales produce el archivo requirements.txt necesario.

Toda vez que sea posible hay que separar la lógica funcional de la lógica relacionada con la presentación e interacción con el usuario.

El programa debe utilizar técnicas de programación de object oriented. El programa debe implementar las funciones toda vez que sea posible mediante el uso de patrones.

Las funciones implementadas deben tener tratamiento y gestión de las excepciones producidas durante el runtime además de las que sean específicamente pedidas en la historia a implementar.

Produce un archivo comprimido con toda la estructura necesaria para subir el proyecto a GitHub.

El programa debe ser optimizado por performance.

El programa debe ser realizado en un formato tal que permita la utilización como package Python.

Las funciones implementadas deben tener tratamiento y gestión de las excepciones producidas durante el runtime además de las que sean específicamente pedidas en la historia a implementar. Produce un archivo comprimido con toda la estructura necesaria para subir el proyecto a GitHub.

El programa debe ser optimizado por performance.

Dada vez que se realiza un commit debe realizar las siguientes validaciones:

Que las modificaciones introducidas en cada iteración con el programador se revisen en todos los módulos y verificado que se han introducido las modificaciones para que sean aceptadas por todos.
Se hará una ejecución local de los programas que se harán en el workflow de validación y no se dará por correcto hasta que se solucionen todas las excepciones..
Cada vez que se introduzca un nuevo argumento o variable global se revisarán todos los módulos para que el mismo tenga correcta definición y uso.
Cada vez que se introduzca una nueva libraría o package Python se revisarán todos los módulos para que el mismo tenga correcta definción y uso.
Cada vez que se haga una modificación estructural en un módulo se hará un análisis de impacto en los restantes y se producirá una actualización para evitar problemas, excepciones, faltantes y otras inconsistencias.

Se mantendrá un script llamado regresion.sh (o regresion.cmd si se ejecuta en ambiente Windows) donde se ejecutarán todos los test cases.


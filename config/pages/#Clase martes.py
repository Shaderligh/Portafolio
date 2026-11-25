#Clase martes
#separar dentro del template, pages y projects. dentro de pages vamos a tener una de about me, experiencia y contactanos
#y dentro de projects vamos a tener proyectos. (todo html, proyectos va a usar sqlite) (o sea modelo de base de datos)
#dentro de la api pages, va a tener los archivos propios de urls.py y views.py
#crear mis porpios achivos dentro de pages
#api projects con urls.py(rutas) y views.py(logica)
#otra api perfiles o autenticacion (ejemplo)
#crear un msaterpage dentro de templates, llamandolo base.html (tendra el menu y un futher)
#en cada uno de los archivos que vayamos a usar, lo vamos a heredar (lo mandas a llamar con import)
#sintaxis jinja tags (python y html) {%   %}instrucciones, {{   }} variables, {#   #} comentarios
#no quiero que toque cierta seccion, va a ser con la clase hija (quien hereda el contenido)
#para que las secciones no tenga control la clase base se usa {%  %}, bloque.
#{% block nombre_del_bloque %} contenido {% endblock %}
#contenido es lo que pertenece a clases hijas.
#pedir a la ia que nos haga un menu con las opciones dea about me como prmera pagina, experiencia en la 2da
#que no cree las paginas, solo el menu, y que haga pie de pagina o futher 

#Miercoles
#para experiencia y proyectos necesitamos mostrar la informacion en cards, solo necesitamos la estructura
# en archivos ccs dentro de la carpeta start
#mandar solicitud hacia el archivo html 
#about.html
#como ya se escribio yodo lo relaciondo con html, estilos, pie de pagina, about me, no se vuelve a escribir toda la estrcutura de html
#lo que se va a hacer es heredar todo lo que se hizo importandolo para usarlo ahi, no se usa import, se usa condiciones de meter valores dentro de html, con extendsq
#con extends te traes todo lo del otro archivo
#lo del block content h1, es todo lo de lapagina, lo que se va a hacer es meterlo dentro del block content, para que se vea en la pagina
#about me no poder contenido solo algo sencillo
#ya casi esta por mostrar la primera pagina
#es importante que este dentor de los bloques, mismo nombre de html
#cuando este listo en servidor (ejemplo aws) o cualquier servidor en linea donde ya tenemos un dominio (parraskills)
#cuando akguuien solicita la pagina llega al servidor, el arfhivo escucha, revisa la ruta q solciitan la tiene ese arvchivo, si tiene la ruta agrra la solicitud y la envia al archivo de views
#mandarla a templates, la de abput me es lo q el usuario va a ver
#lo unico que va a ver es un "hola soy ___" y un menu, lo demas es codigo que no se ve
#tener propio administrador de rutas, en pages click derecho, nuevo archivo y sera el administrador de ruta local, urls.py
#escribir: from django.urls import path
#la ruta necesita saber que ruta es, necesito importar mis funciones desde views.py
#crear ruta: necesitamos el urlpatters
#como la primer pagina es una pagina principal (la de about me) no es necesario que le pongamos la ruta about me
#about me es la ruta raiz
#regresar al urls.py del congif, como es el principal hay q administrar ese
#path include, inlcuir dentro de pages urls, hay que decirle q lo imprima
#urls.py del config
#utiizando una fucnion no registrada, el include lo importamos en la cosa esa del path
#el ccs aplicado, el futher abajo, el h1 about me y el codigo ese q le genero la ia. titulo que le pusimos ese si tiene que aparecer.
#q se aplicara realemnte el ccs y la pagina principal de about me

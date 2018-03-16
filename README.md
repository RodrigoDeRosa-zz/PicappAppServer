# StoriesAppServer

### Linking Heroku + Git

Una vez que esta clonado el repo, abrir una consola en el directorio y hacer: <br/>
<br/>
&&&& git remote add heroku git@heroku.com:project.git<br/>
Y despues:<br/>
&&&& heroku git:remote -a project<br/>
<br/>
En nuestro caso, project es 'stories-app-server'.<br/>
Una vez que se hizo eso. Cada vez que se commitee se hace:<br/>
&&&& git add .<br/>
&&&& git commit -m msg<br/>
&&&& git push<br/>
&&&& git push heroku master<br/>
Esto hace que se actualice el repo nuestro y ademas la app que esta en la nube de 
Heroku.
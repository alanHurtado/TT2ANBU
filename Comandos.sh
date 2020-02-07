#   Proyecto comandos de instalacion Flask
#   Instalar previamente Flask y python 
#   Para instalar Flask
sudo pip install Flask
# ejecutar pagina
python principal.py

##::::::::::::::::::::::MySQL :::::::::::::::::::::::::::::::###
# Instalar MYSQL Fedora 31
sudo yum update 
# Instalamaos el paquete community-mysql-server
sudo yum install -y community-mysql-server
# Habilitar MySQL inicio 
sudo systemctl enable mysqld
# Iniciar el servicio
sudo systemctl start mysqld
# Detener el servicio
sudo systemctl stop mysqld
# conocer el estado 
sudo systemctl status mysqld
# en caso de solo querer el cliente MySQL
sudo yum install -y community-mysql
# Al instalar el server-MySQL el cliente ya esta instalado
# Configurar MySQL
# Geramos la contraseña a root
mysql -u root
# entrando a mysql ingreamos la contraseña 
alter user root@localhost identified by 'password';
# refrescamos la tabla de permisos
flush privileges;
exit
# ingresar a mysql
mysql -h localhost -u root -p
# creamos el usuario ANBU para el proyecto
create user ANBU identified by 'ANBUTT2';
# Damos los privilegios al usuario ANBU
grant all privileges on *.* to ANBU with grant option;
# refrescamos la tabla de permisos 
flush privileges;
exit
## ::::: Conexion remota MysQL :::::::::#
# Checar o habilitar el puerto 3306
# habilitar el acceso remoto en el firewall 
sudo firewall-cmd --permanent --add-service=mysql
# cargar el cambio
sudo firewall-cmd --reload
###::::::::::::Fin Instalacion MySQL ::::::::::::::##

##::::::: Generar la BD para ANBU :::::::::::##
# ejecutar el script en el usuario ANBU
source DataBaseANBU.sql

##::::::::::: MySQL for flask :::::::::::::##
sudo pip install flask-mysql
 


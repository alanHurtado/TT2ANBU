USE anbuDB;
-------------08/JUNIO/2020
ALTER TABLE Arma
MODIFY COLUMN porcentaje FLOAT;

ALTER TABLE Arma
MODIFY COLUMN evaluacion_arma FLOAT;

ALTER TABLE Arma 
MODIFY COLUMN idArma INT NOT NULL AUTO_INCREMENT;
--------------------------------------

-------------MAYO/2020
ALTER TABLE Publicacion
MODIFY COLUMN descripcion varchar(2200);

ALTER TABLE Publicacion
CHANGE url urlPublicacion varchar(500);

ALTER TABLE Publicacion
ADD COLUMN urlImagen varchar(500);
--------------------------------------
USE anbuDB;

ALTER TABLE Publicacion
MODIFY COLUMN descripcion varchar(2200);

ALTER TABLE Publicacion
CHANGE url urlPublicacion varchar(500);

ALTER TABLE Publicacion
ADD COLUMN urlImagen varchar(500);
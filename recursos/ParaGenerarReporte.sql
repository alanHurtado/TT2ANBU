INSERT INTO Busqueda VALUES (108, 'Juan perez', '2020-06-18 13:17:17');
INSERT INTO Busqueda VALUES (109, 'Roberto0981', '2020-06-24 23:37:43');
INSERT INTO Busqueda VALUES (110, 'AlanAS', '2020-06-23 14:17:37');

INSERT INTO Perfil Values (148, 'juanalmudevar', 'JJuan Perez', 'https://www.instagram.com/juanalmudevar/');

INSERT INTO busqueda_perfil VALUES(108, 148);

INSERT INTO Publicacion VALUE(1004, 148, 'CDMX Av Polanco', '2019-08-23 14:17:37', 'https://www.instagram.com/p/B9t7LF8oRfR/', 'En venta', 0, 1, 'tmp/post_img/108/148-1004.jpg', null);
INSERT INTO Publicacion VALUE(1005, 148, 'CDMX Av Polanco', '2019-03-23 04:21:13', 'https://www.instagram.com/p/B9t7LF8oRfR/', null, 1, 1, 'tmp/post_img/108/148-1005.jpg', null);
INSERT INTO Publicacion VALUE(1006, 148, 'CDMX Av Polanco', '2018-07-23 20:21:32', 'https://www.instagram.com/p/B9t7LF8oRfR/', 'En venta', 0, 0, 'tmp/post_img/108/148-1006.jpg', null);

DELETE FROM Publicacion WHERE idPerfil=148;


INSERT INTO Rostro VALUE(21, 1004, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
INSERT INTO Rostro VALUE(20, 1005, 45, 65, 78, 79, 86, 76, 89, 32, 11, 56);
INSERT INTO Rostro VALUE(3, 1006, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

INSERT INTO Arma VALUE(20, 1004, 45, 45);
INSERT INTO Arma VALUE(21, 1005, 75, 75);
INSERT INTO Arma VALUE(23, 1006, 0, 0);
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: pagweb
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `maestro_materia`
--

DROP TABLE IF EXISTS `maestro_materia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maestro_materia` (
  `idMaestro_Materia` int NOT NULL AUTO_INCREMENT,
  `idMaestro` int NOT NULL,
  `idMateria` int NOT NULL,
  PRIMARY KEY (`idMaestro_Materia`),
  UNIQUE KEY `idMaestro` (`idMaestro`,`idMateria`),
  KEY `idMateria` (`idMateria`),
  CONSTRAINT `maestro_materia_ibfk_1` FOREIGN KEY (`idMaestro`) REFERENCES `maestros` (`idMaestro`),
  CONSTRAINT `maestro_materia_ibfk_2` FOREIGN KEY (`idMateria`) REFERENCES `materias` (`idMateria`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maestro_materia`
--

LOCK TABLES `maestro_materia` WRITE;
/*!40000 ALTER TABLE `maestro_materia` DISABLE KEYS */;
INSERT INTO `maestro_materia` VALUES (1,1,1),(2,1,2),(3,2,1),(4,3,5),(5,4,6),(6,5,7),(7,6,9);
/*!40000 ALTER TABLE `maestro_materia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `maestros`
--

DROP TABLE IF EXISTS `maestros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `maestros` (
  `idMaestro` int NOT NULL AUTO_INCREMENT,
  `nombreMaestro` varchar(500) NOT NULL,
  PRIMARY KEY (`idMaestro`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `maestros`
--

LOCK TABLES `maestros` WRITE;
/*!40000 ALTER TABLE `maestros` DISABLE KEYS */;
INSERT INTO `maestros` VALUES (1,'María García'),(2,'Carlos López'),(3,'Ana Martínez'),(4,'Pedro Rodríguez'),(5,'Luisa Fernández'),(6,'Diego Armando ');
/*!40000 ALTER TABLE `maestros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materias`
--

DROP TABLE IF EXISTS `materias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materias` (
  `idMateria` int NOT NULL AUTO_INCREMENT,
  `nombreMateria` varchar(500) NOT NULL,
  PRIMARY KEY (`idMateria`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materias`
--

LOCK TABLES `materias` WRITE;
/*!40000 ALTER TABLE `materias` DISABLE KEYS */;
INSERT INTO `materias` VALUES (1,'Física'),(2,'Química'),(3,'Literatura'),(4,'Historia'),(5,'Biología'),(6,'Programación'),(7,'Inglés'),(8,'Arte'),(9,'Filosofía'),(10,'Educación Física');
/*!40000 ALTER TABLE `materias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `peticiones`
--

DROP TABLE IF EXISTS `peticiones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `peticiones` (
  `idPeticion` int NOT NULL AUTO_INCREMENT,
  `nombreMaestro` varchar(100) NOT NULL,
  `nombreMateria` varchar(100) NOT NULL,
  `mensaje` text,
  `idUsuario` int NOT NULL,
  PRIMARY KEY (`idPeticion`),
  KEY `idUsuario` (`idUsuario`),
  CONSTRAINT `peticiones_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `peticiones`
--

LOCK TABLES `peticiones` WRITE;
/*!40000 ALTER TABLE `peticiones` DISABLE KEYS */;
INSERT INTO `peticiones` VALUES (1,'Juan Pérez','Matemáticas','Por favor agregar esta materia con este maestro',1),(2,'María López','Física','Necesitamos un maestro para física avanzada',2),(3,'Carlos Ruiz','Química','Solicito que se incluya esta materia con este maestro',1),(4,'Ana Gómez','Historia','Agregar historia moderna con esta profesora',2),(5,'Luis Fernández','Programación','Incluir programación avanzada con este maestro',1);
/*!40000 ALTER TABLE `peticiones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reacciones`
--

DROP TABLE IF EXISTS `reacciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reacciones` (
  `idUsuario` int NOT NULL,
  `idReseña` int NOT NULL,
  `idTipo` int NOT NULL,
  PRIMARY KEY (`idUsuario`,`idReseña`),
  KEY `idReseña` (`idReseña`),
  KEY `idTipo` (`idTipo`),
  CONSTRAINT `reacciones_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`),
  CONSTRAINT `reacciones_ibfk_2` FOREIGN KEY (`idReseña`) REFERENCES `reseñas` (`idReseña`),
  CONSTRAINT `reacciones_ibfk_3` FOREIGN KEY (`idTipo`) REFERENCES `tipo_reaccion` (`idTipo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reacciones`
--

LOCK TABLES `reacciones` WRITE;
/*!40000 ALTER TABLE `reacciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `reacciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reseñas`
--

DROP TABLE IF EXISTS `reseñas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reseñas` (
  `idReseña` int NOT NULL AUTO_INCREMENT,
  `comentario` text NOT NULL,
  `calificacion` int NOT NULL,
  `idUsuario` int NOT NULL,
  `idMaestro_Materia` int NOT NULL,
  `reportada` tinyint(1) DEFAULT '0',
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idReseña`),
  KEY `idUsuario` (`idUsuario`),
  KEY `idMaestro_Materia` (`idMaestro_Materia`),
  CONSTRAINT `reseñas_ibfk_1` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`),
  CONSTRAINT `reseñas_ibfk_2` FOREIGN KEY (`idMaestro_Materia`) REFERENCES `maestro_materia` (`idMaestro_Materia`),
  CONSTRAINT `reseñas_chk_1` CHECK ((`calificacion` between 1 and 5))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reseñas`
--

LOCK TABLES `reseñas` WRITE;
/*!40000 ALTER TABLE `reseñas` DISABLE KEYS */;
INSERT INTO `reseñas` VALUES (1,'Muy buena explicación y siempre disponible para resolver dudas.',5,1,1,0,'2025-07-02 21:30:50'),(2,'La clase es un poco difícil, pero aprendí mucho.',4,2,1,0,'2025-07-02 21:30:50'),(3,'Excelente profesora, hace que la química sea fácil de entender.',5,3,2,0,'2025-07-02 21:30:50'),(4,'El profesor explica claro y da muchos ejemplos.',4,1,3,0,'2025-07-02 21:30:50'),(5,'Me gustó mucho la manera de enseñar biología, muy dinámica.',5,2,4,0,'2025-07-02 21:30:50'),(6,'Pedro es paciente y explica bien la programación.',4,3,5,0,'2025-07-02 21:30:50'),(7,'Clases de inglés muy interesantes y útiles.',5,1,6,0,'2025-07-02 21:30:50'),(8,'Buen maestro, muy puntual',4,5,7,0,'2025-07-04 23:24:03');
/*!40000 ALTER TABLE `reseñas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `idRol` int NOT NULL AUTO_INCREMENT,
  `NomRol` varchar(13) NOT NULL,
  PRIMARY KEY (`idRol`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Estudiante'),(2,'Administrador');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_peticion`
--

DROP TABLE IF EXISTS `tipo_peticion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_peticion` (
  `idRol_Peticion` int NOT NULL AUTO_INCREMENT,
  `Nom_Peticion` varchar(13) NOT NULL,
  PRIMARY KEY (`idRol_Peticion`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_peticion`
--

LOCK TABLES `tipo_peticion` WRITE;
/*!40000 ALTER TABLE `tipo_peticion` DISABLE KEYS */;
INSERT INTO `tipo_peticion` VALUES (1,'Materia'),(2,'Maestro');
/*!40000 ALTER TABLE `tipo_peticion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_reaccion`
--

DROP TABLE IF EXISTS `tipo_reaccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_reaccion` (
  `idTipo` int NOT NULL,
  `nombre` varchar(20) NOT NULL,
  PRIMARY KEY (`idTipo`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_reaccion`
--

LOCK TABLES `tipo_reaccion` WRITE;
/*!40000 ALTER TABLE `tipo_reaccion` DISABLE KEYS */;
INSERT INTO `tipo_reaccion` VALUES (2,'dislike'),(1,'like');
/*!40000 ALTER TABLE `tipo_reaccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `idUsuario` int NOT NULL AUTO_INCREMENT,
  `NomUsuario` varchar(40) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `idRol` int NOT NULL,
  PRIMARY KEY (`idUsuario`),
  KEY `idRol` (`idRol`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`idRol`) REFERENCES `roles` (`idRol`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Fatima','scrypt:32768:8:1$X9rPkZ3Ti3hjcghA$97de1fe6bbc34404642739bbb25f2e374ac8f174a293515e8073b0a536d1dde3c580ee3c64c6a6318ccf6dc52f9d65b816f9bfd018806bcb3c431e3cba44dbcc',1),(2,'Ana','scrypt:32768:8:1$JpAwINiPfPrD62N4$0f9ee4afd0736610efcafd37fef78e0daf1f40d9c0b1abbff6c3133a0fac3a13080e65fdb5423be2a749aeb64386b4807c84b9a695e1a5d3b97b850ac9386bde',1),(3,'Sebastian','scrypt:32768:8:1$oKH0gX0180AsUnI3$afed5c8c869e9133ed5712272f76c215f161f8aa08a94612537a9a295c8aa7bbce762ee3a2ce526c94efb967f6627977c2db89069435c140b1d0fca2159df35c',1),(4,'Angel','scrypt:32768:8:1$ZexarVUgqLdEgV1M$056b1695ede07c2ef66b465c692c6a369bc3abd21580ffc80a5009dbe0340b2929be7023551b09ec0c52999d9167d37368b8abda400e6ca6d37f7a71f4c2659d',1),(5,'Emiliano','scrypt:32768:8:1$uG92Ojnw0Ub3wvH5$f07c26f7b5f7203c7b1d9bc371b9066899eb2320da5a210b39247d22d9a3bb27fd43e3ed6e47c8b9ae5e954130004e49410a82f9106c5da9b5971e19fbfa8d36',2),(6,'Emiliano2','scrypt:32768:8:1$OGd8uAOXqhobxd1z$34133614ea1f12cfa77b1cc1f4ad71d003446190396076bb952c78815faa49eeca592d5d7eafe05a18b1300c87e47be6b12a114a018c9e6ae1040785c180582f',1),(7,'Dante','scrypt:32768:8:1$wbY3Y5WsfIMIZzOO$e4ab6adfa9112d35381bcf62c7f5d205a91ba5ce615533a1463437112be4fee0d62724e2f3f11af00ee9dd0a9c3f72b17312d1ae6ebf9f30b3ea628e5909a103',1),(8,'Santiago','scrypt:32768:8:1$vtYx4eSTHrB78xle$f7aec8202f3dbd3e2f79c980a4fff6081217e60fc3b5f9969c9e094454f6629a0cb8f209d3936c2e91188a9121ed12dbda478a66b9486d03d3b24529331c4818',1);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-04 17:26:24

-- MySQL dump 10.13  Distrib 5.5.62, for Win64 (AMD64)
--
-- Host: localhost    Database: tweeter
-- ------------------------------------------------------
-- Server version	5.5.5-10.5.12-MariaDB-0+deb11u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `tweet_id` int(10) unsigned NOT NULL,
  `content` varchar(150) COLLATE utf8mb4_bin NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `comment_FK_1` (`tweet_id`),
  KEY `comment_FK` (`user_id`),
  CONSTRAINT `comment_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_FK_1` FOREIGN KEY (`tweet_id`) REFERENCES `tweet` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,20,6,'comment!','2022-02-24 18:30:12'),(2,20,6,'made in postman','2022-02-24 18:47:27');
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment_like`
--

DROP TABLE IF EXISTS `comment_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comment_like` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `comment_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `comment_like_UN` (`user_id`,`comment_id`),
  KEY `comment_like_FK_1` (`comment_id`),
  CONSTRAINT `comment_like_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_like_FK_1` FOREIGN KEY (`comment_id`) REFERENCES `comment` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment_like`
--

LOCK TABLES `comment_like` WRITE;
/*!40000 ALTER TABLE `comment_like` DISABLE KEYS */;
INSERT INTO `comment_like` VALUES (3,5,1),(1,20,1);
/*!40000 ALTER TABLE `comment_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follow`
--

DROP TABLE IF EXISTS `follow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `follow` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `follow_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `follow_UN` (`user_id`,`follow_id`),
  KEY `follow_FK_1` (`follow_id`),
  CONSTRAINT `follow_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `follow_FK_1` FOREIGN KEY (`follow_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follow`
--

LOCK TABLES `follow` WRITE;
/*!40000 ALTER TABLE `follow` DISABLE KEYS */;
/*!40000 ALTER TABLE `follow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweet`
--

DROP TABLE IF EXISTS `tweet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `userId` int(10) unsigned NOT NULL,
  `content` varchar(500) COLLATE utf8mb4_bin NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `imageUrl` varchar(1000) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tweet_FK` (`userId`),
  CONSTRAINT `tweet_FK` FOREIGN KEY (`userId`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweet`
--

LOCK TABLES `tweet` WRITE;
/*!40000 ALTER TABLE `tweet` DISABLE KEYS */;
INSERT INTO `tweet` VALUES (3,20,'woohoo','2022-02-22 21:20:29',NULL),(4,5,'yay','2022-02-22 21:20:29',NULL),(5,20,'This was made in postman!','2022-02-23 13:33:32',NULL),(6,20,'woohoo','2022-02-23 13:36:14','new_image');
/*!40000 ALTER TABLE `tweet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tweet_like`
--

DROP TABLE IF EXISTS `tweet_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tweet_like` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `tweet_id` int(10) unsigned NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tweet_like_UN` (`tweet_id`,`user_id`),
  KEY `tweet_like_FK` (`user_id`),
  CONSTRAINT `tweet_like_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tweet_like_FK_1` FOREIGN KEY (`tweet_id`) REFERENCES `tweet` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tweet_like`
--

LOCK TABLES `tweet_like` WRITE;
/*!40000 ALTER TABLE `tweet_like` DISABLE KEYS */;
INSERT INTO `tweet_like` VALUES (6,3,21),(2,5,5),(1,6,5),(4,6,20);
/*!40000 ALTER TABLE `tweet_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `username` varchar(15) COLLATE utf8mb4_bin NOT NULL,
  `bio` varchar(150) COLLATE utf8mb4_bin NOT NULL,
  `birthdate` date NOT NULL,
  `imageUrl` varchar(1000) COLLATE utf8mb4_bin DEFAULT NULL,
  `bannerUrl` varchar(1000) COLLATE utf8mb4_bin DEFAULT NULL,
  `password` varchar(150) COLLATE utf8mb4_bin NOT NULL,
  `salt` varchar(15) COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `emailUK` (`email`),
  UNIQUE KEY `username_UN` (`username`),
  CONSTRAINT `user_CHECK` CHECK (octet_length(`username`) > 3)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (4,'email@testing.ca','test4','a new bio','1991-01-01',NULL,NULL,'f71cf5fb68421b15e987c6dccfd1b054aaf81a6f04a8f495e639e40388527ff0748cec8a3f0bc4f060602b3133aaab4c609764e4a21584e7d09b58e88b0b2ea0','8V1NlFMpYmduDg'),(5,'email3@testing.ca','test43','a new bio3','1991-01-01',NULL,NULL,'20cf2a1e1d88acc37466d2624429f30a68b7d237a3c999c0808bc08250f9db76d7b6edcb081eaee12d68073c5d7bf2ebda3b3d762a85bba80298caacb91099f9','-ppXIDkbZGdGSw'),(6,'email34@testing.ca','test434','a new bio34','1991-01-01',NULL,NULL,'ecc555ec7932f22872da4dfdec17804bf6c0e41ca526ccbdc76c383b95c654c1178fd1606d7cb92e9a9639ab6f0dec6be6157a2d4870a43b16b87399db6e3011','R1lW4l0YRP-mXQ'),(7,'email344@testing.ca','test4344','a new bio344','1991-01-01',NULL,NULL,'ea4dda5a4a52695036ff991c1fe73656bfbc425d554394fca9c3e7b50a3d5c06759f6fd2c53c0042c3abf7dfdf10b3952c2868b9d48800082595c6116568c20e','EfrztcLuQh-m0w'),(8,'email3443@testing.ca','test43443','a new bio3443','1991-01-01',NULL,NULL,'31a2ca13d2c714cc22f79d5a0756bd9f55d5bc5ae0627b1f25726d28cfbdf457524ddc70408849c46fddcb71103b3c079b2732f8d7908513a25399834f220b6e','yLq4QKu7Jg127w'),(9,'email34432@testing.ca','test434432','a new bio34432','1991-01-01',NULL,NULL,'ce8c9bf3812854990a73af5825a5a5ff859bd5d9e836ece2437392f24442278d35cf4b1bd21bd122557334457bfad94587218797eabe3e36a89c18bbf899b0c5','IFUhIbwa0p_Y1Q'),(10,'email3422432@testing.ca','test4344322','a new bio3222432','1991-01-01',NULL,NULL,'59fdffded5a0611ddf4975192ce188f95b9cc24579ae08db30de517a4f3ad21ef40a289be33be0c2e1cd7b197c401be34a5f30f0d117680604ec6d11c1d2ad1e','8wXW8UuE7D3AVg'),(11,'email3421112432@testing.ca','test4111344322','a new bio3222111432','1991-01-01',NULL,NULL,'dcdc76e1dd0946aa5db9c1700b4045d47fd4309c8b879405c8611b3ac6a830154dd8027232c2ebd5b82cc1311508e3788b88b509b69e4af9dcf3515dc0fbd01b','m3Jt3PI-Q3dCWw'),(20,'email500@testing.ca','test500','a new bio500','1991-01-01',NULL,NULL,'e7c62978992d41a311ebe074649362262a6f094f65e51eeb1aa4bb627bf7ab779f4aeee9650f17f2350e16cdb70ea54bd71db1811bd387372e55c06ebfe418d8','rI8oUDf_zRqctA'),(21,'myemail','colton','woohoo','1991-05-05',NULL,NULL,'766d95ec6e47e8759052bbbcca80fccc3e5a312e125df2b15e40a03ffd0c97a3de14e6070810f0b63b4535c9f332efd0b336b82d6670831e7437a7cddcd46315','z8gtQun8_vgw4Q');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_session`
--

DROP TABLE IF EXISTS `user_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_session` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `logintoken` varchar(45) COLLATE utf8mb4_bin NOT NULL DEFAULT substr(md5(rand()),1,40),
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_session_UN` (`logintoken`),
  KEY `user_session_FK` (`user_id`),
  CONSTRAINT `user_session_FK` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_session`
--

LOCK TABLES `user_session` WRITE;
/*!40000 ALTER TABLE `user_session` DISABLE KEYS */;
INSERT INTO `user_session` VALUES (15,9,'ccfca26c699522e524c9b05b0f07fc49'),(16,10,'5705722eb2b568be78c0ed8aeb856c60'),(29,20,'ea2a9cbd147caa98509c785430b3715f'),(31,21,'23eb76747a6f15b5f5e8a887de503d49');
/*!40000 ALTER TABLE `user_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'tweeter'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-26 13:29:47

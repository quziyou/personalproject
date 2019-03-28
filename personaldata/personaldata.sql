-- MySQL dump 10.13  Distrib 8.0.12, for Linux (x86_64)
--
-- Host: localhost    Database: personaldata
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_info`
--

DROP TABLE IF EXISTS `account_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `account_info` (
  `account` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `acc_passwd` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `mon_passwd` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `acc_str` varchar(25) DEFAULT NULL,
  `mon_str` varchar(25) NOT NULL,
  `category` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `url` varchar(256) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `note` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `createtime` datetime DEFAULT NULL,
  `updatetime` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_info`
--

LOCK TABLES `account_info` WRITE;
/*!40000 ALTER TABLE `account_info` DISABLE KEYS */;
INSERT INTO `account_info` VALUES ('quziyou@hotmail.com','SNnJcXrxjXyVxdG4sF22VtlPASgVFFdjBwK0BMHnkOD4BHKvZzvAKYRnq4uOXXr5','','422200@LiuYing00','','hotmail','https://www.hotmail.com','hotmail邮箱','2018-09-13 11:26:55','2018-09-13 11:26:55'),('zhuoshuijun@hotmail.com','k3s2aT/y8JnVlczYOURMjDs+17KaDb8hcSDl586wjrxy+pgJacN4mWFn/TPekLgm','','422200@LiuYing00','','hotmail','https://www.hotmail.com','hotmail邮箱','2018-09-13 11:30:08','2018-09-13 11:30:08'),('quziyou@outlook.com','xuHXvcockf50C41Iilp/zk3L5sb3vN7vkniZ2reAlXXSPAiiqqyzg9fWhlxmRC9l','','422200@LiuYing00','','hotmail','https://www.hotmail.com','outlook邮箱','2018-09-13 11:32:13','2018-09-13 11:32:13'),('quziyou@hotmail.com','oES020zKyi6Okk5/utN2G24Zt/13AO6InB5mivXe+YAKz3YrDViVAZQym6mItDud','dYwG5BMBQhivmHySbDRAJ2OammOot+JXbAa2ajJb3E02qyRsDLpvZDI/3O1j3cOC','422200@LiuYing00','422200@LiuYing00','huobi','https://www.huobi.com','火币网','2018-09-13 11:33:56','2018-09-13 11:33:56'),('zhuoshuijun@hotmail.com','fyTH8zU4LzD8owG4qdXV4hPKwRs9q90t1Zllzrqu4RkvnxVvxHOTEbWz24xiE3jr','','422200@LiuYing00','','yunbi','https://www.yunbi.com','云币网','2018-09-13 11:35:24','2018-09-13 11:35:24'),('zhuoshuijun@hotmail.com','WvUSkLUayWdFq4dBiGuzt8SWCDU/+VeW6gTx07T6rxfZXdI+R4OwBB/8JDMKaPDK','+VFFoVkchaeaRcdPOSVvKR2J7NiZjUNU0XGRXU9njrsxZ6cEY75AGJA5sc9H/pTZ','422200@LiuYing00','422200@LiuYing00','ico365','https://ico365.com','ico365','2018-09-13 11:36:41','2018-09-13 11:36:41'),('quziyou@hotmai.com','lJsytQMyULZPUOQL1hVLWCPlPClfSh+OwdIgQFbVCMoyeVM+5OjemcbTNOgbeHBC','Xnjx+GvpWBtUIX8dOXv8+OgSwImDYw5Ya29ZHon5DmTvUk7IU7ds3gI8vMzK2/BS','422200@LiuYing00','422200@LiuYing00','bter','https://bter.com','比特儿','2018-09-13 11:38:07','2018-09-13 11:38:07'),('13902948276','mRWVphCn+LSFT8LSV03iHmVHJsfDVSkzuIwYwxdmm4G9lL8tsRKLC7ohY9vbf4GH','','422200@LiuYing00','','imtoken','','imtoken','2018-09-13 11:39:13','2018-09-13 11:39:13'),('1641592421','tahd206utMY9KiVlnw49WpeuS8EcoN9qe8FaD2vtDETjVqgfLctOUgW0lWjqxsuz','','422200@LiuYing00','','guangda','','光大银行','2018-09-13 11:40:25','2018-09-13 11:40:25'),('quziyou@hotmail.com','wL+gPLkHxT8TJ2GMSdo2YhQJlZh7hbdXJBuLIlgzd5l26+bP9ZsS6yvVjn24XkU8','','422200@LiuYing00','','appleid','','apple id','2018-09-16 21:41:41','2018-09-16 21:41:41'),('13902948276','3yT2DUYTx58cxmq8ncqujT2ApQWKCn5fbmzz9pPIIglqxkeOQtT/vTQ489UdGInK','','qijdcsjgio12xs8d','','okex','https://www.okex.com','okex帐号','2018-09-16 21:44:17','2018-09-16 21:44:17');
/*!40000 ALTER TABLE `account_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account` varchar(50) DEFAULT NULL,
  `acc_passwd` varchar(20) DEFAULT NULL,
  `mon_passwd` varchar(20) DEFAULT NULL,
  `category` varchar(20) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `note` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test`
--

LOCK TABLES `test` WRITE;
/*!40000 ALTER TABLE `test` DISABLE KEYS */;
INSERT INTO `test` VALUES (1,'quziyou@hotmail.com','5389ZhuoShuiJun',NULL,'Email','http://www.hotmail.com','微软账户'),(2,'zhuoshuijun@hotmail.com','8276LiuYing',NULL,'Email','http://www.hotmail.com','微软账户'),(3,'quziyou@outlook.com','8276LiuYing',NULL,'Email','http://www.hotmail.com','微软账户'),(4,'quziyou@hotmail.com','5389@LiuYing','1013@YeJia','DIGICCY','https://www.huobi.com/','火币网'),(5,'zhuoshuijun@hotmail.com','0871@YeJia',NULL,'DIGICCY','https://yunbi.com/','云币网'),(6,'zhuoshuijun@hotmail.com','5389@LiuYing','0871@YeJia','DIGICCY','https://www.ico365.com/','ico365'),(7,'quziyou@hotmail.com','5389@LiuYing','0871@YeJia','DIGICCY','https://bter.com/','比特儿'),(8,'13902948276','0739@KunMing',NULL,'DIGICCY',NULL,'imotoken'),(9,'1641592421','5389@LiuYing',NULL,NULL,NULL,'光大网银');
/*!40000 ALTER TABLE `test` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-17 10:57:58

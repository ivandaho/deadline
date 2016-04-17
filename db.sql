-- MySQL dump 10.13  Distrib 5.7.11, for Linux (x86_64)
--
-- Host: localhost    Database: test
-- ------------------------------------------------------
-- Server version	5.7.11

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
-- Table structure for table `groups`
--

DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groups` (
  `group_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `groupname` varchar(45) NOT NULL,
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groups`
--

LOCK TABLES `groups` WRITE;
/*!40000 ALTER TABLE `groups` DISABLE KEYS */;
INSERT INTO `groups` VALUES (1,'School'),(2,'Family'),(3,'Friends'),(4,'Computer Science Club'),(5,'Work');
/*!40000 ALTER TABLE `groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `people`
--

DROP TABLE IF EXISTS `people`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `people` (
  `firstname` varchar(40) NOT NULL,
  `lastname` varchar(40) NOT NULL,
  `tel` bigint(20) unsigned NOT NULL,
  `person_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `people`
--

LOCK TABLES `people` WRITE;
/*!40000 ALTER TABLE `people` DISABLE KEYS */;
INSERT INTO `people` VALUES ('Cassie','Hagemeier',5552948102,4),('Madlyn','Wenger',5551129818,5),('Ignacio','Britto',5558891210,6),('Kalla','Engelke',5553539212,7),('Olivia','Wheless',5553593431,8),('Harley','Fanser',5558012565,9),('Victor','Vines',5559908888,10),('Madlyn','Wenger',5551129818,11);
/*!40000 ALTER TABLE `people` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pg`
--

DROP TABLE IF EXISTS `pg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pg` (
  `people_person_id` int(10) unsigned NOT NULL,
  `group_group_id` int(10) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pg`
--

LOCK TABLES `pg` WRITE;
/*!40000 ALTER TABLE `pg` DISABLE KEYS */;
INSERT INTO `pg` VALUES (4,1),(5,1),(6,1),(8,1),(10,2),(11,2),(4,3),(5,3),(7,3),(9,3),(4,4),(5,4),(8,4),(6,5),(7,5);
/*!40000 ALTER TABLE `pg` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wt`
--

DROP TABLE IF EXISTS `wt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wt` (
  `name` varchar(80) DEFAULT NULL,
  `timereq` int(10) unsigned NOT NULL,
  `doby` datetime NOT NULL,
  `job_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB AUTO_INCREMENT=35939 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wt`
--

LOCK TABLES `wt` WRITE;
/*!40000 ALTER TABLE `wt` DISABLE KEYS */;
INSERT INTO `wt` VALUES ('laundry',86400,'2016-04-18 20:01:00',35915),('something new on same date',604800,'2016-04-27 23:46:43',35916),('paper',172800,'2016-04-08 14:00:00',35917),('csc club meeting',0,'2016-04-09 11:00:00',35918),('database project',604800,'2016-04-29 08:00:00',35919),('test new on 25th',86400,'2016-04-25 08:00:00',35920),('new item in may',604800,'2016-05-02 08:00:00',35921),('second new item in may',86400,'2016-05-15 08:00:00',35922),('Classes begin',0,'2016-01-11 00:00:00',35923),('Payday',0,'2016-02-03 00:00:00',35924),('Career offices appointment',0,'2016-02-05 20:00:00',35925),('Csc  club meeting',0,'2016-02-08 16:00:00',35926),('Career fair',0,'2016-02-10 12:30:00',35927),('Csc club meeting',0,'2016-02-19 16:00:00',35928),('Facility recital',0,'2016-02-20 00:30:00',35929),('Pep band',0,'2016-02-20 18:20:00',35930),('Music thing',0,'2016-02-21 15:50:00',35931),('Music theory class in chapel',0,'2016-02-22 15:00:00',35932),('Chinese dinner with President',0,'2016-02-26 22:30:00',35933),('Csc club field trip',0,'2016-02-29 17:00:00',35934),('Spring break',0,'2016-03-05 00:00:00',35935),('Potential band gig date',0,'2016-03-24 00:00:00',35936),('8am Final Exams',0,'2016-04-28 12:00:00',35937),('class starts',0,'2016-08-22 09:00:00',35938);
/*!40000 ALTER TABLE `wt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wt2`
--

DROP TABLE IF EXISTS `wt2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wt2` (
  `name` varchar(80) DEFAULT NULL,
  `timereq` int(10) unsigned NOT NULL,
  `doby` datetime NOT NULL,
  `group_id` int(10) unsigned NOT NULL,
  `job_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`job_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wt2`
--

LOCK TABLES `wt2` WRITE;
/*!40000 ALTER TABLE `wt2` DISABLE KEYS */;
INSERT INTO `wt2` VALUES ('CSC Club Meeting',0,'2016-04-08 11:00:00',4,1),('ENG 212 Response Paper #7',172800,'2016-04-13 13:00:00',1,2),('Final Exams',0,'2016-04-28 08:00:00',1,3),('Database Project',1209600,'2016-04-22 08:00:00',1,4),('Important test I need to study for',432000,'2016-05-03 11:00:00',1,5),('Start Work',0,'2016-05-09 09:00:00',5,6),('Harley\'s End of School Party',0,'2016-05-07 18:00:00',3,7),('Family Gathering',0,'2016-05-22 18:00:00',2,8),('ENG 212 Final Paper',604800,'2016-05-02 11:00:00',1,9),('CSC 420 Database Programming Final Exam',0,'2016-04-29 00:00:00',1,10),('my new job, 6th of april',18120,'2016-04-06 12:00:00',3,23),('my job',259200,'2016-04-07 12:00:00',2,24);
/*!40000 ALTER TABLE `wt2` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-04-17 14:16:41

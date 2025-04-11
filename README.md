data(유저테이블) 생성쿼리

CREATE TABLE `data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(200) NOT NULL,
  `userid` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  `phonenumber` int(11) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `filename` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_username` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci

events(모임테이블) 생성쿼리

CREATE TABLE `events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `filename` varchar(255) DEFAULT NULL,
  `userid` varchar(255) DEFAULT NULL,
  `views` int(11) DEFAULT 0,
  `entryfee` int(11) DEFAULT 0,
  `application_start_date` datetime NOT NULL,
  `application_end_date` datetime NOT NULL,
  `latitude` varchar(200) DEFAULT '37.5665',
  `longitude` varchar(200) DEFAULT '126.9780',
  `contents` blob DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci

event_participants (유저와 모임테이블의 관계테이블) 생성쿼리

CREATE TABLE `event_participants` (
  `participant_id` varchar(200) NOT NULL,
  `event_id` int(11) NOT NULL,
  `registration_time` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`participant_id`,`event_id`),
  KEY `event_id` (`event_id`),
  CONSTRAINT `event_participants_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci



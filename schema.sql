DROP TABLE IF EXISTS book;

CREATE TABLE IF NOT EXISTS `books` (
    `cover` varchar NOT NULL,
    `title` varchar(50) NOT NULL,
    `descr` varchar(255) NOT NULL,
    `author` varchar(100) NOT NULL,
    `publisher` varchar(100) NOT NULL,
    `pub_date` date NOT NULL,
    `genres` varchar(100) NOT NULL,
    `lang` varchar(50) NOT NULL,
    `pages` int(5) NOT NULL,
    `comp` varchar(100) NOT NULL,
    `price` decimal(20) NOT NULL,
    `rating` float(5) NOT NULL,
    `tot_rat` int(10) NOT NULL
)

CREATE TABLE IF NOT EXISTS `accounts` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `accounts` (`id`, `username`, `password`, `email`) VALUES (1, 'test', 'test', 'test@test.com');

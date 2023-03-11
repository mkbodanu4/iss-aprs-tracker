CREATE TABLE `history`
(
    `date`         DATETIME       NOT NULL,
    `from`         VARCHAR(20)    NOT NULL,
    `comment`      TEXT           NULL DEFAULT NULL,
    `to`           VARCHAR(20)    NULL DEFAULT NULL,
    `addresse`     VARCHAR(20)    NULL DEFAULT NULL,
    `message_text` TEXT           NULL DEFAULT NULL,
    `latitude`     DECIMAL(10, 8) NULL DEFAULT NULL,
    `longitude`    DECIMAL(11, 8) NULL DEFAULT NULL,
    `raw`          TEXT           NULL DEFAULT NULL,
    CONSTRAINT `from_date` PRIMARY KEY (`date`, `from`),
    INDEX `from` (`from`)
) ENGINE = InnoDB;
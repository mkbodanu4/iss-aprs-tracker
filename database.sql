CREATE TABLE `history`
(
    `date`      DATETIME       NOT NULL,
    `call_sign` VARCHAR(20)    NOT NULL,
    `comment`   TEXT           NULL DEFAULT NULL,
    `latitude`  DECIMAL(10, 8) NULL DEFAULT NULL,
    `longitude` DECIMAL(11, 8) NULL DEFAULT NULL,
    `raw`       TEXT           NULL DEFAULT NULL,
    CONSTRAINT `call_sign_date` PRIMARY KEY (`date`, `call_sign`),
    INDEX `call_sign` (`call_sign`)
) ENGINE = InnoDB;
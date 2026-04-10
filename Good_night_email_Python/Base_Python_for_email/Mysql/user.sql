CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `city` VARCHAR(50) NOT NULL COMMENT '城市名称，必须与weather表中的city一致',
    `email` VARCHAR(100) NOT NULL COMMENT '收件人邮箱',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


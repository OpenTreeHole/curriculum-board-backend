-- upgrade --
CREATE TABLE IF NOT EXISTS `course` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` LONGTEXT NOT NULL,
    `code` LONGTEXT NOT NULL,
    `code_id` LONGTEXT NOT NULL,
    `credit` DOUBLE NOT NULL,
    `department` LONGTEXT NOT NULL,
    `teachers` LONGTEXT NOT NULL,
    `max_student` INT NOT NULL,
    `week_hour` INT NOT NULL,
    `year` INT NOT NULL,
    `semester` INT NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `coursegroup` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` LONGTEXT NOT NULL,
    `code` LONGTEXT NOT NULL,
    `department` LONGTEXT NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `review` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` LONGTEXT NOT NULL,
    `content` LONGTEXT NOT NULL,
    `history` JSON NOT NULL,
    `reviewer_id` INT NOT NULL,
    `time_created` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `time_updated` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `rank` JSON NOT NULL,
    `upvoters` JSON NOT NULL,
    `downvoters` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `course_review` (
    `course_id` INT NOT NULL,
    `review_id` INT NOT NULL,
    FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`review_id`) REFERENCES `review` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `coursegroup_course` (
    `coursegroup_id` INT NOT NULL,
    `course_id` INT NOT NULL,
    FOREIGN KEY (`coursegroup_id`) REFERENCES `coursegroup` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;

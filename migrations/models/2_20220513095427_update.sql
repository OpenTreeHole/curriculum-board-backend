-- upgrade --
ALTER TABLE `course` ADD `campus_name` LONGTEXT NOT NULL;
ALTER TABLE `coursegroup` ADD `campus_name` LONGTEXT NOT NULL;
-- downgrade --
ALTER TABLE `course` DROP COLUMN `campus_name`;
ALTER TABLE `coursegroup` DROP COLUMN `campus_name`;

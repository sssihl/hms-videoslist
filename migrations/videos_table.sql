CREATE TABLE `dbname`.`rec_save_videos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `patient_id` INT NOT NULL,
  `video_type` VARCHAR(10) NOT NULL,
  `filename` VARCHAR(255) NOT NULL,
  `created` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_of_visit` DATE NOT NULL,

  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `filename_UNIQUE` (`filename` ASC) VISIBLE)
COMMENT = 'for the rec_save mini project (don\'t use dashes \"-\" in names)';

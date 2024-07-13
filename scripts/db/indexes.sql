DROP PROCEDURE IF EXISTS CreateIndexIfNotExists;
DELIMITER //
CREATE PROCEDURE CreateIndexIfNotExists(
    IN table_name VARCHAR(64), 
    IN index_name VARCHAR(64), 
    IN index_definition TEXT
)
BEGIN
    DECLARE index_count INT;
    
    SELECT COUNT(1) INTO index_count
    FROM INFORMATION_SCHEMA.STATISTICS 
    WHERE table_schema = DATABASE() 
      AND table_name = table_name 
      AND index_name = index_name;
    
    IF index_count = 0 THEN
        SET @stmt = CONCAT('CREATE INDEX ', index_name, ' ON ', table_name, ' ', index_definition);
        PREPARE stmt FROM @stmt;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
    END IF;
END //
DELIMITER ;

-- Ensure the procedure is created
CALL CreateIndexIfNotExists('equipment', 'idx_equipment_name', '(eqpName)');
CALL CreateIndexIfNotExists('location', 'idx_location_building', '(buildingName)');
CALL CreateIndexIfNotExists('location', 'idx_location_floor', '(floorNo)');
CALL CreateIndexIfNotExists('location', 'idx_location_area', '(areaName)');
CALL CreateIndexIfNotExists('detectionLogs', 'idx_detectionlogs_time', '(detectionTime)');

CALL CreateIndexIfNotExists('user', 'idx_user_username', '(username)');
CALL CreateIndexIfNotExists('camera', 'idx_camera_ipaddress', '(ipAddress)');
CALL CreateIndexIfNotExists('camera', 'idx_camera_model', '(model)');
CALL CreateIndexIfNotExists('camera', 'idx_camera_installationdate', '(installationDate)');
CALL CreateIndexIfNotExists('camera', 'idx_camera_status', '(cameraStatus)');
CALL CreateIndexIfNotExists('camera', 'idx_camera_locid', '(locId)');
CALL CreateIndexIfNotExists('user', 'idx_user_fullname', '(fullName)');
CALL CreateIndexIfNotExists('user', 'idx_user_birthday', '(birthday)');
CALL CreateIndexIfNotExists('user', 'idx_user_email', '(email)');
CALL CreateIndexIfNotExists('user', 'idx_user_phone', '(phoneNo)');
CALL CreateIndexIfNotExists('user', 'idx_user_pid', '(pId)');
CALL CreateIndexIfNotExists('position', 'idx_position_name', '(positionName)');
CALL CreateIndexIfNotExists('position', 'idx_position_category', '(category)');
CALL CreateIndexIfNotExists('user', 'idx_user_password', '(password)');



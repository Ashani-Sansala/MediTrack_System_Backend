-- For Manage Camera
-- Procedure to get camera data
DELIMITER //
CREATE PROCEDURE GetCameraData(
    IN search_term VARCHAR(1000)
)
BEGIN
    SET @query = CONCAT("
        SELECT 
            c.cameraId, 
            c.ipAddress, 
            c.model, 
            c.installationDate, 
            l.buildingName, 
            l.floorNo, 
            l.areaName, 
            c.cameraStatus
        FROM 
            camera c
        JOIN 
            location l ON c.locId = l.locId
        WHERE 
            c.cameraId LIKE ? OR
            c.ipAddress LIKE ? OR
            c.model LIKE ? OR
            c.installationDate LIKE ? OR
            l.buildingName LIKE ? OR
            l.floorNo LIKE ? OR
            l.areaName LIKE ? OR
            c.cameraStatus LIKE ?
    ");
    SET @search_pattern = CONCAT('%', search_term, '%');
    PREPARE stmt FROM @query;
    EXECUTE stmt USING @search_pattern, @search_pattern, @search_pattern, @search_pattern, 
                      @search_pattern, @search_pattern, @search_pattern, @search_pattern;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;
-- -----------------------

-- Procedure to add a camera
DELIMITER //
CREATE PROCEDURE AddCamera(
    IN p_locId INT,
    IN p_ipAddress CHAR(15),
    IN p_model VARCHAR(100),
    IN p_installationDate DATE,
    IN p_cameraStatus ENUM('Disabled', 'Active', 'Under Maintenance')
)
BEGIN
    INSERT INTO camera (locId, ipAddress, model, installationDate, cameraStatus)
    VALUES (p_locId, p_ipAddress, p_model, p_installationDate, p_cameraStatus);
    SELECT LAST_INSERT_ID() AS cameraId;
END //
DELIMITER ;
-- -----------------------

-- Procedure to update a camera
DELIMITER //
CREATE PROCEDURE UpdateCamera(
    IN p_cameraId INT,
    IN p_ipAddress CHAR(15),
    IN p_cameraStatus ENUM('Disabled', 'Active', 'Under Maintenance')
)
BEGIN
    UPDATE camera 
    SET ipAddress = p_ipAddress, cameraStatus = p_cameraStatus 
    WHERE cameraId = p_cameraId;
END //
DELIMITER ;
-- -----------------------

-- Procedure to get location data
DELIMITER //
CREATE PROCEDURE GetLocationData()
BEGIN
    SELECT locId, areaName, floorNo, buildingName 
    FROM location 
    ORDER BY buildingName, floorNo, areaName ASC;
END //
DELIMITER ;
-- --------------------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------------------

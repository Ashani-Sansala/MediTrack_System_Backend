-- For Dashboard
-- Stored procedure for getting equipment options
DELIMITER //
CREATE PROCEDURE GetEquipmentOptions()
BEGIN
    SELECT DISTINCT eqpName 
    FROM equipment 
    ORDER BY eqpName ASC;
END //
DELIMITER ;
-------------------------

-- Stored procedure for getting building options
DELIMITER //
CREATE PROCEDURE GetBuildingOptions()
BEGIN
    SELECT DISTINCT buildingName 
    FROM location 
    ORDER BY buildingName ASC;
END //
DELIMITER ;
-- -----------------------

-- Stored procedure for getting table data
DELIMITER //
CREATE PROCEDURE GetTableData(
    IN p_startTime TIME,
    IN p_endTime TIME,
    IN p_floorNo VARCHAR(100),
    IN p_eqpName VARCHAR(1000),
    IN p_buildingName VARCHAR(1000),
    IN p_areaName VARCHAR(1000)
)
BEGIN
    SET @sql = 'SELECT dl.logId, e.eqpName, l.buildingName, l.floorNo, l.areaName, dl.direction, 
                dl.detectionTime, dl.frameUrl 
                FROM detectionLogs dl 
                JOIN equipment e ON dl.eqpId = e.eqpId 
                JOIN location l ON dl.locId = l.locId';
    
    SET @where = ' WHERE dl.detectionTimestamp >= NOW() - INTERVAL 24 HOUR';
    
    IF p_startTime IS NOT NULL AND p_endTime IS NOT NULL THEN
        SET @where = CONCAT(@where, ' AND detectionTime BETWEEN "', p_startTime, '" AND "', p_endTime, '"');
    END IF;
    
    IF p_floorNo IS NOT NULL AND p_floorNo != '' THEN
        SET @where = CONCAT(@where, ' AND floorNo IN (', p_floorNo, ')');
    END IF;
    
    IF p_eqpName IS NOT NULL AND p_eqpName != '' THEN
        SET @where = CONCAT(@where, ' AND eqpName REGEXP "', REPLACE(p_eqpName, ',', '|'), '"');
    END IF;
    
    IF p_buildingName IS NOT NULL AND p_buildingName != '' THEN
        SET @where = CONCAT(@where, ' AND buildingName REGEXP "', REPLACE(p_buildingName, ',', '|'), '"');
    END IF;
    
    IF p_areaName IS NOT NULL AND p_areaName != '' THEN
        SET @where = CONCAT(@where, ' AND areaName REGEXP "', REPLACE(p_areaName, ',', '|'), '"');
    END IF;
    
    SET @sql = CONCAT(@sql, @where, ' ORDER BY dl.logId DESC');
    
    PREPARE stmt FROM @sql;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;
-- --------------------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------------------

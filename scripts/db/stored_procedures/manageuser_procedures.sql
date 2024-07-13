-- For Manage Users
-- Procedure to get user data
DROP PROCEDURE IF EXISTS GetUserData;
DELIMITER //
CREATE PROCEDURE GetUserData(
    IN search_term VARCHAR(1000)
)
BEGIN
    SET @query = CONCAT("
        SELECT 
            u.username,
            u.fullName,
            DATE_FORMAT(u.birthday, '%Y-%m-%d') AS birthday,
            u.email,
            u.phoneNo,
            p.positionName,
            p.pId
        FROM 
            user u
        JOIN 
            position p ON u.pId = p.pId
        WHERE 
            u.username LIKE ? OR 
            u.fullName LIKE ? OR 
            u.birthday LIKE ? OR 
            u.email LIKE ? OR 
            u.phoneNo LIKE ? OR 
            p.positionName LIKE ?
    ");
    SET @search_pattern = CONCAT('%', search_term, '%');
    PREPARE stmt FROM @query;
    EXECUTE stmt USING @search_pattern, @search_pattern, @search_pattern, 
                      @search_pattern, @search_pattern, @search_pattern;
    DEALLOCATE PREPARE stmt;
END //
DELIMITER ;
-- -----------------------

-- Procedure to remove user
DROP PROCEDURE IF EXISTS RemoveUser;
DELIMITER //
CREATE PROCEDURE RemoveUser(
    IN p_username CHAR(50)
)
BEGIN
    DELETE FROM user WHERE username = p_username;
END //
DELIMITER ;
-- -----------------------

-- Procedure to add a user
DROP PROCEDURE IF EXISTS AddUser;
DELIMITER //
CREATE PROCEDURE AddUser(
    IN p_username CHAR(50),
    IN p_password CHAR(60),
    IN p_fullName VARCHAR(250),
    IN p_birthday DATE,
    IN p_email VARCHAR(100),
    IN p_phoneNo VARCHAR(15),
    IN p_pId CHAR(5)
)
BEGIN
    INSERT INTO user (username, password, fullName, birthday, email, phoneNo, pId)
    VALUES (p_username, p_password, p_fullName, p_birthday, p_email, p_phoneNo, p_pId);
END //
DELIMITER ;
-- -----------------------

-- Procedure to get positions
DROP PROCEDURE IF EXISTS GetPositions;
DELIMITER //
CREATE PROCEDURE GetPositions()
BEGIN
    SELECT pId, positionName FROM position;
END //
DELIMITER ;
-- -----------------------

-- Procedure to check username
DROP PROCEDURE IF EXISTS CheckUsername;
DELIMITER //
CREATE PROCEDURE CheckUsername(
    IN p_username CHAR(50)
)
BEGIN
    SELECT COUNT(*) AS count FROM user WHERE username = p_username;
END //
DELIMITER ;
-- --------------------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------------------

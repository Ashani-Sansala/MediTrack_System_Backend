-- For Profile
-- Procedure to get user profile
DROP PROCEDURE IF EXISTS GetUserProfile;
DELIMITER //
CREATE PROCEDURE GetUserProfile(
    IN p_username CHAR(50)
)
BEGIN
    SELECT u.username, u.fullName, 
    DATE_FORMAT(u.birthday, '%Y-%m-%d') AS birthday,
    u.email, u.phoneNo, p.positionName, u.avatarUrl
    FROM user u
    JOIN position p ON u.pId = p.pId
    WHERE u.username = p_username;
END //
DELIMITER ;
-- -----------------------

-- Procedure to update user profile
DROP PROCEDURE IF EXISTS UpdateUserProfile;
DELIMITER //
CREATE PROCEDURE UpdateUserProfile(
    IN p_username CHAR(50),
    IN p_fullName VARCHAR(250),
    IN p_birthday DATE,
    IN p_email VARCHAR(100),
    IN p_phoneNo VARCHAR(15),
    IN p_positionName VARCHAR(100),
    IN p_avatarUrl CHAR(255)
)
BEGIN
    DECLARE v_pId CHAR(5);
    
    SELECT pId INTO v_pId FROM position WHERE positionName = p_positionName;
    
    IF v_pId IS NOT NULL THEN
        UPDATE user
        SET fullName = p_fullName, 
            birthday = p_birthday, 
            email = p_email, 
            phoneNo = p_phoneNo, 
            pId = v_pId,
            avatarUrl = COALESCE(p_avatarUrl, avatarUrl)
        WHERE username = p_username;
        
        SELECT fullName, avatarUrl FROM user WHERE username = p_username;
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid position';
    END IF;
END //
DELIMITER ;
-- -----------------------

-- Procedure to reset password
DROP PROCEDURE IF EXISTS ResetPassword;
DELIMITER //
CREATE PROCEDURE ResetPassword(
    IN p_username CHAR(50),
    IN p_new_password CHAR(60)
)
BEGIN
    UPDATE User SET password = p_new_password WHERE username = p_username;
END //
DELIMITER ;
-- --------------------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------------------

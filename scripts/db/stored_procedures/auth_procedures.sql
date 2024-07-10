-- For User Login
-- Stored procedure for authenticate users
DELIMITER //
CREATE PROCEDURE AuthenticateUser(
    IN p_username VARCHAR(1000)
)
BEGIN
    SELECT u.username, u.password, u.fullName, p.category, u.avatarUrl 
    FROM user u 
    JOIN position p ON u.pId=p.pId
    WHERE u.username = p_username;
END //
DELIMITER ;
-- --------------------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------------------

SELECT * FROM equipment;
SELECT * FROM location;
SELECT * FROM camera;
SELECT * FROM detectionLogs;
SELECT * FROM position;
SELECT * FROM user;

SELECT username, password FROM User WHERE username = 'amy_scott';

SELECT u.username, u.password, u.fullName, p.category, u.avatarUrl 
    FROM user u 
    JOIN position p ON u.pId=p.pId
    WHERE u.username = 'jane_smith';

ALTER TABLE position ADD COLUMN category ENUM('HS', 'AD') NOT NULL;
UPDATE position SET category='AD' WHERE pId='PA01';
SELECT 
    dl.logId, 
    e.eqpName, 
    l.buildingName, 
    l.floorNo, 
    l.areaName, 
    dl.detectionTime, 
    dl.videoPath
FROM 
    detectionLogs dl
JOIN 
    equipment e ON dl.eqpId = e.eqpId
JOIN 
    location l ON dl.locId = l.locId;
    
SELECT dl.logId, e.eqpName, l.buildingName, l.floorNo, l.areaName, dl.detectionTime, dl.videoPath
FROM detectionLogs dl
JOIN equipment e ON dl.eqpId = e.eqpId
JOIN location l ON dl.locId = l.locId
ORDER BY dl.logId DESC;

SELECT distinct buildingName FROM location ;


SELECT dl.logId, e.eqpName, l.buildingName, l.floorNo, l.areaName, dl.detectionTime, dl.videoPath FROM detectionLogs dl JOIN equipment e ON dl.eqpId = e.eqpId JOIN location l ON dl.locId = l.locId  WHERE l.buildingName REGEXP 'Main Building' ORDER BY dl.logId DESC;

DROP DATABASE meditracker;

DELETE FROM camera WHERE cameraId = "01";

SELECT 
                u.username,
                u.name,
                u.birthday,
                u.email,
                u.phoneNo,
                p.positionName
            FROM 
                user u
            JOIN 
                position p ON u.pId = p.pId;
            
DROP TABLE user;



SELECT dl.logId, e.eqpName, l.buildingName, l.floorNo, l.areaName, dl.detectionTime, dl.videoPath FROM detectionLogs dl JOIN equipment e ON dl.eqpId = e.eqpId JOIN location l ON dl.locId = l.locId  ORDER BY dl.logId DESC;

INSERT INTO camera (locId, ipAddress, model, installationDate, cameraStatus)
        VALUES (11, '192.168.109.103', 'Model 5001ATY', '2020-04-01', 'Under Maintenance');
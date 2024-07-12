CREATE INDEX idx_equipment_name ON equipment(eqpName);
CREATE INDEX idx_location_building ON location(buildingName);
CREATE INDEX idx_location_floor ON location(floorNo);
CREATE INDEX idx_location_area ON location(areaName);
CREATE INDEX idx_detectionlogs_time ON detectionLogs(detectionTime);

CREATE UNIQUE INDEX idx_user_username ON user(username);

CREATE INDEX idx_camera_ipaddress ON camera(ipAddress);
CREATE INDEX idx_camera_model ON camera(model);
CREATE INDEX idx_camera_installationdate ON camera(installationDate);
CREATE INDEX idx_camera_status ON camera(cameraStatus);

CREATE INDEX idx_camera_locid ON camera(locId);

CREATE INDEX idx_user_fullname ON user(fullName);
CREATE INDEX idx_user_birthday ON user(birthday);
CREATE INDEX idx_user_email ON user(email);
CREATE INDEX idx_user_phone ON user(phoneNo);

CREATE INDEX idx_user_pid ON user(pId);

CREATE INDEX idx_position_name ON position (positionName);
CREATE INDEX idx_position_category ON position (category);

CREATE INDEX idx_user_password ON user(password);

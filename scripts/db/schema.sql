-- create database MediTracker
CREATE DATABASE IF NOT EXISTS MediTracker;

-- select the created database
USE MediTracker;

-- create table equipment for equipment details
CREATE TABLE equipment(
	eqpId CHAR(5) PRIMARY KEY,
	eqpName VARCHAR(40) NOT NULL,
	qty INT NOT NULL
);

-- location table for location details of the hospital
CREATE TABLE location(
	locId INT PRIMARY KEY AUTO_INCREMENT,
	buildingName VARCHAR(100) NOT NULL,
	floorNo INT NOT NULL,
	areaName VARCHAR(100) NOT NULL
);

-- camera table for camera details
CREATE TABLE camera(
	cameraId INT PRIMARY KEY AUTO_INCREMENT,
	locId INT NOT NULL,
	ipAddress CHAR(15) NOT NULL,
	model VARCHAR(100) NOT NULL,
	installationDate DATE NOT NULL,
	cameraStatus ENUM('Disabled', 'Active', 'Under Maintenance') NOT NULL,
	FOREIGN KEY (locId) REFERENCES location(locId)
);

-- detectionLogs table for detection details
CREATE TABLE detectionLogs(
	logId INT PRIMARY KEY AUTO_INCREMENT,
	eqpId CHAR(5) NOT NULL,
	camId INT NOT NULL,
	locId INT NOT NULL,
    direction ENUM('Right', 'Left', 'In', 'Out', 'Static') NOT NULL,
	detectionTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	detectionTime TIME AS (TIME(detectionTimestamp)) STORED,
	detectionDate DATE AS (DATE(detectionTimestamp)) STORED,
	frameUrl CHAR(255) NOT NULL,
	FOREIGN KEY (eqpId) REFERENCES equipment(eqpId),
	FOREIGN KEY (locId) REFERENCES location(locId),
	FOREIGN KEY (camId) REFERENCES camera(cameraId)
);

-- position table for position details of the employees
CREATE TABLE position (
	pId CHAR(5) PRIMARY KEY,
	positionName VARCHAR(100) NOT NULL,
    category ENUM('HS', 'AD') NOT NULL 
);

-- user table for user details
CREATE TABLE user (
    username CHAR(50) PRIMARY KEY,
    password CHAR(60) NOT NULL,
    fullName VARCHAR(250) NOT NULL,
    birthday DATE NOT NULL,
    email VARCHAR(100),
    phoneNo VARCHAR(15) NOT NULL,
    avatarUrl CHAR(255),
    pId CHAR(5) NOT NULL,
    FOREIGN KEY (pId) REFERENCES position (pId)
);

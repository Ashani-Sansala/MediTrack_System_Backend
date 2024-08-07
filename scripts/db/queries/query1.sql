-- Insert data into detectionLogs table
INSERT IGNORE INTO detectionLogs (eqpId, camId, locId, direction, detectionTimestamp, frameUrl) VALUES 
('DE01', 1, 6, 'Right', '2024-07-11 08:30:00', '/frame_logs/ct_scanner_20230501.png'),
('DE02', 2, 6, 'Right', '2024-07-11 09:00:00', '/frame_logs/c_arm_20230502.png'),
('DE03', 3, 11, 'Right', '2024-07-11 10:15:00', '/frame_logs/ecg_machine_20230503.png'),
('DE04', 4, 11, 'Left', '2024-07-11 11:45:00', '/frame_logs/ultrasound_machine_20230504.png'),
('DE05', 5, 11, 'Static', '2024-07-11 12:30:00', '/frame_logs/x_ray_machine_20230505.png'),
('TE01', 6, 18, 'Left', '2024-07-10 14:00:00', '/frame_logs/hemodialysis_machine_20230506.png'),
('TE02', 7, 1, 'Static', '2024-07-10 15:20:00', '/frame_logs/defibrillators_20230507.png'),
('TE03', 8, 4, 'In', '2024-07-10 16:45:00', '/frame_logs/anesthesia_machine_20230508.png'),
('TE04', 9, 3, 'Out', '2024-07-10 17:10:00', '/frame_logs/robotic_surgery_system_20230509.png'),
('TE05', 10, 16, 'Right', '2024-07-10 18:30:00', '/frame_logs/radiotherapy_equipment_20230510.png'),
('TE06', 11, 2, 'Out', '2024-07-10 19:00:00', '/frame_logs/ventilator_20230511.png'),
('LS01', 12, 1, 'Left', '2024-07-10 20:15:00', '/frame_logs/patient_monitor_20230512.png'),
('LS02', 13, 1, 'Left', '2024-07-10 21:45:00', '/frame_logs/infusion_pump_20230513.png'),
('LS03', 14, 2, 'In', '2024-07-10 22:30:00', '/frame_logs/oxygen_concentrator_20230514.png'),
('LS04', 15, 1, 'Right', '2024-07-10 23:00:00', '/frame_logs/suction_machine_20230515.png'),
('MT01', 16, 13, 'Left', '2024-07-10 23:30:00', '/frame_logs/hospital_bed_20230516.png'),
('MT02', 17, 13, 'Out', '2024-07-10 23:40:00', '/frame_logs/wheel_chair_20230517.png'),
('EI01', 18, 13, 'In', '2024-07-10 23:45:00', '/frame_logs/crash_cart_20230518.png'),
('DE01', 19, 6, 'In', '2024-07-10 10:30:00', '/frame_logs/ct_scanner_20230519.png'),
('DE02', 20, 6, 'Right', '2024-07-10 11:45:00', '/frame_logs/c_arm_20230520.png');

-- Insert data into user table
INSERT IGNORE INTO user (username, password, fullName, birthday, email, phoneNo, pId) VALUES 
('john_doe', '$2b$12$SF4ZZh3EVntgLrD5pQYK2uVNWFnXTZiya46RncreVUAoOCsypWAgC', 'John Doe', '1980-01-15', 'john.doe@example.com', '712345226', 'PN01'),
('jane_smith', '$2b$12$SF4ZZh3EVntgLrD5pQYK2uVNWFnXTZiya46RncreVUAoOCsypWAgC', 'Jane Smith', '1985-02-20', 'jane.smith@example.com', '723567890', 'PN01'),
('mike_brown', '$2b$12$SF4ZZh3EVntgLrD5pQYK2uVNWFnXTZiya46RncreVUAoOCsypWAgC', 'Mike Brown', '1975-03-30', 'mike.brown@example.com', '721123575', 'PN01'),
('lisa_jones', '$2b$12$Ka6h4w1KzgshGZLwhQnoSOooZAFnhTG6pGB7xt80HBjK5SO.wYomG', 'Lisa Jones', '1990-04-10', 'lisa.jones@example.com', '112233454', 'PN02'),
('paul_wilson', '$2b$12$Ka6h4w1KzgshGZLwhQnoSOooZAFnhTG6pGB7xt80HBjK5SO.wYomG', 'Paul Wilson', '1988-05-25', 'paul.wilson@example.com', '334455612', 'PN02'),
('emily_davis', '$2b$12$Ka6h4w1KzgshGZLwhQnoSOooZAFnhTG6pGB7xt80HBjK5SO.wYomG', 'Emily Davis', '1992-06-15', 'emily.davis@example.com', '556677823', 'PN02'),
('chris_moore', '$2b$12$Ka6h4w1KzgshGZLwhQnoSOooZAFnhTG6pGB7xt80HBjK5SO.wYomG', 'Chris Moore', '1979-07-20', 'chris.moore@example.com', '778899034', 'PN03'),
('anna_taylor', '$2b$12$Ka6h4w1KzgshGZLwhQnoSOooZAFnhTG6pGB7xt80HBjK5SO.wYomG', 'Anna Taylor', '1983-08-25', 'anna.taylor@example.com', '729900112', 'PN03'),
('kevin_anderson', '$2b$12$LrgaUirGNSeaHmMlS559rOVPWwGlW3nDBbMbMt3PGAUpJ8kAxlXU.', 'Kevin Anderson', '1995-09-10', 'kevin.anderson@example.com', '772233445', 'PN03'),
('laura_thomas', '$2b$12$LrgaUirGNSeaHmMlS559rOVPWwGlW3nDBbMbMt3PGAUpJ8kAxlXU.', 'Laura Thomas', '1987-10-05', 'laura.thomas@example.com', '114433556', 'PN04'),
('david_jackson', '$2b$12$LrgaUirGNSeaHmMlS559rOVPWwGlW3nDBbMbMt3PGAUpJ8kAxlXU.', 'David Jackson', '1978-11-15', 'david.jackson@example.com', '116675578', 'PN04'),
('susan_white', '$2b$12$LrgaUirGNSeaHmMlS559rOVPWwGlW3nDBbMbMt3PGAUpJ8kAxlXU.', 'Susan White', '1982-12-20', 'susan.white@example.com', '775558899', 'PN04'),
('robert_harris', '$2b$12$eZ7pNy6IMLhgZoJrHQrvb.997CE7GcKnVtlkYnHrNRPGP0z6HquZi', 'Robert Harris', '1991-01-30', 'robert.harris@example.com', '755561010', 'PD01'),
('karen_martin', '$2b$12$eZ7pNy6IMLhgZoJrHQrvb.997CE7GcKnVtlkYnHrNRPGP0z6HquZi', 'Karen Martin', '1986-02-25', 'karen.martin@example.com', '782312122', 'PD01'),
('steve_clark', '$2b$12$eZ7pNy6IMLhgZoJrHQrvb.997CE7GcKnVtlkYnHrNRPGP0z6HquZi', 'Steve Clark', '1993-03-15', 'steve.clark@example.com', '764664332', 'PD01'),
('nancy_lewis', '$2b$12$eZ7pNy6IMLhgZoJrHQrvb.997CE7GcKnVtlkYnHrNRPGP0z6HquZi', 'Nancy Lewis', '1984-04-10', 'nancy.lewis@example.com', '786714140', 'PD04'),
('mark_robinson', '$2b$12$gOijNVndylnRwbNzGSCez.1ynm42ccL1kNhGiy/s4YcwLfPHfZUPm', 'Mark Robinson', '1977-05-20', 'mark.robinson@example.com', '772915158', 'PD04'),
('jessica_king', '$2b$12$gOijNVndylnRwbNzGSCez.1ynm42ccL1kNhGiy/s4YcwLfPHfZUPm', 'Jessica King', '1996-06-25', 'jessica.king@example.com', '722215616', 'PD06'),
('daniel_wright', '$2b$12$gOijNVndylnRwbNzGSCez.1ynm42ccL1kNhGiy/s4YcwLfPHfZUPm', 'Daniel Wright', '1989-07-30', 'daniel.wright@example.com', '782231717', 'PR02'),
('amy_scott', '$2b$12$gOijNVndylnRwbNzGSCez.1ynm42ccL1kNhGiy/s4YcwLfPHfZUPm', 'Amy Scott', '1994-08-15', 'amy.scott@example.com', '779848180', 'PH02'),
('robert_ford', '$2b$12$gOijNVndylnRwbNzGSCez.1ynm42ccL1kNhGiy/s4YcwLfPHfZUPm', 'Robert Ford', '1996-07-25', 'robert.ford@example.com', '752116199', 'PH04'),
('dolores_abernarthy', '$2b$12$gOijNVndylnRwbNzGSCez.1ynm42ccL1kNhGiy/s4YcwLfPHfZUPm', 'Dolores Abernarthy', '1996-06-25', 'dolores.abernarthy@example.com', '912216200', 'PA01'),
('peter_parker', '$2b$12$gOijNVndylnRwbNzGSCez.1ynm42ccL1kNhGiy/s4YcwLfPHfZUPm', 'Peter Parker', '1996-06-25', 'peter.parker@example.com', '715551630', 'PA01');
CREATE DATABASE IF NOT EXISTS aiaco;

USE aiaco;

DROP TABLE IF EXISTS leaked_credentials;

CREATE TABLE leaked_credentials (

    id INT PRIMARY KEY AUTO_INCREMENT,

    email VARCHAR(150) NOT NULL,

    password_md5 VARCHAR(32),

    password_plain VARCHAR(100)

);

INSERT INTO leaked_credentials
(email,password_md5,password_plain)
VALUES

('alejandro.rodriguez@aiaco.local',
'4d186321c1a7f0f354b297e8914ab240',
NULL),

('laura.garcia@aiaco.local',
'7c6a180b36896a0a8c02787eeafb0e4c',
'Aiaco2024!'),

('miguel.lopez@aiaco.local',
'5f4dcc3b5aa765d61d8327deb882cf99',
'password'),

('fernanda.silva@aiaco.local',
'21232f297a57a5a743894a0e4a801fc3',
NULL),

('juan.torres@aiaco.local',
'e10adc3949ba59abbe56e057f20f883e',
'123456');
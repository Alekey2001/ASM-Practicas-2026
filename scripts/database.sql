CREATE TABLE leaked_credentials (
    id INTEGER PRIMARY KEY,
    email VARCHAR(150),
    password_md5 VARCHAR(32),
    password_plain VARCHAR(100)
);

INSERT INTO leaked_credentials VALUES
(1,'alejandro.rodriguez@aiaco.local','4d186321c1a7f0f354b297e8914ab240',NULL);

INSERT INTO leaked_credentials VALUES
(2,'laura.garcia@aiaco.local','7c6a180b36896a0a8c02787eeafb0e4c','Aiaco2024!');

INSERT INTO leaked_credentials VALUES
(3,'miguel.lopez@aiaco.local','5f4dcc3b5aa765d61d8327deb882cf99','password');

INSERT INTO leaked_credentials VALUES
(4,'fernanda.silva@aiaco.local','21232f297a57a5a743894a0e4a801fc3',NULL);

INSERT INTO leaked_credentials VALUES
(5,'juan.torres@aiaco.local','e10adc3949ba59abbe56e057f20f883e','123456');

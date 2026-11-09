-- MySQL 8.0. Solo laboratorio sintético aiaco.local.
-- Copia saneada reproducible; NO migra contraseñas ni modifica el original.
USE aiaco;

SELECT 'antes_original' AS etapa, COUNT(*) AS registros,
       SUM(password_plain IS NOT NULL) AS texto_plano,
       SUM(password_md5 IS NOT NULL) AS hashes_md5
FROM leaked_credentials;

-- Destino distinto de la copia histórica; LIKE conserva la clave primaria.
CREATE TABLE IF NOT EXISTS leaked_credentials_sanitized LIKE leaked_credentials;

START TRANSACTION;
-- Repetir sobre la misma fuente produce el mismo contenido del destino.
-- No copiar texto plano ni siquiera de forma transitoria.
INSERT INTO leaked_credentials_sanitized (id, email, password_md5, password_plain)
SELECT id, email, password_md5, NULL FROM leaked_credentials
ON DUPLICATE KEY UPDATE
    email = VALUES(email),
    password_md5 = VALUES(password_md5),
    password_plain = NULL;
UPDATE leaked_credentials_sanitized SET password_plain = NULL
WHERE password_plain IS NOT NULL;
COMMIT;

SELECT 'despues_original' AS etapa, COUNT(*) AS registros,
       SUM(password_plain IS NOT NULL) AS texto_plano,
       SUM(password_md5 IS NOT NULL) AS hashes_md5
FROM leaked_credentials;

SELECT 'despues_copia' AS etapa, COUNT(*) AS registros,
       SUM(password_plain IS NOT NULL) AS texto_plano,
       SUM(password_md5 IS NOT NULL) AS hashes_md5
FROM leaked_credentials_sanitized;

-- Cero diferencias esperadas para el fixture; no es una migración de autenticación.
SELECT COUNT(*) AS faltantes_o_diferentes
FROM leaked_credentials AS original
LEFT JOIN leaked_credentials_sanitized AS copia ON original.id = copia.id
WHERE copia.id IS NULL OR NOT (original.email <=> copia.email)
   OR NOT (original.password_md5 <=> copia.password_md5)
   OR copia.password_plain IS NOT NULL;

SELECT COUNT(*) AS filas_adicionales_en_copia
FROM leaked_credentials_sanitized AS copia
LEFT JOIN leaked_credentials AS original ON original.id = copia.id
WHERE original.id IS NULL;

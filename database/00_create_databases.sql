-- =====================================================================
-- ainolez : create the local databases and the application user
-- Run ONCE as root on your PC (XAMPP):
--   mysql -u root < database/00_create_databases.sql
-- On cPanel, create the database and user in "MySQL Databases" instead.
-- =====================================================================

CREATE DATABASE IF NOT EXISTS ainolez
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Used only by the automated tests (wiped on every test run).
CREATE DATABASE IF NOT EXISTS ainolez_test
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Local development user. Never reuse this password on a real server.
CREATE USER IF NOT EXISTS 'ainolez_app'@'localhost' IDENTIFIED BY 'ainolez_local_dev';

GRANT ALL PRIVILEGES ON ainolez.*      TO 'ainolez_app'@'localhost';
GRANT ALL PRIVILEGES ON ainolez_test.* TO 'ainolez_app'@'localhost';
FLUSH PRIVILEGES;

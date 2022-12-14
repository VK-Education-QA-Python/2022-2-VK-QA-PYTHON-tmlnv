USE vkeducation;
CREATE TABLE test_users(
    id int NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    surname varchar(255) NOT NULL,
    middle_name varchar(255) DEFAULT NULL,
    username varchar(16) DEFAULT NULL,
    password varchar(255) NOT NULL,
    email varchar(64) NOT NULL,
    access smallint DEFAULT NULL,
    active smallint DEFAULT NULL,
    start_active_time datetime DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY email (email),
    UNIQUE KEY ix_test_users_username (username)
);
GRANT ALL ON vkeducation.* TO "test_qa"@"%";
INSERT INTO test_users (name, surname, middle_name, username, password, email, access, active)
values ('admin', 'admin', NULL, 'admin!', 'admin', 'admin@admin.com', 1, 0);
INSERT INTO test_users (name, surname, middle_name, username, password, email, access, active)
values ('Arima', 'Kisho', NULL, 'Arima_Kisho', '1234', 'aaaa@aaaa.com', 1, 0);
INSERT INTO test_users (name, surname, middle_name, username, password, email, access, active)
values ('blocked', 'blocked', NULL, 'blocked', 'blocked', 'blockeda@blocked.com', 0, 0);
INSERT INTO test_users (name, surname, middle_name, username, password, email, access, active)
values ('set_access0', 'set_access0', NULL, 'set_access0', 'set_access0', 'set_access0@set_access0.com', 1, 0);
INSERT INTO test_users (name, surname, middle_name, username, password, email, access, active)
values ('Jack', 'Sparrow', NULL, 'captain', 'captain', 'captain0@captain.com', 1, 0);

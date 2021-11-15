/*CREATE DATABASE test;

CREATE USER 'user'@'%' IDENTIFIED WITH mysql_native_password BY 'pass123!';
GRANT ALL ON test.* TO 'user'@'%';

FLUSH PRIVILEGES;*/
USE test;
CREATE TABLE users(
	id int not null auto_increment,
	firstname char(64) NOT NULL,
	lastname char(64) NOT NULL,
	phone char(64) NOT NULL,
    email char(64) NOT NULL UNIQUE,
    password_  text NOT NULL,
	primary key(id)
);
CREATE TABLE tasks(
	id int not null auto_increment,
    user_id int not null,
    task text,
    primary key (id),
    foreign key(user_id) references users(id)
)
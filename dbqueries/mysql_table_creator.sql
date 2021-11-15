DROP DATABASE IF EXISTS test;

CREATE DATABASE test;
use test;

CREATE TABLE users(
	id int not null auto_increment,
	firstname char(64) NOT NULL,
	lastname char(64) NOT NULL,
	phone char(64) NOT NULL,
    email char(64) NOT NULL UNIQUE,
    pass  char(255) NOT NULL,
	primary key(id)
);
CREATE TABLE tasks(
	id int not null auto_increment,
    user_id int not null,
    task text,
    primary key (id),
    foreign key(user_id) references users(id)
)

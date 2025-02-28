drop database if exists examen_dwes;
create database examen_dwes;
use examen_dwes;

create table users(
	id int unsigned auto_increment primary key,
    username varchar(50),
    password varchar(255)
);
create table productos(
	id int unsigned auto_increment primary key,
    nombre varchar(50),
    precio int unsigned
);
create table carrito(
	id int unsigned primary key,
    nombre varchar(50),
    precio int unsigned,
    user_id int unsigned,
    foreign key(id) references productos(id),
    foreign key(user_id) references users(id) 
);
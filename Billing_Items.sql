create Database Food;
use food;
create table Food_1
(
Id int auto_increment primary key,
Item varchar(255),
Price int
);
insert into Food_1(Item,Price) values('Momo',40),('Samosa',15),('Biriyani',60),('Chowmin',70);




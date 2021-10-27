create table category(
    codename varchar(255) primary key,
    name varchar(255),
    aliases text
);

create table tasks(
    id integer primary key autoincrement,
    user_id integer,
    category varchar(255),
    date varchar(11),
    text text
);

insert into category (codename, name, aliases)
values
    ("unimportant", "Неважные", "@неважно, @несрочное, @несрочные"),
    ("important", "Важные", "@важные, @срочные, @неотложные, @срочно, @неотложно, @важно"),
    ("other", "прочее", "");
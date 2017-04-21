drop user if exists 'www'@'%';
create user 'www'@'%' identified by '$3cureUS';
drop database if exists cs4501;
create database cs4501 character set utf8;
grant all on cs4501.* to 'www'@'%';

DROP TABLE IF EXISTS Users CASCADE;

CREATE TABLE IF NOT EXISTS Users(
	pk serial not null PRIMARY KEY,
	user_name varchar(50) UNIQUE,
  full_name varchar(50),
	password varchar(120),
  has_stall boolean default false
);

CREATE INDEX IF NOT EXISTS users_index
ON Users (pk, user_name);

DELETE FROM Users;

INSERT INTO Users(user_name, full_name, password)
VALUES ('user', 'User', 'pass');
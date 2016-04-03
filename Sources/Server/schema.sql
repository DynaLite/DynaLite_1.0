CREATE DATABASE IF NOT EXISTS Dynalite;
USE Dynalite;

-- Uncomment below to drop tables first
-- ------------------------------------
-- DROP TABLE IF EXISTS User;
-- DROP TABLE IF EXISTS Location;
-- DROP TABLE IF EXISTS UserModel;
-- ------------------------------------

-- CREATE TABLE IF NOT EXISTS User (
-- 	id INTEGER PRIMARY KEY,

-- );

-- CREATE TABLE IF NOT EXISTS Location (
-- 	id	
-- 	timestamp
-- 	loc
-- );

CREATE TABLE IF NOT EXISTS UserModel (
	time_stamp	TIMESTAMP,
	u1_loc		INTEGER,
	u2_loc		INTEGER,
	u1_emotion	INTEGER,	
	u2_emotion	INTEGER
);
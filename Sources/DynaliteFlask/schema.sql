-- DynaLite 

-- Emotion values
	-- 1 = neutral
	-- 2 = calm
	-- 3 = happy
	-- 4 = sad
	-- 5 = angry

drop table if exists user_model;
create table user_model (
	time_stamp	TIMESTAMP,
	u1_loc		INTEGER,
	u2_loc		INTEGER,
	u1_emotion	INTEGER,	
	u2_emotion	INTEGER
);
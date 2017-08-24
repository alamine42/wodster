CREATE TABLE IF NOT EXISTS invictus_workouts 
(
	workout_date text NOT NULL,
	workout_day text NOT NULL,
	workout_url text PRIMARY KEY,
	workout_alt_url text,
	workout_level text,
	workout_desc text,
	workout_html text,
	workout_final text,
	workout_exists integer
)
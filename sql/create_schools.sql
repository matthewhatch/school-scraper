CREATE TABLE schools(
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  address1 VARCHAR,
  city VARCHAR,
  state VARCHAR,
  zip VARCHAR,
  county VARCHAR,
  phone VARCHAR,
  soundex VARCHAR,
  enrollment INTEGER,
  start_grade VARCHAR,
  end_grade VARCHAR
);
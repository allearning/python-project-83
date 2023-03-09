--noqa: disable=L010
DROP TABLE IF EXISTS urls CASCADE;
CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name varchar(255) UNIQUE,
    created_at date
);

INSERT INTO urls (name, created_at) VALUES
('Sansa', '2018-11-03'),
('Sansa2', '2018-10-23'),
('Daenerys', '2018-12-23'),
('Arya', '2018-11-18'),
('Robb', '2018-11-10'),
('Brienne', '2018-11-28'),
('Tirion', '2018-11-23');


DROP TABLE IF EXISTS url_checks;
CREATE TABLE url_checks (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id bigint REFERENCES urls (id),
    status_code integer,
    h1 varchar(255),
    title varchar(255),
    description varchar(255),
    created_at date
);

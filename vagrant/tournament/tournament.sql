-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
  id  SERIAL PRIMARY KEY,
  name VARCHAR(40) NOT NULL
);

CREATE TABLE matches (
  id  SERIAL PRIMARY KEY,
  winner INTEGER REFERENCES players,
  loser  INTEGER REFERENCES players
);

-- View for counting wins per player
CREATE VIEW wincounts AS
  SELECT players.id, players.name, count(matches.winner)
  AS wins
  FROM players
  LEFT JOIN matches
  ON players.id = matches.winner
  GROUP BY players.id;

-- View for counting total matches per player
CREATE VIEW totalmatches AS
  SELECT players.id, count(matches.id) AS total_matches
  FROM players
  LEFT JOIN matches
  ON players.id = matches.winner OR players.id = matches.loser
  GROUP BY players.id;


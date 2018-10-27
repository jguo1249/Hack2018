DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  phone TEXT UNIQUE NOT NULL,
  world BOOLEAN NOT NULL,
  local BOOLEAN NOT NULL,
  sports BOOLEAN NOT NULL,
  science BOOLEAN NOT NULL,
  food BOOLEAN NOT NULL,
  entertainment BOOLEAN NOT NULL,
  politics BOOLEAN NOT NULL,
  technology BOOLEAN NOT NULL,
  context TEXT,
  firstDelivery TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  frequency TEXT NOT NULL DEFAULT "24h"
);

CREATE TABLE article (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  topic TEXT NOT NULL,
  published TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  headline TEXT NOT NULL,
  body TEXT NOT NULL,
  link TEXT NOT NULL,
  author TEXT NOT NULL,
  imglink TEXT
);
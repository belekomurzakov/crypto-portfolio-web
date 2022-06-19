DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS activityHistory;
DROP TABLE IF EXISTS wallet;

CREATE TABLE user
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT        NOT NULL,
    lastName  TEXT        NOT NULL,
    username  TEXT UNIQUE NOT NULL,
    password  TEXT        NOT NULL,
    isActive  INTEGER     NOT NULL
);

CREATE TABLE activityHistory
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    cryptoId    TEXT    NOT NULL,
    userId      INTEGER NOT NULL,
    amount      DOUBLE  NOT NULL,
    isPurchased INTEGER NOT NULL,
    created     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES user (id)
);

CREATE TABLE wallet
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    cryptoId TEXT    NOT NULL,
    userId   INTEGER NOT NULL,
    amount   DOUBLE  NOT NULL,
    FOREIGN KEY (userId) REFERENCES user (id)
);
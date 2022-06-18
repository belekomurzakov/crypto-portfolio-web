DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS cryptocurrency;
DROP TABLE IF EXISTS wallet;

CREATE TABLE User
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT        NOT NULL,
    lastName  TEXT        NOT NULL,
    username  TEXT UNIQUE NOT NULL,
    password  TEXT        NOT NULL,
    isActive  INTEGER     NOT NULL
);

CREATE TABLE ActivityHistory
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    cryptoId    TEXT    NOT NULL,
    userId      INTEGER NOT NULL,
    amount      DOUBLE  NOT NULL,
    isPurchased INTEGER NOT NULL,
    FOREIGN KEY (userId) REFERENCES user (id),
    UNIQUE (userId)
);

CREATE TABLE Wallet
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    cryptoId TEXT    NOT NULL,
    userId   INTEGER NOT NULL,
    amount   DOUBLE  NOT NULL,
    FOREIGN KEY (userId) REFERENCES user (id),
    UNIQUE (userId)
);
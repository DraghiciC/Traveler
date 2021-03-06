DROP TABLE IF EXISTS messages;

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lang TEXT NOT NULL,
    country TEXT NOT NULL,
    person TEXT NOT NULL,
    message TEXT NOT NULL
);
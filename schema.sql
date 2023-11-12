CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    text TEXT,
    created_at TIMESTAMP
);

CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    message_id INTEGER REFERENCES messages,
    answer TEXT,
    sent_at TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);

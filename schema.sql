CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    text TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);


CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    message_id INTEGER REFERENCES messages,
    answer TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);
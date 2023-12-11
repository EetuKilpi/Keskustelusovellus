CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL CHECK (LENGTH(username) >= 3) UNIQUE,
    password TEXT NOT NULL CHECK (LENGTH(password) >= 3),
    admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    text TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    edited BOOLEAN DEFAULT FALSE,
    private BOOLEAN DEFAULT FALSE
);


CREATE TABLE answers (
    id SERIAL PRIMARY KEY,
    message_id INTEGER REFERENCES messages ON DELETE CASCADE,
    answer TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP,
    edited BOOLEAN DEFAULT FALSE
);

CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    message_id INTEGER UNIQUE REFERENCES messages ON DELETE CASCADE,
    user_id INTEGER REFERENCES users
);

CREATE TABLE polls (
    id SERIAL PRIMARY KEY,
    topic TEXT,
    user_id INTEGER REFERENCES users,
    created_at TIMESTAMP
);

CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    poll_id INTEGER REFERENCES polls ON DELETE CASCADE,
    choice TEXT
);

CREATE TABLE poll_answers (
    id SERIAL PRIMARY KEY,
    choice_id INTEGER REFERENCES choices ON DELETE CASCADE,
    sent_at TIMESTAMP
);

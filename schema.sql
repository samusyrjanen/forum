create table users (
    id serial primary key,
    username text unique,
    password text
);

create table threads (
    id serial primary key,
    content text,
    user_id integer references users,
    sent_at timestamp
);

create table comments (
    id serial primary key,
    content text,
    user_id integer references users,
    sent_at timestamp
);

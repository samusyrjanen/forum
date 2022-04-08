create table users (
    id serial primary key,
    username text unique,
    password text
);

create table threads (
    id serial primary key,
    topic text,
    content text,
    user_id integer references users,
    sent_at timestamp
);

create table comments (
    id serial primary key,
    content text,
    user_id integer references users,
    sent_at timestamp,
    thread_id integer references threads
);

create table likes (
    id serial primary key,
    user_id integer references users,
    thread_id integer references threads,
    comment_id integer references comments
);

--update to server
create table messages (
    id serial primary key,
    sender_id integer references users,
    receiver_id integer references users,
    content text,
    sent_at timestamp
);

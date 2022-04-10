
create table users (
    id serial primary key,
    username text unique,
    password text,
    admin boolean
);

create table threads (
    id serial primary key,
    topic text,
    content text,
    user_id integer references users on delete cascade,
    sent_at timestamp
);

create table comments (
    id serial primary key,
    content text,
    user_id integer references users on delete cascade,
    sent_at timestamp,
    thread_id integer references threads on delete cascade
);

create table likes (
    id serial primary key,
    user_id integer references users on delete cascade,
    thread_id integer references threads on delete cascade,
    comment_id integer references comments on delete cascade
);

create table messages (
    id serial primary key,
    sender_id integer references users on delete cascade,
    receiver_id integer references users on delete cascade,
    content text,
    sent_at timestamp
);

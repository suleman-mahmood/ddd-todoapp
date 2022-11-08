drop table if exists users cascade;
drop table if exists tasks cascade;
drop table if exists histories cascade;
drop type if exists task_action cascade;

create type task_action as enum ('add', 'edit', 'delete');

create table users (
    user_id uuid,
    first_name varchar (100),
    last_name varchar (100),

    primary key (user_id)
);

create table tasks (
    task_id uuid,
    task_description varchar (200),
    is_completed boolean,
    task_order int,
    is_deleted boolean,

    user_id uuid,

    primary key (task_id),
    foreign key (user_id)
        references users (user_id)
);

create table histories (
    history_id uuid,
    action_taken task_action,
    
    task_id uuid,

    primary key (history_id),
    foreign key (task_id)
        references tasks (task_id)
);
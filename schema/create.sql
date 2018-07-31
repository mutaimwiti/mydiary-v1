create table if not exists users (
  id         serial    not null primary key,
  name       varchar   not null,
  email      varchar   not null,
  password   varchar   not null,
  created_at timestamp not null default now(),
  updated_at timestamp          default current_timestamp
);

create table if not exists entries (
  id         serial    not null primary key,
  title      varchar   not null,
  body       text      not null,
  created_by integer   not null references users (id),
  created_at timestamp not null default now(),
  updated_at timestamp          default current_timestamp
);

-- create a procedure that can update the updated_at column
create or replace function update_updated_at_column()
  returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$
language 'plpgsql';

-- create a trigger that updates the updated_at column when updates occur
create trigger update_entries_created_at
  before update
  on entries
  for each row
execute procedure update_updated_at_column();

-- create a trigger that updates the updated_at column when updates occur
create trigger update_users_created_at
  before update
  on users
  for each row
execute procedure update_updated_at_column();

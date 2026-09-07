alter table public."user"
    add constraint user_first_name_required check (nullif(trim(first_name), '') is not null) not valid,
    add constraint user_last_name_required check (nullif(trim(last_name), '') is not null) not valid;

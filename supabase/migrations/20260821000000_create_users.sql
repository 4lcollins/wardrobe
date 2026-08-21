create table if not exists public."user" (
    id uuid primary key default gen_random_uuid(),
    created_at timestamptz not null default now(),
    email text not null unique,
    first_name text,
    last_name text,
    is_email_enabled boolean not null default true
);

create index if not exists user_is_email_enabled_email_idx
    on public."user" (is_email_enabled, email);

alter table public."user" enable row level security;

drop policy if exists "Users are readable by anon" on public."user";

create policy "Users are readable by anon"
    on public."user"
    for select
    to anon
    using (is_email_enabled = true);

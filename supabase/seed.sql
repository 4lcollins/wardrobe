insert into public."user" (email, first_name, last_name, is_email_enabled)
values
    ('a@b.com', 'Alex', 'Rivera', true),
    ('jordan@example.com', 'Jordan', 'Lee', false),
    ('sam@example.com', 'Sam', 'Patel', false)
on conflict (email) do nothing;

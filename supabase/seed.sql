insert into public."user" (email, first_name, last_name, is_email_enabled)
values
    ('alex@example.com', 'Alex', 'Rivera', true),
    ('jordan@example.com', 'Jordan', 'Lee', true),
    ('sam@example.com', 'Sam', 'Patel', false)
on conflict (email) do nothing;

insert into public."user" (email, first_name, last_name)
values
    ('alex@example.com', 'Alex', 'Rivera'),
    ('jordan@example.com', 'Jordan', 'Lee'),
    ('sam@example.com', 'Sam', 'Patel')
on conflict (email) do nothing;

create table public.calendar (
    user_id uuid not null references public."user"(id) on delete cascade,
    weekday smallint not null check (weekday between 0 and 6),
    position smallint not null check (position between 0 and 9),
    name text not null check (length(trim(name)) > 0),
    start_time time not null,
    end_time time not null,
    primary key (user_id, weekday, position),
    check (start_time <> end_time)
);

alter table public.calendar enable row level security;

create or replace function public.save_calendar_periods(p_user_id uuid, p_periods jsonb)
returns void
language plpgsql
security invoker
as $$
begin
    delete from public.calendar where user_id = p_user_id;

    insert into public.calendar (user_id, weekday, position, name, start_time, end_time)
    select p_user_id, item.weekday, item.position, item.name,
           item.start_time::time, item.end_time::time
    from jsonb_to_recordset(p_periods) as item(
        weekday smallint,
        position smallint,
        name text,
        start_time text,
        end_time text
    );
end;
$$;

revoke all on function public.save_calendar_periods(uuid, jsonb) from public, anon, authenticated;
grant execute on function public.save_calendar_periods(uuid, jsonb) to service_role;

from typing import Any

from src.db.client import get_supabase


def get_week_template(user_id: str) -> dict[str, list[dict[str, Any]]]:
    response = (
        get_supabase()
        .table("calendar")
        .select("weekday,position,name,start_time,end_time")
        .eq("user_id", user_id)
        .order("weekday")
        .order("position")
        .execute()
    )
    rows = response.data or []
    if not rows:
        return {}
    template = {str(day): [] for day in range(7)}
    for row in rows:
        start_hour = _time_to_hour(row["start_time"])
        end_hour = _time_to_hour(row["end_time"])
        template[str(row["weekday"])].append(
            {"name": row["name"], "start_hour": start_hour, "end_hour": end_hour}
        )
    return template


def _time_to_hour(value: str) -> float:
    hour, minute, *_ = value.split(":")
    return int(hour) + int(minute) / 60


def save_week_template(user_id: str, week_template: dict[str, Any]) -> None:
    rows = [
        {
            "weekday": int(day),
            "position": position,
            "name": period["name"],
            "start_time": _hour_to_time(period["start_hour"]),
            "end_time": _hour_to_time(period["end_hour"]),
        }
        for day, periods in week_template.items()
        for position, period in enumerate(periods)
    ]
    get_supabase().rpc(
        "save_calendar_periods",
        {"p_user_id": user_id, "p_periods": rows},
    ).execute()


def _hour_to_time(value: float) -> str:
    minutes = round(float(value) * 60)
    if minutes == 1440:
        return "24:00:00"
    return f"{minutes // 60:02d}:{minutes % 60:02d}:00"

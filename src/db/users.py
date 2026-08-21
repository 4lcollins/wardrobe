from typing import Any

from src.db.client import get_supabase


def list_active_users() -> list[dict[str, Any]]:
    response = (
        get_supabase()
        .table("user")
        .select("id,created_at,email,first_name,last_name,is_email_enabled")
        .eq("is_email_enabled", True)
        .order("email")
        .execute()
    )
    return response.data or []


def list_user_emails() -> list[str]:
    users = list_active_users()
    return [user["email"] for user in users if user.get("email")]

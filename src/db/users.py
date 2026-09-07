from typing import Any

from src.db.client import get_supabase

USER_COLUMNS = "id,created_at,email,first_name,last_name,is_email_enabled"


class DuplicateUserError(ValueError):
    pass


def normalize_email(email: str) -> str:
    return email.strip().lower()


def _required_text(value: str, field_name: str) -> str:
    normalized_value = value.strip()

    if not normalized_value:
        raise ValueError(f"{field_name} is required.")

    return normalized_value


def list_email_enabled_users() -> list[dict[str, Any]]:
    response = (
        get_supabase()
        .table("user")
        .select(USER_COLUMNS)
        .eq("is_email_enabled", True)
        .order("email")
        .execute()
    )
    return response.data or []


def get_user_by_email(email: str) -> dict[str, Any] | None:
    normalized_email = normalize_email(email)

    if not normalized_email:
        return None

    response = (
        get_supabase()
        .table("user")
        .select(USER_COLUMNS)
        .eq("email", normalized_email)
        .limit(1)
        .execute()
    )

    data = response.data or []
    return data[0] if data else None


def create_user_account(
    *,
    email: str,
    first_name: str = "",
    last_name: str = "",
    is_email_enabled: bool = True,
) -> dict[str, Any]:
    normalized_email = normalize_email(email)

    if not normalized_email:
        raise ValueError("Email is required.")

    normalized_first_name = _required_text(first_name, "First name")
    normalized_last_name = _required_text(last_name, "Last name")

    if get_user_by_email(normalized_email):
        raise DuplicateUserError("A Wardrobe account already exists for this email.")

    profile = {
        "email": normalized_email,
        "first_name": normalized_first_name,
        "last_name": normalized_last_name,
        "is_email_enabled": is_email_enabled,
    }

    try:
        response = get_supabase().table("user").insert(profile).execute()
    except Exception as exc:
        message = str(exc).lower()
        if "duplicate" in message or "unique" in message or "23505" in message:
            raise DuplicateUserError("A Wardrobe account already exists for this email.") from exc
        raise

    data = response.data or []
    return data[0] if data else profile


def update_user_profile(
    *,
    user_id: str,
    first_name: str,
    last_name: str,
    is_email_enabled: bool,
) -> dict[str, Any]:
    normalized_first_name = _required_text(first_name, "First name")
    normalized_last_name = _required_text(last_name, "Last name")

    profile = {
        "first_name": normalized_first_name,
        "last_name": normalized_last_name,
        "is_email_enabled": is_email_enabled,
    }

    response = (
        get_supabase()
        .table("user")
        .update(profile)
        .eq("id", user_id)
        .execute()
    )

    data = response.data or []
    return data[0] if data else {**profile, "id": user_id}

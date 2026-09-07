from types import SimpleNamespace

import pytest

from src.db import users


class FakeQuery:
    def __init__(self, data):
        self.data = data
        self.filters = []
        self.limit_count = None
        self.inserted = None

    def select(self, columns):
        self.columns = columns
        return self

    def insert(self, row):
        self.inserted = row
        self.data = [row]
        return self

    def eq(self, column, value):
        self.filters.append((column, value))
        return self

    def limit(self, count):
        self.limit_count = count
        return self

    def order(self, column):
        self.order_column = column
        return self

    def execute(self):
        return SimpleNamespace(data=self.data)


class FakeSupabase:
    def __init__(self, data):
        self.data = data
        self.query = None
        self.queries = []

    def table(self, table_name):
        self.table_name = table_name
        self.query = FakeQuery(self.data)
        self.queries.append(self.query)
        return self.query


def test_list_email_enabled_users_filters_email_enabled(monkeypatch):
    fake_client = FakeSupabase([])
    monkeypatch.setattr(users, "get_supabase", lambda: fake_client)

    users.list_email_enabled_users()

    assert fake_client.table_name == "user"
    assert fake_client.query.filters == [("is_email_enabled", True)]


def test_get_user_by_email(monkeypatch):
    fake_client = FakeSupabase(
        [
            {
                "id": "44ef5b7e-e665-4d3c-b956-6ccecbdf7e5c",
                "created_at": "2026-08-21T00:00:00+00:00",
                "email": "one@example.com",
                "first_name": "One",
                "last_name": "User",
                "is_email_enabled": True,
            }
        ]
    )
    monkeypatch.setattr(users, "get_supabase", lambda: fake_client)

    found_user = users.get_user_by_email(" One@Example.com ")

    assert found_user["email"] == "one@example.com"
    assert fake_client.query.filters == [
        ("email", "one@example.com"),
    ]
    assert fake_client.query.limit_count == 1


def test_get_user_by_email_skips_blank_email(monkeypatch):
    fake_client = FakeSupabase([])
    monkeypatch.setattr(users, "get_supabase", lambda: fake_client)

    assert users.get_user_by_email(" ") is None
    assert fake_client.query is None


def test_create_user_account_inserts_profile(monkeypatch):
    fake_client = FakeSupabase([])
    monkeypatch.setattr(users, "get_supabase", lambda: fake_client)

    created_user = users.create_user_account(
        email=" New@Example.com ",
        first_name=" New ",
        last_name=" User ",
        is_email_enabled=False,
    )

    assert fake_client.queries[-1].inserted == {
        "email": "new@example.com",
        "first_name": "New",
        "last_name": "User",
        "is_email_enabled": False,
    }
    assert created_user["email"] == "new@example.com"


def test_create_user_account_rejects_existing_email(monkeypatch):
    fake_client = FakeSupabase(
        [
            {
                "id": "44ef5b7e-e665-4d3c-b956-6ccecbdf7e5c",
                "created_at": "2026-08-21T00:00:00+00:00",
                "email": "one@example.com",
                "first_name": "One",
                "last_name": "User",
                "is_email_enabled": True,
            }
        ]
    )
    monkeypatch.setattr(users, "get_supabase", lambda: fake_client)

    try:
        users.create_user_account(
            email="one@example.com",
            first_name="One",
            last_name="User",
        )
    except users.DuplicateUserError:
        pass
    else:
        raise AssertionError("Expected duplicate user error")


def test_create_user_account_requires_names(monkeypatch):
    fake_client = FakeSupabase([])
    monkeypatch.setattr(users, "get_supabase", lambda: fake_client)

    with pytest.raises(ValueError, match="First name is required"):
        users.create_user_account(
            email="new@example.com",
            first_name=" ",
            last_name="User",
        )

    with pytest.raises(ValueError, match="Last name is required"):
        users.create_user_account(
            email="new@example.com",
            first_name="New",
            last_name=" ",
        )

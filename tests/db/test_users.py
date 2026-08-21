from types import SimpleNamespace

from src.db import users


class FakeQuery:
    def __init__(self, data):
        self.data = data
        self.filters = []
        self.limit_count = None

    def select(self, columns):
        self.columns = columns
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

    def table(self, table_name):
        self.table_name = table_name
        self.query = FakeQuery(self.data)
        return self.query


def test_list_user_emails(monkeypatch):
    fake_client = FakeSupabase(
        [
            {
                "id": "44ef5b7e-e665-4d3c-b956-6ccecbdf7e5c",
                "created_at": "2026-08-21T00:00:00+00:00",
                "email": "one@example.com",
                "first_name": "One",
                "last_name": "User",
                "is_email_enabled": True,
            },
            {
                "id": "6070af8a-0aa7-4e06-bfc6-9292d6e72d76",
                "created_at": "2026-08-21T00:00:00+00:00",
                "email": "two@example.com",
                "first_name": "Two",
                "last_name": "User",
                "is_email_enabled": True,
            },
        ]
    )
    monkeypatch.setattr(users, "get_supabase", lambda: fake_client)

    assert users.list_user_emails() == ["one@example.com", "two@example.com"]


def test_list_user_emails_skips_missing_email(monkeypatch):
    fake_client = FakeSupabase(
        [
            {
                "id": "44ef5b7e-e665-4d3c-b956-6ccecbdf7e5c",
                "created_at": "2026-08-21T00:00:00+00:00",
                "email": "",
                "first_name": "No",
                "last_name": "Email",
                "is_email_enabled": True,
            }
        ]
    )
    monkeypatch.setattr(users, "get_supabase", lambda: fake_client)

    assert users.list_user_emails() == []


def test_list_active_users_filters_email_enabled(monkeypatch):
    fake_client = FakeSupabase([])
    monkeypatch.setattr(users, "get_supabase", lambda: fake_client)

    users.list_active_users()

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

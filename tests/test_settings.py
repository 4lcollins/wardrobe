from src.settings import parse_email_list


class TestParseEmailList:
    def test_splits_commas_and_newlines(self):
        assert parse_email_list("one@example.com, two@example.com\nthree@example.com") == [
            "one@example.com",
            "two@example.com",
            "three@example.com",
        ]

    def test_ignores_empty_entries(self):
        assert parse_email_list("one@example.com,,\n  ") == ["one@example.com"]

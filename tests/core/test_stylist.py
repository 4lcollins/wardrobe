from datetime import date

from src.core.stylist import Stylist


class TestRecommendClothing:
    def test_recommends_clothing_for_each_day_period(self, monkeypatch):
        class Period:
            def __init__(self, name):
                self.name = name
                self.date = date(2026, 6, 7)
                self.display_date = "Today"

        class FakeThermometer:
            def get_period_temperatures(self, calendar=None):
                return [
                    {"period": Period("Morning"), "temperature": 45},
                    {"period": Period("Afternoon"), "temperature": 70},
                ]

        monkeypatch.setattr(
            "src.core.stylist.Prompt.generate",
            lambda self: self.response_schema(insight="Layer up, then simplify."),
        )
        monkeypatch.setattr("src.core.stylist.random.choice", lambda options: options[0])

        recommendation = Stylist(FakeThermometer()).recommend_clothing()

        assert [period["name"] for period in recommendation["time_periods"]] == [
            "Morning",
            "Afternoon",
        ]
        assert [
            period["display_date"]
            for period in recommendation["time_periods"]
        ] == ["Today", "Today"]
        assert recommendation["insight"] == "Layer up, then simplify."

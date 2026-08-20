from src.core.stylist import Stylist


class TestRecommendClothing:
    def test_recommends_clothing_for_each_day_period(self, monkeypatch):
        class FakeThermometer:
            def get_period_temperatures(self, calendar=None):
                return [
                    {"period": type("Period", (), {"name": "Morning"})(), "temperature": 45},
                    {"period": type("Period", (), {"name": "Afternoon"})(), "temperature": 70},
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
        assert recommendation["temperatures"] == [45, 70]
        assert recommendation["insight"] == "Layer up, then simplify."

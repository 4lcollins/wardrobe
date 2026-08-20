from src.core.stylist import Stylist
from src.core.thermometer import Thermometer


class TestRecommendClothing:
    def test_recommends_clothing_for_each_day_period(self, monkeypatch):
        class FakeThermometer(Thermometer):
            def __init__(city = "", state = ""):
                pass
            def get_period_temperatures(self, calendar=None):
                return [
                    {"period": type("Period", (), {"name": "Morning"})(), "temperature": 45},
                    {"period": type("Period", (), {"name": "Afternoon"})(), "temperature": 70},
                ]

        monkeypatch.setattr(
            "src.core.stylist.Prompt.generate",
            lambda user_input, model_class: model_class(insight="Layer up, then simplify."),
        )
        monkeypatch.setattr("src.core.stylist.random.choice", lambda options: options[0])

        recommendation = Stylist(FakeThermometer()).recommend_clothing()

        assert [period["name"] for period in recommendation["time_periods"]] == [
            "Morning",
            "Afternoon",
        ]
        assert recommendation["temperatures"] == [45, 70]
        assert recommendation["insight"] == "Layer up, then simplify."

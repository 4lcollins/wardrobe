import argparse
import importlib


def run_automation(automation_name: str) -> None:
    module = importlib.import_module(f"src.automations.{automation_name}")
    module.run()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a Wardrobe automation.")
    parser.add_argument(
        "automation",
        help="Automation module name from src/automations, without .py.",
    )
    args = parser.parse_args()

    run_automation(args.automation)


if __name__ == "__main__":
    main()

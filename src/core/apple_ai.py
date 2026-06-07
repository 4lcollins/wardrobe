import json
import re
import time
import sys
import uuid
import webbrowser
import urllib.parse
from pathlib import Path
from typing import Type, TypeVar
import subprocess


T = TypeVar("T")

class AppleAI:
    def __init__(self):
        pass

    def generate(self, user_input: str, model_class: Type[T]) -> T:
        # Extract the JSON Schema
        schema = "{\n" + ", ".join(

            f"\t{name}: {field.type.__name__}"

            for name, field in model_class.__dataclass_fields__.items()

        ) + "\n}"

        # The Pedantic System Wrapper
        pedantic_prompt = (
            "You are a JSON generator.\n"
            "Return ONLY valid JSON.\n"
            "No explanations. No prose. No markdown.\n\n"

            "You must output EXACTLY one JSON object in this format:\n"
            f"{json.dumps(schema, indent=2)}\n\n"

            "REQUEST:\n"
            f"{user_input}\n\n"
            "OUTPUT:"
        )

        if sys.platform == "ios":
            text_response = self._run_ios(pedantic_prompt)
        else:
            text_response = self._run_subprocess(pedantic_prompt)

        return self._parse_response(text_response, model_class)

    def _run_subprocess(self, prompt: str) -> str:
        result = subprocess.run(
            ["shortcuts", "run", "Apple AI - Generate"],
            input=prompt,
            text=True,
            capture_output=True,
            check=True,
        )

        return result.stdout.strip()

    def _run_ios(self, prompt: str, timeout: int = 15) -> str:
        filename = f"{uuid.uuid4().hex}.txt"
        output_path = Path(filename)

        payload = {
            "filename": filename,
            "prompt": prompt,
        }

        url = (
            "shortcuts://run-shortcut?"
            "name=" + urllib.parse.quote("Apple AI - Generate File")
            + "&input=text&text=" + urllib.parse.quote(json.dumps(payload))
        )
        webbrowser.open(url)

        start = time.time()
        while not output_path.exists():
            if time.time() - start > timeout:
                raise TimeoutError(
                    f"Timed out waiting for Apple AI output: {output_path}"
                )
            time.sleep(1)

        text_response = output_path.read_text()
        output_path.unlink(missing_ok=True)

        return text_response

    def _parse_response(self, text_response: str, model_class: Type[T]) -> T:
        # Snipe JSON from response
        json_match = re.search(
            r"\{.*\}",
            text_response,
            re.DOTALL,
        )

        if json_match:
            try:
                data = json.loads(json_match.group(0))
                return model_class(**data)

            except Exception as e:
                raise ValueError(
                    f"Failed to parse or validate AI response: "
                    f"{e}\n{text_response}"
                )

        raise ValueError(
            "No JSON block found in AI response:\n"
            f"{text_response}"
        )

apple_ai = AppleAI()
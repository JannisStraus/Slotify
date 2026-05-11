import json
import os
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

FIXTURES = Path(__file__).parent / "fixtures"


def _load_json(bot: str, name: str) -> Any:
    return json.loads((FIXTURES / bot / name).read_text())


def _load_expected(bot: str) -> str:
    return (FIXTURES / bot / "expected.md").read_text()


def _mock_response(payload: Any) -> MagicMock:
    response = MagicMock()
    response.json.return_value = payload
    response.raise_for_status.return_value = None
    return response


class TestWellnest(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["WELLNEST_SLUG"] = "test-location"

    def tearDown(self) -> None:
        os.environ.pop("WELLNEST_SLUG", None)

    @patch("slotify.wellnest.api.requests.get")
    def test_markdown(self, mock_get: MagicMock) -> None:
        from slotify.wellnest.main import main  # noqa: PLC0415

        mock_get.return_value = _mock_response(_load_json("wellnest", "day_slots.json"))
        result = main("11.05.2026")

        self.assertEqual(result, _load_expected("wellnest"))


class TestMyWellness(unittest.TestCase):
    @patch("slotify.mywellness.api.requests.get")
    def test_markdown(self, mock_get: MagicMock) -> None:
        from slotify.mywellness.main import main  # noqa: PLC0415

        mock_get.return_value = _mock_response(
            _load_json("mywellness", "start_times.json")
        )
        result = main("11.05.2026")

        self.assertEqual(result, _load_expected("mywellness"))


class TestJustiz(unittest.TestCase):
    @patch("slotify.justiz.api.requests.get")
    def test_markdown(self, mock_get: MagicMock) -> None:
        from slotify.justiz.main import main  # noqa: PLC0415

        mock_get.return_value = _mock_response(
            _load_json("justiz", "available_times.json")
        )
        result = main("19.05.2026")

        self.assertEqual(result, _load_expected("justiz"))


class TestMorante(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["MORANTE_SALON_SLUG"] = "testsalon"
        os.environ["MORANTE_STAFF_ID"] = "test-staff"
        os.environ["MORANTE_SERVICE_ID"] = "test-service"

    def tearDown(self) -> None:
        for key in ("MORANTE_SALON_SLUG", "MORANTE_STAFF_ID", "MORANTE_SERVICE_ID"):
            os.environ.pop(key, None)

    @patch("slotify.morante.api.api_post")
    def test_markdown(self, mock_post: MagicMock) -> None:
        from slotify.morante.main import main  # noqa: PLC0415

        mock_post.return_value = _load_json("morante", "availability_requests.json")
        result = main("11.05.2026,12.05.2026")

        self.assertEqual(result, _load_expected("morante"))

    @patch("slotify.morante.api.api_post")
    def test_filters_to_requested_dates(self, mock_post: MagicMock) -> None:
        from slotify.morante.main import main  # noqa: PLC0415

        mock_post.return_value = _load_json("morante", "availability_requests.json")
        result = main("11.05.2026")

        self.assertIsNotNone(result)
        assert result is not None
        self.assertIn("11\\.05\\.2026", result)
        self.assertNotIn("12\\.05\\.2026", result)


if __name__ == "__main__":
    unittest.main()

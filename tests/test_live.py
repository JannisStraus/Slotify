import os
import unittest
from datetime import date, timedelta

from dotenv import load_dotenv

load_dotenv()

_START = date.today() + timedelta(days=7)
_END = _START + timedelta(days=7)
DATE_RANGE = f"{_START:%d.%m.%Y}-{_END:%d.%m.%Y}"


def _have(*keys: str) -> bool:
    return all(os.getenv(k) for k in keys)


class TestLiveBots(unittest.TestCase):
    def _assert_valid(self, result: str | None) -> None:
        self.assertTrue(
            result is None or (isinstance(result, str) and result),
            f"expected None or non-empty str, got: {result!r}",
        )

    @unittest.skipUnless(
        _have("MORANTE_SALON_SLUG", "MORANTE_STAFF_ID", "MORANTE_SERVICE_ID"),
        "MORANTE_SALON_SLUG / STAFF_ID / SERVICE_ID not set",
    )
    def test_morante(self) -> None:
        from slotify.morante.main import main  # noqa: PLC0415

        self._assert_valid(main(DATE_RANGE))

    @unittest.skipUnless(_have("WELLNEST_SLUG"), "WELLNEST_SLUG not set")
    def test_wellnest(self) -> None:
        from slotify.wellnest.main import main  # noqa: PLC0415

        self._assert_valid(main(DATE_RANGE))

    def test_mywellness(self) -> None:
        from slotify.mywellness.main import main  # noqa: PLC0415

        self._assert_valid(main(DATE_RANGE))

    def test_justiz(self) -> None:
        from slotify.justiz.main import main  # noqa: PLC0415

        self._assert_valid(main(DATE_RANGE))


if __name__ == "__main__":
    unittest.main()

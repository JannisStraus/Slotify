import unittest

from slotify.utils import DateTime, Time, parse_date, parse_dates


class TestParseDate(unittest.TestCase):
    def test_dot_format(self) -> None:
        dt = parse_date("11.05.2026")
        self.assertEqual((dt.year, dt.month, dt.day), (2026, 5, 11))

    def test_iso_format(self) -> None:
        dt = parse_date("2026-05-11")
        self.assertEqual((dt.year, dt.month, dt.day), (2026, 5, 11))

    def test_returns_DateTime(self) -> None:
        self.assertIsInstance(parse_date("11.05.2026"), DateTime)

    def test_invalid_format_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_date("foo")

    def test_invalid_day_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_date("2026-13-40")


class TestParseDates(unittest.TestCase):
    def test_single_iso(self) -> None:
        result = parse_dates("2026-05-11")
        self.assertEqual([str(d) for d in result], ["11.05.2026"])

    def test_single_dot(self) -> None:
        result = parse_dates("11.05.2026")
        self.assertEqual([str(d) for d in result], ["11.05.2026"])

    def test_comma_list_dot(self) -> None:
        result = parse_dates("11.05.2026,13.05.2026")
        self.assertEqual([str(d) for d in result], ["11.05.2026", "13.05.2026"])

    def test_comma_list_iso(self) -> None:
        result = parse_dates("2026-05-11,2026-05-13")
        self.assertEqual([str(d) for d in result], ["11.05.2026", "13.05.2026"])

    def test_range_dot(self) -> None:
        result = parse_dates("11.05.2026-15.05.2026")
        self.assertEqual(
            [str(d) for d in result],
            ["11.05.2026", "12.05.2026", "13.05.2026", "14.05.2026", "15.05.2026"],
        )

    def test_range_iso(self) -> None:
        result = parse_dates("2026-05-11-2026-05-15")
        self.assertEqual(
            [str(d) for d in result],
            ["11.05.2026", "12.05.2026", "13.05.2026", "14.05.2026", "15.05.2026"],
        )

    def test_mixed_combination(self) -> None:
        result = parse_dates("11.05.2026,2026-05-13-2026-05-15")
        self.assertEqual(
            [str(d) for d in result],
            ["11.05.2026", "13.05.2026", "14.05.2026", "15.05.2026"],
        )

    def test_whitespace_tolerated(self) -> None:
        result = parse_dates(" 11.05.2026 , 13.05.2026 ")
        self.assertEqual([str(d) for d in result], ["11.05.2026", "13.05.2026"])

    def test_dedup_preserves_order(self) -> None:
        result = parse_dates("13.05.2026,11.05.2026,13.05.2026")
        self.assertEqual([str(d) for d in result], ["13.05.2026", "11.05.2026"])

    def test_range_dedup_with_overlap(self) -> None:
        result = parse_dates("11.05.2026,11.05.2026-13.05.2026")
        self.assertEqual(
            [str(d) for d in result], ["11.05.2026", "12.05.2026", "13.05.2026"]
        )

    def test_reversed_range_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_dates("2026-05-15-2026-05-11")

    def test_empty_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_dates("")

    def test_only_commas_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_dates(",,,")

    def test_garbage_input_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_dates("foo")

    def test_trailing_dash_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_dates("2026-05-11-")

    def test_returns_DateTime_instances(self) -> None:
        for d in parse_dates("11.05.2026-13.05.2026"):
            self.assertIsInstance(d, DateTime)


class TestDateTime(unittest.TestCase):
    def test_str(self) -> None:
        self.assertEqual(str(DateTime(2026, 5, 11)), "11.05.2026")

    def test_fmt_en(self) -> None:
        self.assertEqual(DateTime(2026, 5, 11).fmt_en(), "2026-05-11")

    def test_zero_padding(self) -> None:
        self.assertEqual(str(DateTime(2026, 1, 3)), "03.01.2026")
        self.assertEqual(DateTime(2026, 1, 3).fmt_en(), "2026-01-03")


class TestTime(unittest.TestCase):
    def test_str(self) -> None:
        self.assertEqual(str(Time(14, 30)), "14:30")

    def test_zero_padding(self) -> None:
        self.assertEqual(str(Time(8, 5)), "08:05")


if __name__ == "__main__":
    unittest.main()

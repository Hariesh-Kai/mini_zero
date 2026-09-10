import unittest
from datetime import datetime
from zoneinfo import ZoneInfo

from assistant import ZeroAssistant


class ZeroAssistantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assistant = ZeroAssistant(lambda: datetime(2026, 9, 10, 14, 5, 6))

    def test_time_command_and_natural_language_alias(self) -> None:
        expected = "The current time in India is 02:05:06 PM (14:05:06), IST (UTC+05:30)."
        self.assertEqual(self.assistant.handle("what time is it"), expected)

    def test_time_uses_india_timezone_with_default_clock(self) -> None:
        india_time = datetime(2026, 9, 10, 19, 35, 6, tzinfo=ZoneInfo("Asia/Kolkata"))
        assistant = ZeroAssistant(lambda: india_time)
        self.assertEqual(
            assistant.handle("time"),
            "The current time in India is 07:35:06 PM (19:35:06), IST (UTC+05:30).",
        )

    def test_time_details_include_local_utc_and_timestamp(self) -> None:
        response = self.assistant.handle("time details")
        self.assertIn("Thursday, 2026-09-10, 02:05:06 PM IST", response)
        self.assertIn("24-hour: 14:05:06", response)
        self.assertIn("UTC: 2026-09-10 08:35:06 UTC", response)
        self.assertIn("Unix timestamp: 1789029306", response)

    def test_calendar_details_include_date_position_and_leap_year(self) -> None:
        response = self.assistant.handle("calendar")
        self.assertIn("Thursday, September 10, 2026", response)
        self.assertIn("ISO week 37", response)
        self.assertIn("day 253 of 365", response)
        self.assertIn("Quarter 3", response)
        self.assertIn("It is not a leap year", response)

    def test_practical_time_aliases(self) -> None:
        expected = "The current time in India is 02:05:06 PM (14:05:06), IST (UTC+05:30)."
        self.assertEqual(self.assistant.handle("now"), expected)
        self.assertEqual(self.assistant.handle("what is the current time"), expected)

    def test_natural_time_questions(self) -> None:
        expected = "The current time in India is 02:05:06 PM (14:05:06), IST (UTC+05:30)."
        questions = (
            "what's the time",
            "tell me the time",
            "can you tell me the time",
            "do you know the time",
            "what time is it now",
            "what is the time right now",
            "what's the current time",
            "how late is it",
            "time please",
            "what's the time in india",
            "what is indian time",
        )
        for question in questions:
            with self.subTest(question=question):
                self.assertEqual(self.assistant.handle(question), expected)

    def test_natural_date_questions(self) -> None:
        expected = "Today's date is 2026-09-10."
        questions = (
            "what's the date",
            "what date is it",
            "tell me the date",
            "tell me today's date",
            "is today",
            "date today",
            "date please",
        )
        for question in questions:
            with self.subTest(question=question):
                self.assertEqual(self.assistant.handle(question), expected)

    def test_natural_calendar_timezone_utc_and_timestamp_questions(self) -> None:
        self.assertIn("ISO week 37", self.assistant.handle("which day is it"))
        self.assertIn("Asia/Kolkata", self.assistant.handle("what time zone am I in"))
        self.assertIn("UTC", self.assistant.handle("what time is it in utc"))
        self.assertIn("Unix timestamp", self.assistant.handle("what is the timestamp"))

    def test_timezone_utc_and_timestamp_commands(self) -> None:
        self.assertIn("India Standard Time (IST), Asia/Kolkata, UTC+05:30", self.assistant.handle("timezone"))
        self.assertEqual(self.assistant.handle("utc"), "The current UTC time is 2026-09-10 08:35:06 UTC.")
        self.assertEqual(self.assistant.handle("timestamp"), "The current Unix timestamp is 1789029306.")

    def test_date_command_and_natural_language_alias(self) -> None:
        self.assertEqual(self.assistant.handle("what is today date"), "Today's date is 2026-09-10.")
        self.assertEqual(self.assistant.handle("what is today's date?"), "Today's date is 2026-09-10.")

    def test_date_details_include_calendar_facts(self) -> None:
        response = self.assistant.handle("date details")
        self.assertIn("Thursday, September 10, 2026", response)
        self.assertIn("ISO date: 2026-09-10", response)
        self.assertIn("ISO week: 37", response)
        self.assertIn("Day 253 of 365; 112 days remain", response)
        self.assertIn("Quarter 3", response)
        self.assertIn("Month: September", response)
        self.assertIn("This is not a leap year", response)

    def test_relative_date_questions(self) -> None:
        self.assertEqual(self.assistant.handle("what date is tomorrow"), "Tomorrow is Friday, 2026-09-11.")
        self.assertEqual(self.assistant.handle("what day was yesterday"), "Yesterday was Wednesday, 2026-09-09.")

    def test_calendar_date_wording_aliases(self) -> None:
        self.assertIn("Month: September", self.assistant.handle("what month is it"))
        self.assertIn("ISO week: 37", self.assistant.handle("what is the week number"))
        self.assertIn("Day 253 of 365", self.assistant.handle("what day of the year is it"))

    def test_greeting_command_and_alias(self) -> None:
        expected = "Hello. I am Zero, your assistant."
        self.assertEqual(self.assistant.handle("greet"), expected)
        self.assertEqual(self.assistant.handle("hello"), expected)

    def test_combined_greeting_date_and_time_request(self) -> None:
        response = self.assistant.handle("hey what is today's date and time?")
        self.assertEqual(
            response,
            "Hello. I am Zero, your assistant. Today's date is 2026-09-10. "
            "The current time in India is 02:05:06 PM (14:05:06), IST (UTC+05:30).",
        )

    def test_combined_greeting_and_date_request(self) -> None:
        self.assertEqual(
            self.assistant.handle("hi what's today's date"),
            "Hello. I am Zero, your assistant. Today's date is 2026-09-10.",
        )

    def test_combined_greeting_and_time_request(self) -> None:
        self.assertEqual(
            self.assistant.handle("hi what time is it"),
            "Hello. I am Zero, your assistant. The current time in India is "
            "02:05:06 PM (14:05:06), IST (UTC+05:30).",
        )

    def test_combined_date_and_time_without_greeting(self) -> None:
        self.assertEqual(
            self.assistant.handle("what is today's date and time"),
            "Today's date is 2026-09-10. The current time in India is "
            "02:05:06 PM (14:05:06), IST (UTC+05:30).",
        )

    def test_unknown_command_explains_unbuilt_skills(self) -> None:
        response = self.assistant.handle("open my email")
        self.assertIn("skills have yet to be built", response)
        self.assertIn("time, time details, calendar, timezone, utc, timestamp", response)

    def test_empty_and_non_text_input_are_handled(self) -> None:
        self.assertIn("Please enter a command", self.assistant.handle("   "))
        self.assertIn("could not understand", self.assistant.handle(None))

    def test_help_lists_all_commands(self) -> None:
        response = self.assistant.handle("help")
        for command in (
            "time", "time details", "calendar", "timezone", "utc", "timestamp",
            "date", "greet", "help", "skills", "status", "quit",
        ):
            self.assertIn(command, response)


if __name__ == "__main__":
    unittest.main()
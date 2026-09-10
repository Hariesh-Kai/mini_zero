"""Zero v0.1: a small, dependency-free command line assistant."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Callable
from zoneinfo import ZoneInfo


CommandHandler = Callable[[], str]
INDIA_TIMEZONE = ZoneInfo("Asia/Kolkata")


@dataclass(frozen=True)
class Command:
    name: str
    description: str
    handler: CommandHandler


class ZeroAssistant:
    """Route user input to the small set of skills available in v0.1."""

    def __init__(self, clock: Callable[[], datetime] | None = None) -> None:
        self._clock = clock or (lambda: datetime.now(INDIA_TIMEZONE))
        self._commands = {
            command.name: command
            for command in (
                Command("time", "Show the current time", self.current_time),
                Command("time details", "Show complete India time details", self.time_details),
                Command("calendar", "Show calendar details for today", self.calendar),
                Command("timezone", "Show the current timezone", self.timezone),
                Command("utc", "Show the current UTC time", self.current_utc),
                Command("timestamp", "Show the current Unix timestamp", self.timestamp),
                Command("date", "Show today's date", self.current_date),
                Command("date details", "Show complete calendar date details", self.date_details),
                Command("today", "Show today's date", self.current_date),
                Command("tomorrow", "Show tomorrow's date", self.tomorrow),
                Command("yesterday", "Show yesterday's date", self.yesterday),
                Command("greet", "Greet the user", self.greet),
                Command("help", "Show available commands", self.help),
                Command("skills", "Show the current skill status", self.skills),
                Command("status", "Show Zero's status", self.status),
                Command("quit", "Exit Zero", self.quit),
            )
        }

    def handle(self, request: str) -> str:
        """Return a response for a request without allowing input errors to escape."""
        try:
            normalized = " ".join(
                request.strip().lower().strip(".,!?;").split()
            )
        except (AttributeError, TypeError):
            return "I could not understand that request. Please enter text."

        if not normalized:
            return "Please enter a command. Type 'help' to see available commands."

        compound_response = self._handle_compound_request(normalized)
        if compound_response is not None:
            return compound_response

        command_name = self._resolve_command(normalized)
        if command_name is None:
            return self.unknown_command()

        try:
            return self._commands[command_name].handler()
        except Exception:
            return "I could not complete that command right now. Please try again."

    def _handle_compound_request(self, request: str) -> str | None:
        has_date_request = self._contains_any(request, ("date", "today"))
        has_time_request = self._contains_any(
            request, ("time", "clock", "hour", "what's the time", "now")
        ) and "timezone" not in request and "time zone" not in request
        first_word = request.split(maxsplit=1)[0].strip(".,!?;")
        has_greeting_request = first_word in {"hey", "hello", "hi"}
        requested_parts = has_date_request + has_time_request + has_greeting_request
        if requested_parts < 2:
            return None

        responses = []
        if has_greeting_request:
            responses.append(self.greet())
        if has_date_request:
            responses.append(self.current_date())
        if has_time_request:
            responses.append(self.current_time())
        return " ".join(responses)

    @staticmethod
    def _contains_any(request: str, phrases: tuple[str, ...]) -> bool:
        return any(phrase in request for phrase in phrases)

    def _resolve_command(self, request: str) -> str | None:
        aliases = {
            "hello": "greet",
            "hi": "greet",
            "hey": "greet",
            "what time is it": "time",
            "what is the time": "time",
            "current time": "time",
            "time details": "time details",
            "detailed time": "time details",
            "full time": "time details",
            "give me time details": "time details",
            "show me time details": "time details",
            "give me the full time": "time details",
            "now": "time",
            "what is the current time": "time",
            "what's the time": "time",
            "what time": "time",
            "tell me the time": "time",
            "tell me time": "time",
            "can you tell me the time": "time",
            "do you know the time": "time",
            "time now": "time",
            "current time please": "time",
            "check the time": "time",
            "check time": "time",
            "read the clock": "time",
            "what time is it now": "time",
            "what is the time right now": "time",
            "what's the current time": "time",
            "how late is it": "time",
            "time please": "time",
            "what's the time in india": "time",
            "what is the time in india": "time",
            "what is indian time": "time",
            "what is the current date": "date",
            "what's the date": "date",
            "what date is it": "date",
            "what date": "date",
            "tell me the date": "date",
            "tell me today's date": "date",
            "tell me todays date": "date",
            "is today": "date",
            "date today": "date",
            "what's today's date": "date",
            "what is today's date today": "date",
            "date please": "date",
            "today": "today",
            "what is today": "today",
            "what day is today": "today",
            "tomorrow": "tomorrow",
            "what is tomorrow's date": "tomorrow",
            "what is tomorrows date": "tomorrow",
            "what date is tomorrow": "tomorrow",
            "what day is tomorrow": "tomorrow",
            "yesterday": "yesterday",
            "what was yesterday's date": "yesterday",
            "what was yesterdays date": "yesterday",
            "what date was yesterday": "yesterday",
            "what day was yesterday": "yesterday",
            "date details": "date details",
            "detailed date": "date details",
            "full date": "date details",
            "tell me everything about today's date": "date details",
            "calendar": "calendar",
            "calendar details": "calendar",
            "what day is it": "calendar",
            "what day of the week is it": "calendar",
            "what day is today": "calendar",
            "which day is it": "calendar",
            "which day of the week is it": "calendar",
            "what is today's day": "calendar",
            "show me the calendar": "calendar",
            "what is today's calendar": "calendar",
            "what month is it": "date details",
            "which month is it": "date details",
            "what week is it": "date details",
            "what is the week number": "date details",
            "what day of the year is it": "date details",
            "how many days are left in the year": "date details",
            "what timezone am i in": "timezone",
            "what is my timezone": "timezone",
            "what is the timezone": "timezone",
            "what time zone am i in": "timezone",
            "what timezone is this": "timezone",
            "which timezone am i in": "timezone",
            "tell me my timezone": "timezone",
            "is this ist": "timezone",
            "india time zone": "timezone",
            "utc time": "utc",
            "what is utc time": "utc",
            "what time is it in utc": "utc",
            "tell me the utc time": "utc",
            "current utc": "utc",
            "what is utc": "utc",
            "unix timestamp": "timestamp",
            "epoch time": "timestamp",
            "what is the unix timestamp": "timestamp",
            "what is the timestamp": "timestamp",
            "tell me the unix time": "timestamp",
            "what is today's date": "date",
            "what is todays date": "date",
            "what is today date": "date",
            "today's date": "date",
            "todays date": "date",
            "exit": "quit",
            "bye": "quit",
        }
        return aliases.get(request, request if request in self._commands else None)

    def _india_now(self) -> datetime:
        current = self._clock()
        if current.tzinfo is None:
            return current.replace(tzinfo=INDIA_TIMEZONE)
        return current.astimezone(INDIA_TIMEZONE)

    def current_time(self) -> str:
        current = self._india_now()
        return (
            f"The current time in India is {current.strftime('%I:%M:%S %p')} "
            f"({current.strftime('%H:%M:%S')}), IST (UTC{current.strftime('%z')[:3]}:"
            f"{current.strftime('%z')[3:]})."
        )

    def current_date(self) -> str:
        return f"Today's date is {self._india_now().strftime('%Y-%m-%d')}."

    def date_details(self) -> str:
        current = self._india_now()
        day_of_year = int(current.strftime("%j"))
        year_days = 366 if current.year % 4 == 0 and (current.year % 100 != 0 or current.year % 400 == 0) else 365
        days_remaining = year_days - day_of_year
        return (
            f"Today is {current.strftime('%A, %B %-d, %Y')}. "
            f"ISO date: {current.strftime('%Y-%m-%d')}. "
            f"ISO week: {current.isocalendar().week}. "
            f"Day {day_of_year} of {year_days}; {days_remaining} days remain in the year. "
            f"Quarter {(current.month - 1) // 3 + 1}. "
            f"Month: {current.strftime('%B')}. "
            f"{'This is' if year_days == 366 else 'This is not'} a leap year."
        )

    def tomorrow(self) -> str:
        tomorrow = self._india_now().date() + timedelta(days=1)
        return f"Tomorrow is {tomorrow.strftime('%A, %Y-%m-%d')}."

    def yesterday(self) -> str:
        yesterday = self._india_now().date() - timedelta(days=1)
        return f"Yesterday was {yesterday.strftime('%A, %Y-%m-%d')}."

    def time_details(self) -> str:
        current = self._india_now()
        utc_time = current.astimezone(timezone.utc)
        return (
            f"India time: {current.strftime('%A, %Y-%m-%d, %I:%M:%S %p')} IST. "
            f"24-hour: {current.strftime('%H:%M:%S')}. "
            f"UTC: {utc_time.strftime('%Y-%m-%d %H:%M:%S')} UTC. "
            f"Unix timestamp: {int(current.timestamp())}."
        )

    def calendar(self) -> str:
        current = self._india_now()
        year_days = 366 if current.year % 4 == 0 and (current.year % 100 != 0 or current.year % 400 == 0) else 365
        return (
            f"Today is {current.strftime('%A, %B %-d, %Y')}. "
            f"ISO week {current.isocalendar().week}, day {current.strftime('%j').lstrip('0')} of {year_days}. "
            f"Quarter {(current.month - 1) // 3 + 1}. "
            f"{'It is' if year_days == 366 else 'It is not'} a leap year."
        )

    def timezone(self) -> str:
        current = self._india_now()
        return f"The timezone is India Standard Time (IST), Asia/Kolkata, UTC{current.strftime('%z')[:3]}:{current.strftime('%z')[3:]}."

    def current_utc(self) -> str:
        return f"The current UTC time is {self._india_now().astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC."

    def timestamp(self) -> str:
        return f"The current Unix timestamp is {int(self._india_now().timestamp())}."

    def greet(self) -> str:
        return "Hello. I am Zero, your assistant."

    def help(self) -> str:
        lines = ["Available commands:"]
        lines.extend(
            f"- {command.name}: {command.description}"
            for command in self._commands.values()
        )
        return "\n".join(lines)

    def skills(self) -> str:
        return "The skills have yet to be built. Current skills: greeting, time, and date."

    def status(self) -> str:
        return "Zero v0.1 is online. Skills have yet to be built beyond greeting, time, and date."

    def quit(self) -> str:
        return "Goodbye."

    def unknown_command(self) -> str:
        return (
            "The skills have yet to be built for that command. "
            "Available commands: time, time details, calendar, timezone, utc, "
            "timestamp, date, date details, today, tomorrow, yesterday, greet, "
            "help, skills, status, quit."
        )


def run() -> None:
    assistant = ZeroAssistant()
    print("Zero v0.1 online. Type 'help' for commands or 'quit' to exit.")

    while True:
        try:
            request = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return

        response = assistant.handle(request)
        print(f"Zero: {response}")
        if request.strip().lower() in {"quit", "exit", "bye"}:
            return


if __name__ == "__main__":
    run()
# Zero v0.1

## Release

Zero v0.1 is a dependency-free command line assistant with a command router, reliable error handling, and India Standard Time support.

## Run

From the repository root:

```bash
python3 assistant.py
```

## Commands

### Time and date

- `time`: Shows India local time in 12-hour and 24-hour formats.
- `time details`: Shows complete local time, UTC time, and Unix timestamp details.
- `calendar`: Shows weekday, ISO week, day of year, quarter, and leap-year status.
- `timezone`: Shows the configured timezone, `Asia/Kolkata`.
- `utc`: Shows the current UTC time.
- `timestamp`: Shows the current Unix timestamp.
- `date`: Shows today's ISO date.
- `date details`: Shows complete calendar details for today.
- `today`: Shows today's date details.
- `tomorrow`: Shows tomorrow's date details.
- `yesterday`: Shows yesterday's date details.

### Assistant

- `greet`, `hello`, `hi`, or `hey`: Greets the user.
- `help`: Lists available commands.
- `skills`: Shows the current skill status.
- `status`: Shows that Zero is online.
- `quit`, `exit`, or `bye`: Exits the assistant.

## Natural language

Zero accepts natural questions such as:

- `what's the time`
- `tell me today's date`
- `what day is it`
- `what time zone am I in`
- `what time is it in utc`
- `what is the timestamp`
- `hey what's today's date and time`

Date and time questions can be combined with greetings and with each other.

## Tests

Run the test suite with:

```bash
python3 -m unittest -v
```

Zero v0.1 is complete when all tests pass.

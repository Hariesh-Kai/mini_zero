# Zero v0.1

A dependency-free command line assistant with a small command router. Time and date use India Standard Time (IST, `Asia/Kolkata`).

## Run

```bash
python3 assistant.py
```

Available commands:

- `time` or `what time is it`
- `time details` or `detailed time`
- `calendar`, `calendar details`, or `what day is it`
- `timezone`
- `utc` or `utc time`
- `timestamp` or `epoch time`
- `date` or `what is today date`
- `date details`, `detailed date`, or `full date`
- `today`
- `tomorrow` or `what date is tomorrow`
- `yesterday` or `what date was yesterday`
- `greet`, `hello`, `hi`, or `hey`
- `help`
- `skills`
- `status`
- `quit`

The date skill reports the long date, ISO date, weekday, ISO week, day of year, days remaining in the year, month, quarter, and leap-year status. It also answers relative questions about today, tomorrow, and yesterday. Unknown commands are handled safely and list the available commands.

Natural questions are supported, including `what's the time`, `tell me the time`, `what's the date`, `what day is it`, `what time zone am I in`, `what time is it in utc`, and `what is the timestamp`. These can be combined with greetings and with date/time requests.

## Test

```bash
python3 -m unittest -v
```
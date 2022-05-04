from datetime import datetime, timedelta

from core.config import COLORS


def ceil_dt(dt: datetime, delta: timedelta) -> str:
    """round up function"""
    return (dt + (datetime.min - dt) % delta).strftime("%H:%M")


def set_style_button(state: str, x: int, y: int, offset: int) -> str:
    """function sets styles for buttons"""
    return f"""
        div:nth-child({offset}) > div:nth-child({y}) > div:nth-child(1) > div > div:nth-child({x}) > div > button {{
        border-color: {COLORS[state]};
        border-width: 2px;

        width:100px;
        border-radius: 10px;
        height:2em;
        color:#fffffff;
    }}
    div:nth-child({offset}) > div:nth-child({y}) > div:nth-child(1) > div > div:nth-child({x}) > div > button:hover {{
        background-color: #ff4c4c;
        border-width: 2px;
        width:100px;
        border-radius: 10px;
        height:2em;
        color:#ffffff;
    }}   
    """


# 6em
def calculate_index(start, end) -> float:
    """Function counts the number of time slots between two dates"""
    return (end - start) / timedelta(minutes=30)


def to_readable_format(date: datetime) -> str:
    """the function converts the date to a human-readable format"""
    return date.strftime(r"%d.%m.%Y %H:%M")


def format_events(event) -> str:
    """event formatting function"""
    return f"{to_readable_format(event.start_date)} — {to_readable_format(event.end_date)} Комната: {event.room} место: {event.place}"

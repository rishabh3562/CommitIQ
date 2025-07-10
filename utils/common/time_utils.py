from datetime import datetime, timedelta
from dateutil.parser import parse as dt_parse
def iso_now_minus(days=7):
    return (datetime.utcnow() - timedelta(days=days)).isoformat() + "Z"
def iso_now():
    return datetime.utcnow().isoformat() + "Z"
def iso_now_plus(days=7):
    return (datetime.utcnow() + timedelta(days=days)).isoformat() + "Z"


def convert_to_iso(date_str):
    return dt_parse(date_str, dayfirst=True).date().isoformat()

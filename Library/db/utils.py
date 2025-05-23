from datetime import date

def calculate_total_days(issue_date: date, return_date: date) -> int:
    return (return_date - issue_date).days

def calculate_rent(total_days: int, rate_per_day: float = 10.0) -> float:
    return total_days * rate_per_day

def full_image_url(path: str, base_url: str = "http://localhost:8000") -> str:
    if not path:
        return ""
    return f"{base_url}/images/{path}"

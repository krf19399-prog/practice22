SLA_HOURS = {
    "low": 72,
    "medium": 24,
    "high": 8,
    "critical": 2,
}
 
 
def _normalize_priority(priority):
    if not isinstance(priority, str):
        raise TypeError("priority must be a string")
    normalized = priority.strip().lower()
    if normalized not in SLA_HOURS:
        raise ValueError("unknown priority")
    return normalized
 
 
def _validate_vip(is_vip):
    if not isinstance(is_vip, bool):
        raise TypeError("is_vip must be bool")
 
 
def calculate_sla(priority, is_vip=False):
    priority = _normalize_priority(priority)
    _validate_vip(is_vip)
    hours = SLA_HOURS[priority]
    return max(1, hours // 2) if is_vip else hours
 
 
def build_ticket(title, priority, is_vip=False):
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    title = title.strip()
    if not 5 <= len(title) <= 100:
        raise ValueError("title length must be from 5 to 100")
    priority = _normalize_priority(priority)
    return {
        "title": title,
        "priority": priority,
        "is_vip": is_vip,
        "sla_hours": calculate_sla(priority, is_vip),
        "status": "open",
    }
 
 
def remaining_hours(ticket, elapsed_hours):
    if isinstance(elapsed_hours, bool) or not isinstance(
        elapsed_hours, (int, float)
    ):
        raise TypeError("elapsed_hours must be a number")
    if elapsed_hours < 0:
        raise ValueError("elapsed_hours cannot be negative")
    return max(0, ticket["sla_hours"] - elapsed_hours)

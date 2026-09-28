import pytest
 
from helpdesk import build_ticket, calculate_sla, remaining_hours
 
 
def test_sla_for_each_priority():
    assert calculate_sla("low") == 72
    assert calculate_sla("medium") == 24
    assert calculate_sla("high") == 8
    assert calculate_sla("critical") == 2
 
 
def test_priority_is_normalized():
    assert calculate_sla(" HIGH ") == 8
 
 
def test_vip_reduces_sla():
    assert calculate_sla("high", True) == 4
 
 
def test_unknown_priority():
    with pytest.raises(ValueError):
        calculate_sla("urgent")
 
 
def test_invalid_priority_type():
    with pytest.raises(TypeError):
        calculate_sla(None)
 
 
def test_invalid_vip_type():
    with pytest.raises(TypeError):
        calculate_sla("low", "yes")
 
 
def test_build_ticket():
    ticket = build_ticket("Printer is unavailable", "critical")
    assert ticket["status"] == "open"
    assert ticket["sla_hours"] == 2
 
 
def test_title_is_trimmed():
    ticket = build_ticket("  Network problem  ", "high")
    assert ticket["title"] == "Network problem"
 
 
def test_invalid_title_type():
    with pytest.raises(TypeError):
        build_ticket(123, "low")
 
 
def test_short_title():
    with pytest.raises(ValueError):
        build_ticket("Err", "low")
 
 
def test_long_title():
    with pytest.raises(ValueError):
        build_ticket("x" * 101, "low")
 
 
def test_remaining_hours():
    ticket = build_ticket("Database is unavailable", "high")
    assert remaining_hours(ticket, 3) == 5
 
 
def test_remaining_hours_never_negative():
    ticket = build_ticket("Database is unavailable", "critical")
    assert remaining_hours(ticket, 10) == 0
 
 
def test_negative_elapsed_hours():
    ticket = build_ticket("Database is unavailable", "high")
    with pytest.raises(ValueError):
        remaining_hours(ticket, -1)
 
 
@pytest.mark.parametrize("value", [True, "4"])
def test_invalid_elapsed_hours_type(value):
    ticket = build_ticket("Database is unavailable", "high")
    with pytest.raises(TypeError):
        remaining_hours(ticket, value)

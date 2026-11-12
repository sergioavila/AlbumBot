from datetime import date

from scripts.adoption_gate import is_adoption_period


def test_adoption_period_includes_deadline() -> None:
    assert is_adoption_period(date(2026, 11, 25))


def test_adoption_period_ends_after_deadline() -> None:
    assert not is_adoption_period(date(2026, 11, 26))

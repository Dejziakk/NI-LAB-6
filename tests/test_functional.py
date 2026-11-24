import pytest

from src.manager import Manager
from src.models import Parameters, Transfer


def test_total_due_matches_apartment_costs():
    manager = Manager(Parameters())
    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    settlement = manager.get_settlement('apart-polanka', 2025, 1)
    tenants_settlements = manager.create_tenants_settlements(settlement)

    total = 0.0
    for ts in tenants_settlements:
        total += ts.total_due_pln

    assert total == pytest.approx(costs)


def test_get_tax():
    manager = Manager(Parameters())
    assert manager.get_tax(2025, 1, 0.085) == 638
    assert manager.get_tax(2025, 2, 0.085) == 0

    manager.transfers.append(Transfer(
        amount_pln=1000.0,
        date='2025-03-05',
        settlement_year=2025,
        settlement_month=3,
        tenant='tenant-1'
    ))
    assert manager.get_tax(2025, 3, 0.085) == 85

    with pytest.raises(ValueError):
        manager.get_tax(2025, 13, 0.085)

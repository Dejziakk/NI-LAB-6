import pytest

from src.manager import Manager
from src.models import Parameters, Transfer


def test_total_due_matches_apartment_costs():
    manager = Manager(Parameters())

    apartment_costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    apartment_settlement = manager.get_settlement('apart-polanka', 2025, 1)
    tenants_settlements = manager.create_tenants_settlements(apartment_settlement)

    assert apartment_costs is not None
    assert apartment_settlement is not None
    assert len(tenants_settlements) > 0

    total_tenants_due = 0.0
    for tenant_settlement in tenants_settlements:
        total_tenants_due += tenant_settlement.total_due_pln

    assert total_tenants_due == pytest.approx(apartment_costs)
    assert total_tenants_due == pytest.approx(apartment_settlement.total_due_pln)


def test_get_tax_for_month():
    manager = Manager(Parameters())

    tax = manager.get_tax(2025, 1, 0.085)
    assert tax == 638

    tax_empty = manager.get_tax(2025, 2, 0.085)
    assert tax_empty == 0


def test_get_tax_with_custom_transfers():
    manager = Manager(Parameters())
    manager.transfers = [
        Transfer(
            amount_pln=1000.0,
            date='2025-03-05',
            settlement_year=2025,
            settlement_month=3,
            tenant='tenant-1'
        ),
        Transfer(
            amount_pln=1000.0,
            date='2025-03-10',
            settlement_year=2025,
            settlement_month=3,
            tenant='tenant-2'
        ),
    ]

    tax = manager.get_tax(2025, 3, 0.085)
    assert tax == 170

    with pytest.raises(ValueError):
        manager.get_tax(2025, 13, 0.085)


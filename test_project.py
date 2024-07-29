import pytest
from project import get_args
from otm_helper import OnTheMarketSearch, OnTheMarketResult


def test_get_args_required_args(monkeypatch):
    # Mock command line arguments
    monkeypatch.setattr('sys.argv', ['script.py', '--postcode', 'SW111HF', '--radius', '10'])

    # Test case for required arguments
    args = get_args()
    assert args.postcode == 'sw11-1hf'
    assert args.radius == 10.0
    assert args.min_price is None
    assert args.max_price is None
    assert args.min_bed is None
    assert args.max_bed is None
    assert args.type is None
    assert not args.potential_to_extend
    assert args.criteria is None
    assert args.debug is None


def test_get_args_all_args(monkeypatch):
    argv = ['script.py', '--postcode', 'SW111HF', '--radius', '10.0', '--min-price', '100000', '--max-price', '200000',
            '--min-bed', '2', '--max-bed', '4', '--type', 'house', '--potential-to-extend', '--criteria', 'garden', '--debug']
    monkeypatch.setattr('sys.argv', argv)

    args = get_args()
    assert args.postcode == 'sw11-1hf'
    assert args.radius == 10.0
    assert args.min_price == 100000
    assert args.max_price == 200000
    assert args.min_bed == 2
    assert args.max_bed == 4
    assert args.type == 'house'
    assert args.potential_to_extend
    assert args.criteria == 'garden'
    assert args.debug


def test_get_args_different_postcodes(monkeypatch):
    # Case 1 - no space
    monkeypatch.setattr('sys.argv', ['script.py', '--postcode', 'SW111HF', '--radius', '10'])

    args = get_args()
    assert args.postcode == 'sw11-1hf'
    assert args.radius == 10.0

    # Case 2 - space
    monkeypatch.setattr('sys.argv', ['script.py', '--postcode', 'SW11 1HF', '--radius', '10'])

    args = get_args()
    assert args.postcode == 'sw11-1hf'
    assert args.radius == 10.0

    # Case 3 - random case
    monkeypatch.setattr('sys.argv', ['script.py', '--postcode', 'sW111hF', '--radius', '10'])

    args = get_args()
    assert args.postcode == 'sw11-1hf'
    assert args.radius == 10.0

    # Case 4 - double space
    monkeypatch.setattr('sys.argv', ['script.py', '--postcode', 'SW11  1HF', '--radius', '10'])

    args = get_args()
    assert args.postcode == 'sw11-1hf'
    assert args.radius == 10.0


def test_get_args_different_radius(monkeypatch):
    # Case 1 - int
    monkeypatch.setattr('sys.argv', ['script.py', '--postcode', 'SW111HF', '--radius', '10'])

    args = get_args()
    assert args.postcode == 'sw11-1hf'
    assert args.radius == 10.0

    # Case 2 - float rounded to the next 0.25
    monkeypatch.setattr('sys.argv', ['script.py', '--postcode', 'SW111HF', '--radius', '10.33'])

    args = get_args()
    assert args.postcode == 'sw11-1hf'
    assert args.radius == 10.25

    # Case 3 - sub 0.25
    monkeypatch.setattr('sys.argv', ['script.py', '--postcode', 'SW111HF', '--radius', '0'])

    args = get_args()
    assert args.postcode == 'sw11-1hf'
    assert args.radius == 0.25


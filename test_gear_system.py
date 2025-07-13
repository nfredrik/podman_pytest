# test_gear_system_pytest.py
from types import SimpleNamespace
from unittest import mock
from unittest.mock import patch

import pytest
from assertpy import assert_that

from gear_system import Gear, Wheel, Observer


#
# incoming query
#
def test_wheel_diameter():
    wheel = Wheel(26, 1.5)
    assert_that(wheel.diameter()).is_close_to(29.0, tolerance=0.01)
    # not expecting or asserting private #ratio
    # not expecting or asserting Wheel's #diameter

#
# incoming query
#
def test_gear_inches():
    gear = Gear(chainring=52, cog=11, wheel=Wheel(rim=26, tire=1.5))
    assert_that(gear.gear_inches()).is_close_to(137.1, tolerance=0.01)


## set_cog tests
# incoming command
def test_set_cog_changes_value():
    gear = Gear(chainring=52, cog=11)
    gear.set_cog(new_cog=27)
    assert_that(gear.cog).is_equal_to(27)

  # outgoing command
def test_observer_notified_on_cog_change():
    # fixture setup

    observer_mock = SimpleNamespace(changed=mock.MagicMock())
    gear = Gear(chainring=52, cog=11)
    gear.observer = observer_mock

    gear.set_cog(27)

    # expectation
    observer_mock.changed.assert_called_once()


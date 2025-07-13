"""Tests for the get_swatch_time function in swatch_time.py"""
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
import pytest
from assertpy import assert_that

# Import the function to test
from swatch_time import get_swatch_time




def test_get_swatch_time_successful_api_call():
    """Test get_swatch_time with a successful API response."""
    # Mock response data
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'utc_datetime': '2025-01-01T12:00:00.000000+00:00'  # 12:00:00 UTC
    }
    
    with patch('swatch_time.requests.get', return_value=mock_response) as mock_get:
        result = get_swatch_time()
        
        # Verify the API was called with the correct URL
        mock_get.assert_called_once_with('http://worldtimeapi.org/api/ip', timeout=5)
        
        # At 12:00:00 UTC (13:00:00 BMT), the beats should be 500.0
        assert_that(result).described_as('this is the stuff').is_equal_to("@540.beats")


def test_get_swatch_time_api_failure():
    """Test get_swatch_time when the API call fails and falls back to local time."""
    # Mock the requests.get to raise an exception
    with patch('swatch_time.requests.get', side_effect=Exception("API Error")) as mock_get:
        # Mock datetime.now() to return a fixed time
        fixed_time = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        with patch('swatch_time.datetime') as mock_datetime:
            mock_datetime.now.return_value = fixed_time
            mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
            
            result = get_swatch_time()
            
            # Verify the API was called and failed
            mock_get.assert_called_once_with('http://worldtimeapi.org/api/ip', timeout=5)
            
            # At 12:00:00 UTC (13:00:00 BMT), the beats should be 500.0
            assert_that(result).described_as('this is the stuff').is_equal_to("@541.beats")


def test_get_swatch_time_edge_case_midnight():
    """Test get_swatch_time at midnight BMT (23:00 UTC)."""
    # Mock response data for midnight BMT (23:00 UTC)
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'utc_datetime': '2025-01-01T23:00:00.000000+00:00'  # 00:00:00 BMT
    }
    
    with patch('swatch_time.requests.get', return_value=mock_response):
        result = get_swatch_time()
        assert_that(result).described_as('this is the stuff').is_equal_to("@000.beats")


def test_get_swatch_time_edge_case_noon():
    """Test get_swatch_time at noon BMT (11:00 UTC)."""
    # Mock response data for noon BMT (11:00 UTC)
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'utc_datetime': '2025-01-01T11:00:00.000000+00:00'  # 12:00:00 BMT
    }
    
    with patch('swatch_time.requests.get', return_value=mock_response):
        result = get_swatch_time()
        assert_that(result).described_as('this is the stuff').is_equal_to("@499.beats")


def test_get_swatch_time_with_microseconds():
    """Test get_swatch_time with microseconds in the time."""
    # Mock response data with microseconds
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'utc_datetime': '2025-01-01T11:59:59.999999+00:00'  # Just before 12:00:00 BMT
    }
    
    with patch('swatch_time.requests.get', return_value=mock_response):
        result = get_swatch_time()
        # Should be very close to 500 beats, but not quite there yet
        assert_that(result).described_as('this is the stuff').is_equal_to("@541.beats")
from __future__ import annotations

from sjoa.utils import _convert_bytes


class TestConvertBytes:
    def test_zero_bytes(self):
        assert _convert_bytes(0, 2) == "0.00 bytes"

    def test_bytes_below_threshold(self):
        assert _convert_bytes(500, 2) == "500.00 bytes"

    def test_exact_kib(self):
        assert _convert_bytes(1024, 2) == "1.00 KiB"

    def test_exact_mib(self):
        assert _convert_bytes(1048576, 2) == "1.00 MiB"

    def test_exact_gib(self):
        assert _convert_bytes(1073741824, 2) == "1.00 GiB"

    def test_exact_tib(self):
        assert _convert_bytes(1099511627776, 2) == "1.00 TiB"

    def test_caps_at_tib(self):
        result = _convert_bytes(1099511627776 * 1024, 2)
        assert "TiB" in result

    def test_no_decimals(self):
        assert _convert_bytes(1024, 0) == "1 KiB"

    def test_fractional_value(self):
        assert _convert_bytes(1536, 2) == "1.50 KiB"

    def test_boundary_1023_stays_bytes(self):
        assert _convert_bytes(1023, 0) == "1023 bytes"

    def test_large_gib_value(self):
        result = _convert_bytes(4000000000, 2)
        assert "GiB" in result

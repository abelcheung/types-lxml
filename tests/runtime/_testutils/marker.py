import os

import pytest
from lxml.etree import LXML_VERSION

byte_bug_marker = pytest.mark.xfail(
    LXML_VERSION[:3] == (5, 1, 0),
    reason="lxml 5.1.0 has bug in bytes support of html processing functions",
)

github_fail_marker = pytest.mark.xfail(
    condition=os.getenv("GITHUB_ACTION") is not None,
    reason="Failures only on GitHub Actions CI",
)
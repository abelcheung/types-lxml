"""Consumer smoke test for a wheel installed without integration extras."""

from importlib.metadata import distributions
from typing import assert_type

from lxml import etree, html

installed = {distribution.metadata["Name"].lower() for distribution in distributions()}
assert not installed.intersection({
    "beautifulsoup4",
    "soupsieve",
    "html5lib",
    "types-html5lib",
})

assert_type(etree.fromstring(b"<root/>"), etree._Element)
assert_type(html.fromstring("<p>Hello</p>"), html.HtmlElement)

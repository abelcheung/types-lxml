from functools import partial

from ..builder import ElementMaker
from ._element import HtmlElement
from ._form import (
    FormElement,
    InputElement,
    LabelElement,
    SelectElement,
    TextareaElement,
)

E: ElementMaker[HtmlElement]

# Use inferred type, value is not important in stub
A = E.a
ABBR = E.abbr
ACRONYM = E.acronym
ADDRESS = E.address
APPLET = E.applet
AREA = E.area
ARTICLE = E.article
ASIDE = E.aside
AUDIO = E.audio
B = E.b
BASE = E.base
BASEFONT = E.basefont
BDI = E.bdi
BDO = E.bdo
BIG = E.big
BLOCKQUOTE = E.blockquote
BODY = E.body
BR = E.br
BUTTON = E.button
CANVAS = E.canvas
CAPTION = E.caption
CENTER = E.center
CITE = E.cite
CODE = E.code
COL = E.col
COLGROUP = E.colgroup
DATA = E.data
DATALIST = E.datalist
DD = E.dd
DEL = E.__getattr__("del")
DETAILS = E.details
DFN = E.dfn
DIALOG = E.dialog
DIR = E.dir
DIV = E.div
DL = E.dl
DT = E.dt
EM = E.em
EMBED = E.embed
FIELDSET = E.fieldset
FIGCAPTION = E.figcaption
FIGURE = E.figure
FONT = E.font
FOOTER = E.footer
FORM: partial[FormElement]
FRAME = E.frame
FRAMESET = E.frameset
H1 = E.h1
H2 = E.h2
H3 = E.h3
H4 = E.h4
H5 = E.h5
H6 = E.h6
HEAD = E.head
HEADER = E.header
HGROUP = E.hgroup
HR = E.hr
HTML = E.html
I = E.i
IFRAME = E.iframe
IMG = E.img
INPUT: partial[InputElement]
INS = E.ins
ISINDEX = E.isindex
KBD = E.kbd
LABEL: partial[LabelElement]
LEGEND = E.legend
LI = E.li
LINK = E.link
MAIN = E.main
MAP = E.map
MARK = E.mark
MARQUEE = E.marquee
MENU = E.menu
META = E.meta
METER = E.meter
NAV = E.nav
NOBR = E.nobr
NOFRAMES = E.noframes
NOSCRIPT = E.noscript
OBJECT = E.object
OL = E.ol
OPTGROUP = E.optgroup
OPTION = E.option
OUTPUT = E.output
P = E.p
PARAM = E.param
PICTURE = E.picture
PORTAL = E.portal
PRE = E.pre
PROGRESS = E.progress
Q = E.q
RB = E.rb
RP = E.rp
RT = E.rt
RTC = E.rtc
RUBY = E.ruby
S = E.s
SAMP = E.samp
SCRIPT = E.script
SEARCH = E.search
SECTION = E.section
SELECT: partial[SelectElement]
SLOT = E.slot
SMALL = E.small
SOURCE = E.source
SPAN = E.span
STRIKE = E.strike
STRONG = E.strong
STYLE = E.style
SUB = E.sub
SUMMARY = E.summary
SUP = E.sup
TABLE = E.table
TBODY = E.tbody
TD = E.td
TEMPLATE = E.template
TEXTAREA: partial[TextareaElement]
TFOOT = E.tfoot
TH = E.th
THEAD = E.thead
TIME = E.time
TITLE = E.title
TR = E.tr
TRACK = E.track
TT = E.tt
U = E.u
UL = E.ul
VAR = E.var
VIDEO = E.video
WBR = E.wbr

# attributes
ATTR = dict

def CLASS(v: str) -> dict[str, str]: ...
def FOR(v: str) -> dict[str, str]: ...

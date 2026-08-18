"""Shared pill/badge rendering + status color mapping.

Colors follow the dataviz status palette (good/warning/serious/critical) --
these are fixed, meaning-carrying colors and intentionally not themed. Risk
bands map onto that severity scale 1:1 (Normal->good ... Critical->critical),
and per-factor "Impact" / event "Result" reuse the same scale since they are
also severity/outcome states, not categorical series.
"""

GOOD = "#0ca30c"
WARNING = "#fab219"
SERIOUS = "#ec835a"
CRITICAL = "#d03b3b"

BAND_COLORS = {
    "Normal": GOOD,
    "Suspicious": WARNING,
    "High Risk": SERIOUS,
    "Critical": CRITICAL,
}
# warning's pale yellow needs dark text to stay legible; the rest are dark
# enough for white text
BAND_TEXT_COLORS = {
    "Normal": "#ffffff",
    "Suspicious": "#2b2100",
    "High Risk": "#ffffff",
    "Critical": "#ffffff",
}

IMPACT_COLORS = {"Low": GOOD, "Medium": WARNING, "High": SERIOUS}
IMPACT_TEXT_COLORS = {"Low": "#ffffff", "Medium": "#2b2100", "High": "#ffffff"}

RESULT_COLORS = {"Success": (GOOD, "#ffffff"), "Failure": (CRITICAL, "#ffffff")}


def _pill(text: str, bg: str, fg: str) -> str:
    return (
        '<span style="display:inline-block;padding:3px 11px;border-radius:999px;'
        f'font-size:0.78rem;font-weight:700;background:{bg};color:{fg};'
        f'white-space:nowrap;">{text}</span>'
    )


def band_badge(band: str) -> str:
    return _pill(band, BAND_COLORS.get(band, "#898781"), BAND_TEXT_COLORS.get(band, "#ffffff"))


def impact_badge(level: str) -> str:
    return _pill(level, IMPACT_COLORS.get(level, "#898781"), IMPACT_TEXT_COLORS.get(level, "#ffffff"))


def result_badge(result: str) -> str:
    bg, fg = RESULT_COLORS.get(result, ("#898781", "#ffffff"))
    return _pill(result, bg, fg)

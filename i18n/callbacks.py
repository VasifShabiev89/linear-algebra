"""Global locale switcher callbacks."""

from __future__ import annotations

from dash import Input, Output, callback

from i18n import normalize_locale


@callback(
    Output("locale", "data"),
    Input("locale-select", "value"),
    prevent_initial_call=True,
)
def set_locale(value: str | None) -> str:
    return normalize_locale(value)


@callback(
    Output("locale-select", "value"),
    Input("locale", "data"),
)
def sync_locale_select(locale: str | None) -> str:
    return normalize_locale(locale)

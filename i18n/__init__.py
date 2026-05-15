"""UI strings: Russian and English."""

from __future__ import annotations

from typing import Any

from i18n.catalog import MESSAGES

DEFAULT_LOCALE = "en"
SUPPORTED_LOCALES = frozenset({"en", "ru"})


def normalize_locale(locale: str | None) -> str:
    if locale in SUPPORTED_LOCALES:
        return locale
    return DEFAULT_LOCALE


def t(key: str, locale: str | None = "en", **kwargs: Any) -> str:
    lang = normalize_locale(locale)
    text = MESSAGES[lang].get(key) or MESSAGES[DEFAULT_LOCALE].get(key) or key
    if kwargs:
        return text.format(**kwargs)
    return text


def get_steps(topic: str, locale: str | None = "en") -> list[dict[str, str]]:
    lang = normalize_locale(locale)
    steps = MESSAGES[lang].get(f"{topic}.steps")
    if steps is None:
        steps = MESSAGES[DEFAULT_LOCALE][f"{topic}.steps"]
    return steps


def step_count(topic: str) -> int:
    return len(MESSAGES[DEFAULT_LOCALE][f"{topic}.steps"])


def preset_label(topic: str, preset_id: str, locale: str | None = "en") -> str:
    return t(f"{topic}.preset.{preset_id}.label", locale)


def preset_hint(topic: str, preset_id: str, locale: str | None = "en") -> str:
    return t(f"{topic}.preset.{preset_id}.hint", locale)

#!/usr/bin/env python
from typing import Dict, Any

from django.core.management import execute_from_command_line
from coltrane import _get_base_dir, _merge_settings, _configure_settings
from dotenv import load_dotenv

from django import setup as django_setup
from django.core.handlers.wsgi import WSGIHandler


def initialize(
        **django_settings: Dict[str, Any],
) -> WSGIHandler:
    """
    Initializes the Django static site.
    """

    base_dir = _get_base_dir(django_settings.get("BASE_DIR"))

    load_dotenv(base_dir / ".env")

    django_settings = _merge_settings(base_dir, django_settings)
    django_settings["INSTALLED_APPS"].insert(0, "pw")
    django_settings["ROOT_URLCONF"] = "pw.urls"
    _configure_settings(django_settings)

    django_setup()

    return WSGIHandler()


wsgi = initialize()

if __name__ == "__main__":
    execute_from_command_line()

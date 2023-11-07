#!/usr/bin/env python

from django.core.management import execute_from_command_line

from coltrane import initialize, DEFAULT_INSTALLED_APPS

wsgi = initialize(**{"ROOT_URLCONF": "pw.urls", "INSTALLED_APPS": ["pw"] + DEFAULT_INSTALLED_APPS})

if __name__ == "__main__":
    execute_from_command_line()

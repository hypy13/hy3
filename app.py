#!/usr/bin/env python

from django.core.management import execute_from_command_line

from coltrane import initialize

wsgi = initialize(**{"ROOT_URLCONF": "pw.urls", "INSTALLED_APPS": ["pw"]})

if __name__ == "__main__":
    execute_from_command_line()

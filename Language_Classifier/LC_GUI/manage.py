#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import re


def simple_tokenizer(txt, min_len=2):
    all_tokens = re.compile(r'[\w\d]+').findall(txt)
    all_tokens = [x.lower() for x in all_tokens]
    return [token for token in all_tokens if len(token) >= min_len]


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LC_GUI.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

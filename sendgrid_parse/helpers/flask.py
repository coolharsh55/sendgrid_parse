#!/usr/bin/python
# -*- coding: utf-8 -*-

# === flask ===

# This helper works with **flask** where the `request` variable
# containing the POST parameters is available via `request.form`
# and the attachments are available via `request.files`.

from sendgrid_parse import parse as base_parse


def parse(request):
    """Wraps sendgrid_parse and uses flask specific parameters"""
    if request is None:
        return None

    if getattr(request, 'method', None) is None:
        return None

    if getattr(request, 'form', None) is None:
        return None

    if request.method != 'POST':
        return None

    if request.form is None:
        return None

    return base_parse(request.form, request.files)

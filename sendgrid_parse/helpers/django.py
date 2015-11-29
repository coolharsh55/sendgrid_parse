#!/usr/bin/python
# -*- coding: utf-8 -*-

# === django ===

# This helper works with **django* where the `request` variable
# containing the POST parameters is available via `request.POST`
# and the attachments are available via `request.FILES`.

from sendgrid_parse import parse as base_parse


def parse(request):
    """Wraps sendgrid_parse and uses django specific parameters"""
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

    return base_parse(request.POST, request.FILES)

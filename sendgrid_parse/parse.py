#!/usr/bin/python
# -*- coding: utf-8 -*-

# === Webhook API ===

# ** Sendgrid's Inbox Parse Webhook API **
#
# The Parse API will _POST_ the parsed email to a _URL_ specified in the
# Sendgrid settings. If _POST_ is unsuccesful,
# SendGrid automatically queues and
# retries any POSTs that respond with a `4XX` or `5XX` status.
# To prevent redelivery or queueing of the mail, respond with `2XX`.
# Messages that cannot be delivered after **3 days** will be dropped.

# ** POST Parameters **
#
# **headers**: _raw_ headers of the email
#
# **text**: text body of the email.
# If not set, the email did not have a text body.
#
# **html**: HTML body of the email.
# If not set, the email did not have a HTML body.
#
# **from**: email sender taken from message headers.
#
# **to**: email recipient field taken from message headers.
#
# **cc**: email cc field taken from message headers.
#
# **subject**: email subject.
#
# **dkim**: a _JSON_ string containing the verification results of any
# dkim and domain keys signatures in the message.
#
# **SPF**: results of Sender Policy Framework verification of the
# message sender and receiving IP address.
#
# **envelope**: _JSON_ string containing the _SMTP_ envelope.
# Has two variables:
#   **to**: a single-element array containing the receiving address;
#   **from**: return path of the message.
#
# **charsets**: _JSON_ string for character set of fields extracted.
#
# **spam_score**: Spam Assassin's rating for whether this is _spam_.
#
# **spam_report**: Spam Assassin's spam report.
#
# **attachments**: Number of attachments included in email.
#
# **attachment-info**: _JSON_ string containing `attachmentX` keys
# with another _JSON_ string as the value.
# Contains the keys _filename_, _type_ (media type)
#
# **attachmentX**: file upload names, where **`N`** is the total number of
# attachments in the email. Attachments are provided as file uploads.


def parse(request, filedict=None):
    """
    Parses mails sent via POST by SendGrid.

    **Args**: `request: dict` containing POST request

    **Returns**: `dict` of items.

    **Raises**: `SendGridParseError` or its child classes.
    """

    # The `mail` dictionary will hold all required fields.
    # The `errors` dictionary will hold all errors.
    mail = {}
    errors = {}

    def _parse_nonempty_field(key, dictionary):
        value = dictionary.get(key, None)
        if value is None:
            errors[key] = "%s cannot be empty." % key
        return value

    # TODO: validate email addresses

    # get the address the mail was sent to
    mail['to'] = _parse_nonempty_field('to', request)

    # get the address the mail was sent from
    mail['from'] = _parse_nonempty_field('from', request)

    # get mail subject
    mail['subject'] = _parse_nonempty_field('subject', request)

    # CC and BCC fields.
    # It doesn't matter if these fields are empty,
    # the email would still be valid.
    mail['cc'] = request.get('cc', None)
    mail['bcc'] = request.get('bcc', None)

    # The body contents of the email can be in either text or html format.
    # The body can also be empty.
    # The body_type key offers hints on which values are available.
    mail['text'] = request.get('text', None)
    mail['html'] = request.get('html', None)

    # ```
    #     if mail['html'] is None:
    #         if mail['text'] is None:
    #             mail['body_type'] = None
    #         else:
    #             mail['body_type'] = 'text'
    #     else:
    #         mail['body_type'] = 'html'
    # ```

    # Retrieve the email RAW headers.
    mail['headers'] = _parse_nonempty_field('headers', request)

    # DKIM is a JSON string verification message
    mail['dkim'] = request.get('dkim', None)

    # SPF verification message
    mail['SPF'] = request.get('SPF', None)

    # TODO: parse _to_ and _from_

    # SMTP envelope containing JSON string
    mail['envelope'] = request.get('envelope', None)

    # TODO: encode fields using parsed charset

    # charset of the mail
    mail['charsets'] = request.get('charsets', None)

    # Spam score and report
    mail['spam_score'] = request.get('spam_score', None)
    mail['spam_report'] = request.get('spam_report', None)

    # TODO: save attachments to temporary location

    # Mail attachments is a list of attachments.
    # To get count, use `len()`.
    mail['attachments'] = []
    no_attachments = int(request.get('attachments', 0))
    if no_attachments > 0:
        if filedict is None:
            errors['attachments'] = "file dictionary is empty / None."
        else:
            for no in range(1, no_attachments + 1):
                attachment = filedict.get('attachment%d' % no, None)
                if attachment is None:
                    errors['attachment%d' % no] = "attachment%d is empty." % no
                else:
                    mail['attachments'].append(attachment)

    # Attach errors to the return object.
    # Uses property of empty dictionaries where -
    #
    #  - `d = {}`
    #  - `bool(d) is False`
    #  - `not d is True`
    #  - `len(d) == 0 is True`
    if errors:
        mail['errors'] = errors
    else:
        mail['errors'] = None

    return mail

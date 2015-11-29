SendGrid Inbound Parse Emails
-----------------------------

Parses SendGrid's Inbound Parse Emails into a dictionary of fields from POST parameters.

The Parse API will *POST* the parsed email to a *URL* specified in the
Sendgrid settings. If *POST* is unsuccesful,
SendGrid automatically queues and
retries any POSTs that respond with a `4XX` or `5XX` status.
To prevent redelivery or queueing of the mail, respond with `2XX`.
Messages that cannot be delivered after **3 days** will be dropped.

See `SendGrid documentation
<https://sendgrid.com/docs/API_Reference/Webhooks/parse.html>`_
for more details.


POST Parameters
---------------

The POST parameters are available from the returned dictionary with the following keys:

* **headers**: *raw* headers of the email

* **text**: text body of the email.
  If not set, the email did not have a text body.

* **html**: HTML body of the email.
  If not set, the email did not have a HTML body.

* **from**: email sender taken from message headers.

* **to**: email recipient field taken from message headers.

* **cc**: email cc field taken from message headers.

* **subject**: email subject.

* **dkim**: a *JSON* string containing the verification results of any
  dkim and domain keys signatures in the message.

* **SPF**: results of Sender Policy Framework verification of the
  message sender and receiving IP address.

* **envelope**: *JSON* string containing the *SMTP* envelope.
  Has two variables:

  1. **to**: a single-element array containing the receiving address;
  2. **from**: return path of the message.

* **charsets**: *JSON* string for character set of fields extracted.

* **spam_score**: Spam Assassin's rating for whether this is *spam*.

* **spam_report**: Spam Assassin's spam report.

* **attachments**: List containing file objects ordered by attachment number in email.
  If available, file object/stream will be appended to the list.
  If no file objects/streams are available, the attachment dictionary keys will be appended.
  These keys can be then used to access the attachments.
  Keys are the string ``attachment`` suffixed by n
  where n is in 1...N with N being the total number of attachments

* **attachment-info**: *JSON* string containing `attachmentX` keys
  with another *JSON* string as the value.
  Contains the keys *filename*, *type* (media type)

* **errors**: All errors are silently ignored and are returned as strings in a dictionary
  whose keys are the other keys. So, for e.g. an error about parsing *subject* is available as
  ``mail['errors']['subject']``


Helper utilities
----------------

The ``sendgrid_parse.helpers`` contains utilities for **flask** and **django**
that use the correct request variables to access the POST data and attachments.
These are wrappers around the ``parse`` method
and do not contain any framework specific except for naming and access conventions.


Usage
-----

The package is available under :code:`sendgrid_parse`.

.. code:: python

   # install
   pip install sendgrid_parse

   # plain python (args: POST dictionary, files dictionary)
   from sendgrid_parse import parse
   mail = parse(post_dict, file_dict)

   # for flask
   from sendgrid_parse.helpers.flask import parse
   # for django
   from sendgrid_parse.helpers.django import parse

   mail = parse(request)


Github Repository
-----------------

`sendgrid_parse
<https://github.com/coolharsh55/pnl2lnl>`_

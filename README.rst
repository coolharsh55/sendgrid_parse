SendGrid Inbound Parse Emails
--------------------------

Parses SendGrid's Inbound Parse Emails into a dictionary of fields from POST parameters.

The Parse API will _POST_ the parsed email to a _URL_ specified in the
Sendgrid settings. If _POST_ is unsuccesful,
SendGrid automatically queues and
retries any POSTs that respond with a `4XX` or `5XX` status.
To prevent redelivery or queueing of the mail, respond with `2XX`.
Messages that cannot be delivered after **3 days** will be dropped.

** POST Parameters **

**headers**: _raw_ headers of the email

**text**: text body of the email.
If not set, the email did not have a text body.

**html**: HTML body of the email.
If not set, the email did not have a HTML body.

**from**: email sender taken from message headers.

**to**: email recipient field taken from message headers.

**cc**: email cc field taken from message headers.

**subject**: email subject.

**dkim**: a _JSON_ string containing the verification results of any
dkim and domain keys signatures in the message.

**SPF**: results of Sender Policy Framework verification of the
message sender and receiving IP address.

**envelope**: _JSON_ string containing the _SMTP_ envelope.
Has two variables:
  **to**: a single-element array containing the receiving address;
  **from**: return path of the message.

**charsets**: _JSON_ string for character set of fields extracted.

**spam_score**: Spam Assassin's rating for whether this is _spam_.

**spam_report**: Spam Assassin's spam report.

**attachments**: Number of attachments included in email.

**attachment-info**: _JSON_ string containing `attachmentX` keys
with another _JSON_ string as the value.
Contains the keys _filename_, _type_ (media type)

**attachmentX**: file upload names, where **`N`** is the total number of
attachments in the email. Attachments are provided as file uploads.

To use, do (generic example):

    > from sendgrid_parse import parse
    > mail = parse(request.POST, request.files)

This is a generic example, in some frameworks, the POST data could be in `form` variable (in flask) whereas in others, it could be in the `POST` variable (in django). Also, the attachments sent via POST are stored in another dictionary, which can be `request.files` or `request.FILES`. If no file dictionary is supplied, parse will instead return a list of keys for accessing attachments in the file dictionary.

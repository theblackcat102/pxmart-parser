import os
import imaplib
from email.header import decode_header
import email
import dateparser
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

USER = os.getenv('EMAIL_ADDR')
PASS = os.getenv('EMAIL_PASS')


def parse_context(context):
    result = {}

    for line in context.split('\n'):
        if line[:len('From:')] == 'From:':
            result['from'] = line.replace('From: ', '').strip()
        elif line[:len('Date:')] == 'Date:':
            sent_date  = dateparser.parse(line.replace('Date: ', '').strip())
            result['date'] = sent_date
        elif line[:len('Subject: ')] == 'Subject: ':
            result['subject'] = line.replace('Subject: ', '').strip()
            # f.write(line+'\n')
    # print(result.keys())

    return result


def find_emails():
    imap_url = 'imap.gmail.com'
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(USER, PASS)
    con.select("INBOX")
    status, messages = con.search(None, "ALL")
    messages = messages[0].split()
    messages.reverse()

    for message in messages:
        # fetch the email message by ID
        res, raw_msg = con.fetch(message, "(RFC822)")
        if res == 'OK':
            for response in raw_msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])

                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes) and encoding != None:
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                        if '全聯電子發票' in subject:
                            body = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    ctype = part.get_content_type()
                                    cdispo = str(part.get('Content-Disposition'))

                                    # skip any text/plain (txt) attachments
                                    if ctype == 'text/plain' and 'attachment' not in cdispo:
                                        body = part.get_payload(decode=True)  # decode
                                        break
                            # not multipart - i.e. plain text, no attachments, keeping fingers crossed
                            else:
                                body = msg.get_payload(decode=True)
                            body_html = body.decode('utf-8')
                            context = parse_context(raw_msg[0][1].decode('utf-8'))
                            yield context, body_html

if __name__ == "__main__":
    imap_url = 'imap.gmail.com'
    con = imaplib.IMAP4_SSL(imap_url)
    con.login(USER, PASS)
    con.select("INBOX")
    status, messages = con.search(None, "ALL")
    messages = messages[0].split()
    print(con.list())
    messages.reverse()

    for message in messages:
        # fetch the email message by ID
        res, raw_msg = con.fetch(message, "(RFC822)")
        if res == 'OK':
            for response in raw_msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])

                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes) and encoding != None:
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                        if '全聯電子發票' in subject:
                            body = ""
                            if msg.is_multipart():
                                for part in msg.walk():
                                    ctype = part.get_content_type()
                                    cdispo = str(part.get('Content-Disposition'))

                                    # skip any text/plain (txt) attachments
                                    if ctype == 'text/plain' and 'attachment' not in cdispo:
                                        body = part.get_payload(decode=True)  # decode
                                        break
                            # not multipart - i.e. plain text, no attachments, keeping fingers crossed
                            else:
                                body = msg.get_payload(decode=True)
                            body_html = body.decode('utf-8')
                            context = parse_context(raw_msg[0][1].decode('utf-8'))
                            print(subject, context['date'])
                            output_file = os.path.join('examples', 
                                context['date'].strftime('%Y-%m-%d-%H-%M-%S.html'))
                            with open(output_file, 'w') as f:
                                f.write(body_html)



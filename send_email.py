import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

try:
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
except:
    pass

HEADERS = ['Date', 'ID', 'User', 'URL', 'Text']
EMAIL_AVATAR = {
    'addr': os.environ['BILL_LANG_EMAIL'],
    'username': 'william.langeford',
    'password': os.environ['BILL_LANG_PASSWORD'],
    'realname': 'William Langeford'
    }

def create_msg(addrs, subject):
    formataddr = lambda name, email: name + ' <' + email + '>'
    msg = MIMEMultipart('alternative')
    msg['To'] = ','.join([formataddr(name, email) for name, email in addrs.items()])
    msg['From'] = formataddr(EMAIL_AVATAR['realname'], EMAIL_AVATAR['addr'])
    msg['Subject'] = subject
    return msg

def attach_content(msg, message, message_html):
    part1 = MIMEText(message, 'plain')
    part2 = MIMEText(message_html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    return msg

def attach_images(msg, images):
    for image_id, imagefile in images.items(): # might need to be .PNG
        fp = open(imagefile, 'rb')
        img = MIMEImage(fp.read())
        img.add_header('Content-ID', '<' + image_id + '>')
        fp.close()
        msg.attach(img)
    return msg

def send_email_inner(args):
    """
    args is dict with the keys ['addrs', 'subject', 'message']
        where optional keys are ['message_html', 'images']
    'addrs' is dict of {name: email}
    'message' is str
    'message_html' is str
    'images' is dict of {image_id: image_filename}
        e.g. where message_html may reference image_id 'image1' as <img src="cid:image1">
    """
    addrs = args['addrs']
    subject = args['subject']
    message = args['message']
    message_html = args.get('message_html', message)
    images = args.get('images', {})

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.login(EMAIL_AVATAR['username'], EMAIL_AVATAR['password'])

    msg = create_msg(addrs, subject)
    msg = attach_content(msg, message, message_html)
    msg = attach_images(msg, images)
    
    s.sendmail(EMAIL_AVATAR['addr'], addrs.values(), msg.as_string())
    s.close()

def render(items):
    first_row = '<tr>' + '\n'.join(['<th>' + item + '</th>' for item in HEADERS]) + '</tr>'
    rows = [first_row]
    for item in items:
        row = '<tr>' + '\n'.join(['<td>{}</td>'.format(col) for col in item]) + '</tr>'
        rows.append(row)
    return '<table>' + '\n'.join(rows) + '</table>'

def send_update_email(msg, subj):
    html_msg = '<html><head></head><body>'
    html_msg += msg
    html_msg += '</body></html>'

    send_email_inner({'addrs': {'Jay': 'mobeets@gmail.com'},
            'subject': subj,
            'message': msg,
            'message_html': html_msg,
            })

def send_email(items):
    subj = '{} new #tweeprints'.format(len(items))
    if len(items) == 0:
        return
    html = render(items)
    print(subj)
    print(html)
    send_update_email(html, subj)

if __name__ == '__main__':
    send_email([[1,2,3,4,5], [4,5,6,7,8]])

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from main.models import Profile,Contact,Testimony,Collage,TestQuestion,Order,Token


def write_message(email,html_filename,image_filename,checkedValue,name,pdf_path):
    message = MIMEMultipart()
    message['to'] = email
    message['subject'] = 'XL Academy 試題購買'
    with open(html_filename, 'r') as html_file:
        html_body = html_file.read()
    with open(image_filename, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    html_body = html_body.replace('<!-- INSERT_IMAGE_HERE -->',f'<img style="height:38px" src="data:image/jpeg;base64,{image_data}" alt="Image">')
    html_body = html_body.replace('<!-- INSERT_NAME -->', name)
    html_msg = MIMEText(html_body, 'html')
    message.attach(html_msg)
    for id in list(checkedValue):
                testQuestion = TestQuestion.objects.filter(id= id).first()
                pdf_filename = f'{pdf_path}/{testQuestion.pdf}'
                with open(pdf_filename, 'rb') as pdf_file:
                        pdf_attachment = MIMEBase('application', 'octet-stream')
                        pdf_attachment.set_payload(pdf_file.read())
                        encoders.encode_base64(pdf_attachment)
                        pdf_attachment.add_header('Content-Disposition', f'attachment; filename={pdf_filename}')
                        message.attach(pdf_attachment)

    return  base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
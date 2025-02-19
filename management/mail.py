import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from main.models import Profile,Contact,Testimony,Collage,TestQuestion,Order,Token

import requests
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.conf import settings
import os


# 取得新的 access_token
def get_access_token():
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": settings.GMAIL_CLIENT_ID,
        "client_secret": settings.GMAIL_CLIENT_SECRET,
        "refresh_token": settings.GMAIL_REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }

    response = requests.post(token_url, data=data).json()
    return response.get("access_token")


# 發送 Email
def send_email(email,html_filename,image_filename,checkedValue,name,pdf_path):
    access_token = get_access_token()

    creds = Credentials(access_token)
    service = build('gmail', 'v1', credentials=creds)

    message = MIMEMultipart()
    message["to"] = email
    message["subject"] = "XL Academy 試題購買"

    # 2. 讀取 HTML 內容
    with open(html_filename, "r", encoding="utf-8") as html_file:
        html_body = html_file.read()

    # 3. 內嵌圖片，使用 Content-ID (CID)
    with open(image_filename, "rb") as image_file:
        image_data = image_file.read()
        image_part = MIMEBase("image", "jpeg")
        image_part.set_payload(image_data)
        encoders.encode_base64(image_part)
        image_part.add_header("Content-ID", "<email_image>")
        image_part.add_header("Content-Disposition", "inline", filename=os.path.basename(image_filename))
        message.attach(image_part)

    # 4. 替換 HTML 內的佔位符
    html_body = html_body.replace("<!-- INSERT_IMAGE_HERE -->",
                                  '<img style="height:38px" src="cid:email_image" alt="Image">')
    html_body = html_body.replace("<!-- INSERT_NAME -->", name)
    html_msg = MIMEText(html_body, "html")
    message.attach(html_msg)

    # 5. 添加 PDF 附件
    for id in checkedValue:
        testQuestion = TestQuestion.objects.filter(id=id).first()
        pdf_filename = os.path.join(f'{pdf_path}', f"{testQuestion.pdf}")
        print(pdf_filename)

        with open(pdf_filename, "rb") as pdf_file:
            pdf_attachment = MIMEBase("application", "octet-stream")
            pdf_attachment.set_payload(pdf_file.read())
            encoders.encode_base64(pdf_attachment)
            pdf_attachment.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(pdf_filename)}"')
            message.attach(pdf_attachment)

    # 6. 編碼郵件內容
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    send_request = {"raw": encoded_message}
    service.users().messages().send(userId="me", body=send_request).execute()


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
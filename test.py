# # from async_sender import Mail
# # import asyncio


# # async def send_email(
# #         title: str = "Hello",
# #         to: str = "denis.pis@yahoo.com",
# #         body: str = "Hello"
# # ):
# #     mail = Mail()
# #     await mail.send_message("Hello", from_address="from@example.com",
# #                             to="to@example.com", body="Hello world!")


# # asyncio.run(send_email())

# import asyncio
# from email.message import EmailMessage

# from aiosmtplib import SMTP, send


# async def say_hello():
#     email = "piskarev.py@yandex.ru"
#     password = "hufxmblgfzpcobyy"
#     # message = EmailMessage()
#     # message["From"] = email
#     # message["To"] = "rikotem929@scubalm.com"
#     # message["Subject"] = "Hello World!"
#     # message.set_content("Sent via aiosmtplib")

#     server = SMTP('smtp.yandex.ru', 465)
#     server.ehlo()  # Кстати, зачем это?
#     server.starttls()
#     server.login(email, password)

#     dest_email = "rikotem929@scubalm.com"
#     subject = 'Booking from chatbot'
#     email_text = 'Text'
#     message = 'From: %s\nTo: %s\nSubject: %s\n\n%s' % (email, dest_email, subject, email_text)

#     # server.set_debuglevel(1)  # Необязательно; так будут отображаться данные с сервера в консоли
#     server.sendmail(email, "rikotem929@scubalm.com", message)
#     await server.quit()

# #     await send(
# #         message,
# #         hostname="smtp.yandex.ru",
# #         port=465,
# #         username="CosmoWins1@yandex.ru",
# #         password="hufxmblgfzpcobyy"
# #         )

# #     smtp_client = SMTP("smtp.yandex.ru", 465)
# #     await smtp_client.starttls()
# #     await smtp_client.login("CosmoWins1", "hufxmblgfzpcobyy")
# #     await smtp_client.connect()
# #     async with smtp_client:
# #         await smtp_client.send(message)

# asyncio.run(say_hello())


import smtplib


smtp_server = smtplib.SMTP_SSL("smtp.yandex.ru", 465)
# smtp_server.starttls()
smtp_server.login("piskarev.py@yandex.ru", "rdijvzsxvlftmozs")

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 
# Создание объекта сообщения
msg = MIMEMultipart()
 
# Настройка параметров сообщения
msg["From"] = "piskarev.py@yandex.ru"
msg["To"] = 'rikotem929@scubalm.com'
msg["Subject"] = "Тестовое письмо 📧"
 
# Добавление текста в сообщение
text = "Привет! Это тестовое письмо, отправленное с помощью Python 😊"
msg.attach(MIMEText(text, "plain"))
 
# Отправка письма
smtp_server.sendmail("piskarev.py@yandex.ru", 'rikotem929@scubalm.com', msg.as_string())
 
# Закрытие соединения
smtp_server.quit()

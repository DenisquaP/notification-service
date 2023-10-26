import asyncio

from aiosmtplib import SMTP


smtp_client = SMTP(hostname="smtp.yadnex.ru", port=465, use_tls=True)
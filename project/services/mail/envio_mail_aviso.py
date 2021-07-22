import os

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

load_dotenv()

EMAIL_QUE_ENVIA = os.getenv('SENDER_EMAIL')
EMAIL_PASSWORD = os.getenv('PASSWORD_EMAIL')
SERVIDOR_SMTP = os.getenv('SERVER_SMTP')
PUERTO_SMTP = os.getenv('PORT_SMTP')


def enviar_correo_de_notificacion(email_que_recibe, nombre_de_usuario, evento, endpoint, id_registro_endpoint):
  message = MIMEMultipart("alternative")
  message["Subject"] = "Aviso de modificación por parte de un Super Administrador"
  message["From"] = EMAIL_QUE_ENVIA
  message["To"] = email_que_recibe

  # Creando version en texto plano y version HTML del mensaje.
  text = """\
  Hola, ¿Como estas?
  Este correo es para notificar que el usuario {mail_nombre_de_usuario}
  *{mail_evento}* en el endpoint {mail_endpoint} un registro con el siguiente ID {mail_id_registro_endpoint}.
  """.format(mail_nombre_de_usuario=nombre_de_usuario, mail_evento=evento, mail_endpoint=endpoint, mail_id_registro_endpoint=id_registro_endpoint)

  html = """\
  <html>
    <body>
      <p>Hola, ¿Como estas?<br>
        Este correo es para notificar que el usuario <b>{mail_nombre_de_usuario}</b>
        *{mail_evento}* en el endpoint {mail_endpoint} un registro con el siguiente ID {mail_id_registro_endpoint}.
      </p>
    </body>
  </html>
  """.format(mail_nombre_de_usuario=nombre_de_usuario, mail_evento=evento, mail_endpoint=endpoint, mail_id_registro_endpoint=id_registro_endpoint)

  # Convirtiendo a objetos las versiones de los mensajes
  part1 = MIMEText(text, "plain")
  part2 = MIMEText(html, "html")

  # El cliente de correo electrónico intentará renderizar primero el mensaje HTML.
  message.attach(part1)
  message.attach(part2)

  # Creando conexión segura con el servidor para enviar el email.
  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(SERVIDOR_SMTP, PUERTO_SMTP, context=context) as server:
      server.login(EMAIL_QUE_ENVIA, EMAIL_PASSWORD)
      server.sendmail(
          EMAIL_QUE_ENVIA, email_que_recibe, message.as_string()
      )
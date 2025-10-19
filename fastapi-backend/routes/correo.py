from fastapi import APIRouter, FastAPI, HTTPException
from aiosmtplib import send
from dto import EmailRequest
from email.message import EmailMessage

app = FastAPI()

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

SMTP_USER = "daynortito13@gmail.com"
SMTP_PASSWORD = "ynug zgad jxzp bfar "

router = APIRouter(prefix="/correo", tags=["correo"])

@router.post("/enviar-correo")
async def enviar_correo(email_request: EmailRequest):
    try:
        message = EmailMessage()
        message["From"] = SMTP_USER
        message["To"] = ", ".join(email_request.destinatarios)
        message["Subject"] = email_request.asunto
        message.set_content(email_request.contenido)

        await send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
            start_tls=True,
        )
        return {"mensaje": "Correo enviado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo enviar el correo: {str(e)}")

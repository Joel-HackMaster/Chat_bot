import requests
import sett
import json
import time


def obtener_Mensaje_whatsapp(message):
    if 'type' not in message:
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']

    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no conocido'

    return text


def enviar_Mensaje_whatsapp(data):
    whatsapp_token = sett.whatsapp_token
    whatsapp_url = sett.whatsapp_url
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + whatsapp_token}
    response = requests.post(whatsapp_url, headers=headers, data=data)
    if response.status_code == 200:
        return 'mensaje enviado', 200
    else:
        response.raise_for_status()


def text_Message(number, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data


def buttonReply_Message(number, options, body, footer, sedd, messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data


def listReply_Message(number, options, body, footer, sedd, messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "header": {
                    "type": "text",
                    "text": "Opciones"
                },
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data


def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
            }
        }
    )

    return data


def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )

    return data


def get_media_id(media_name, media_type):
    media_id = ""
    if media_type == "image":
        media_id = sett.media_id_image(media_name, None)
    elif media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    elif media_type == "video":
        media_id = sett.videos.get(media_name, None)
    elif media_type == "audio":
        media_id = sett.audio.get(media_name, None)
    return media_id


def replyReaction_Message(number, messageId, reaction):
    data = json.dumps(
        {
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "reaction",
                "reaction": {
                    "message_id": messageId,
                    "emoji": reaction
                }
            }
        }
    )

    print("hola")
    return data


def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": {
                "message_id": messageId
            },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data


def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": messageId
        }
    )
    return data


def administrar_chatbot(text, number, messageId, name):
    text = text.lower()
    list = []
    if "hola" in text:
        body = "Hola! 👋 Bienvenido a mi plataforma de whatsapp. ¿Como puedo ayudarte?"
        footer = "Plataforma de Interaccion"
        options = ["👨‍🎓 Curriculum Vitae", "🗿 Agendar una cita"]

        replyButtonData = buttonReply_Message(
            number, options, body, footer, "sed1", messageId)
        # replyReaction = replyReaction_Message(number, messageId, "👍")
        # list.append(replyReaction)
        list.append(replyButtonData)
    elif "servicios" in text:
        body = "Estas son las opciones disponibles"
        footer = "Plataforma de Interaccion"
        options = ["👨‍🎓 Sobre Mi", "🗿 Web Portafolio", "📲Skills"]

        listReplyData = listReply_Message(
            number, options, body, footer, "sed2", messageId)
        sticker = sticker_Message(
            number, get_media_id("gato_festejando", "sticker"))
        list.append(sticker)
        list.append(listReplyData)
    elif "sobre mi" in text:
        body = "Buena Eleccion, ¿Te gustaria que te envie mi CV en formato PDF?"
        footer = "Plataforma de Interaccion"
        options = ["✅ Si, envia el PDF", "⛔ No, gracias"]

        replyButtonData = buttonReply_Message(
            number, options, body, footer, "sed3", messageId)
        list.append(replyButtonData)
    elif "si, envia el pdf" in text:
        # sticker = sticker_Message(number, get_media_id("perro_traje", "sticker"))
        textMessage = text_Message(
            number, "Genial, por favor espera un momento.")

        # enviar_Mensaje_whatsapp(sticker)
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(3)

        document = document_Message(
            number, sett.document_url, "Listo 👍", "Curriculum Vitae")

        enviar_Mensaje_whatsapp(document)
        time.sleep(3)

        body = "¿Te gustaria contactarme?"
        footer = "Plataforma de Interaccion"
        options = ["✅ Si, quiero contactar", "⛔ No, gracias"]

        replyButtonData = buttonReply_Message(
            number, options, body, footer, "sed4", messageId)
        list.append(replyButtonData)
    elif "si, quiero contactar" in text:
        body = "Genial, por favor espera un momento"
        footer = "Plataforma de Interaccion"
        options = ["✅ Contactar", "⛔ No contactar"]

        listReply = listReply_Message(
            number, options, body, footer, "sed5", messageId)
        list.append(listReply)
    elif "contactar" in text:
        body = "Genial, ⌚ En un momento te repondere"
        footer = "Plataforma de interaccion"
        options = ["✅ Sí, por favor", "⛔ No, gracias"]

        buttonReply = buttonReply_Message(
            number, options, body, footer, "sed6", messageId)
        list.append(buttonReply)
    elif "no, gracias" in text:
        textMessage = text_Message(
            number, "Perfecto! Recuerda que puedes contactarme en cualquier momento, ¡Hasta Luego!")
        list.append(textMessage)
    else:
        data = text_Message(
            number, "Lo siento, ¿Quieres que te ayude con alguna opcion?")
        list.append(data)

    for item in list:
        enviar_Mensaje_whatsapp(item)

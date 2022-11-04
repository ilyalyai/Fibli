import vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import requests
import random
from random import randint
import schedule
import time
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
import datetime
import json
from json import JSONDecodeError
import os
from google.colab import drive
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import pickle
from flask import jsonify
import tensorflow as tf
import numpy as np

settings = dict(one_time=False, inline=True)
# №1. Клавиатура с 3 кнопками: "показать всплывающее сообщение", "открыть URL" и изменить меню (свой собственный тип)
keyboard_1 = VkKeyboard(**settings)
# pop-up кнопка
keyboard_1.add_callback_button(label='Погода', color=VkKeyboardColor.PRIMARY, payload={"type": "request_day_weather"})
keyboard_1.add_line()
# кнопка по открытию ВК-приложения
keyboard_1.add_callback_button(label='Картинка дня NASA', color=VkKeyboardColor.PRIMARY, payload={"type": "SendNasaPicture"})
keyboard_1.add_line()
# кнопка переключения на 2ое меню
keyboard_1.add_callback_button(label='Выбрать мем', color=VkKeyboardColor.PRIMARY, payload={"type": "MemeMenu"})

# №2. Клавиатура с одной красной callback-кнопкой. Нажатие изменяет меню на предыдущее.
keyboard_2 = VkKeyboard(**settings)
keyboard_2.add_callback_button(label='Просто мем', color=VkKeyboardColor.PRIMARY, payload={"type": "GetMeme"})
keyboard_2.add_line()
keyboard_2.add_callback_button(label='MGR мем', color=VkKeyboardColor.PRIMARY, payload={"type": "GetMGRMeme"})
keyboard_2.add_line()
keyboard_2.add_callback_button(label='Милый мем', color=VkKeyboardColor.PRIMARY, payload={"type": "GetWholesomeMeme"})
keyboard_2.add_line()
keyboard_2.add_callback_button(label='P5 мем', color=VkKeyboardColor.PRIMARY, payload={"type": "GetP5Meme"})
keyboard_2.add_line()
# кнопка переключения назад, на 1ое меню.
keyboard_2.add_callback_button('Назад', color=VkKeyboardColor.NEGATIVE, payload={"type": "MemeMenu"})

session = requests.Session()
vk_session = vk_api.VkApi(token=vkToken)
longpoll = VkBotLongPoll(vk_session, group_id=vkGroupId)
vk = vk_session.get_api()

if not os.path.exists("fibliData"): 
  if not os.path.exists("/content/gdrive/My Drive/fiblyMeme/"):
    drive.mount("/content/gdrive")
  path = "/content/gdrive/My Drive/fiblyMeme/"
else:
  path = "/fibliData/"
sys.path.append(path)
#-3 часа
##if datetime.datetime.today().weekday() is 4:
##  schedule.every().day.at("13:45").do(SendUsHome)
##else:
##  schedule.every().day.at("14:45").do(SendUsHome)
##schedule.every().day.at("10:45").do(CheckIfTruthUnspoken)


#vk.messages.send(
#     chat_id=2,
  #    random_id=get_random_id(),
  #   sticker_id = 3871)
while True:
  try:
    #schedule.run_pending()
    for event in longpoll.listen():
      schedule.run_pending()
      if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat: #Если написали в беседе
          message = event.obj['message']          
          user_get=vk.users.get(user_ids = (message['from_id']))
          user_get=user_get[0]       
          first_name=user_get['first_name']
          last_name=user_get['last_name']
          separator = " "
          if(first_name == "Илья" and last_name == "Ляпцев"):
            first_name = "Сэр"
            last_name = ""
            separator = ""
            if(message['text']):
              if("режим админа" in message['text'].lower()):     
                adminModeId.append(event.chat_id)
                vk.messages.send(
                  chat_id=event.chat_id,
                  random_id=get_random_id(),
                  message="Режим админа включен")
                continue
              if("выключить" in message['text'].lower() and event.chat_id in adminModeId):     
                adminModeId.remove(event.chat_id)
                vk.messages.send(
                  chat_id=event.chat_id,
                  random_id=get_random_id(),
                  message="Режим админа выключен")
                continue
          if(event.chat_id in adminModeId):
            text = CheckAdminMessage(message['text'])
          else:
            text = ChechMessage(message['text'])
          if text: 
            vk.messages.send(
              chat_id=event.chat_id,
              random_id=get_random_id(),
              keyboard=(keyboard_1 if f_toggle else keyboard_2).get_keyboard() if keyboardOn else None,
              message=first_name + ", " + text.lower())
        if event.from_user: #Если написали в личке
          message = event.obj['message']       
          user_get=vk.users.get(user_ids = (message['from_id']))
          user_get=user_get[0]
          first_name=user_get['first_name']
          last_name=user_get['last_name']
          separator = " "
          if(first_name == "Илья" and last_name == "Ляпцев"):
            first_name = "Сэр"
            last_name = ""
            separator = "" 
            if(message['text']):
              if("режим админа" in message['text'].lower()):     
                adminModeId.append(message['from_id'])
                vk.messages.send(
                  user_id=message['from_id'],
                  random_id=get_random_id(),
                  message="Режим админа включен")
                continue
              if("выключить" in message['text'].lower() and message['from_id'] in adminModeId):     
                adminModeId.remove(message['from_id'])
                vk.messages.send(
                  user_id=message['from_id'],
                  random_id=get_random_id(),
                  message="Режим админа выключен")
                continue
          if(message['from_id'] in adminModeId):
            text = CheckAdminMessage(message['text'])
          else:
            text = ChechMessage(message['text'])
          if text:
            vk.messages.send(
                user_id=message['from_id'],
                random_id=get_random_id(),
                keyboard=(keyboard_1 if f_toggle else keyboard_2).get_keyboard() if keyboardOn else None,
                message=first_name + ", " + text.lower())
      elif event.type == VkBotEventType.MESSAGE_EVENT:
        if event.object.payload.get('type') == "GetMeme":
          GetMeme("");
        if event.object.payload.get('type') == "GetWholesomeMeme":
          GetMeme("wholesome");
        if event.object.payload.get('type') == "GetMGRMeme":
          GetMeme("MGRMemes");
        if event.object.payload.get('type') == "GetP5Meme":
          GetMeme("Persona5memes");
        elif event.object.payload.get('type') == "SendNasaPicture":
          SendNasaPicture();
        elif event.object.payload.get('type') == "request_day_weather":          
          if str(event.obj.peer_id).startswith('200000000'):
            vk.messages.send(
                        chat_id=str(event.obj.peer_id)[-1],
                        random_id=get_random_id(),
                        keyboard=(keyboard_1 if f_toggle else keyboard_2).get_keyboard() if keyboardOn else None,
                        message=request_day_weather()) 
          elif message['from_id']:
            vk.messages.send(
                        user_id=message['from_id'],
                        random_id=get_random_id(),
                        keyboard=(keyboard_1 if f_toggle else keyboard_2).get_keyboard() if keyboardOn else None,
                        message=request_day_weather()) 
        elif event.object.payload.get('type') == 'MemeMenu':
          f_toggle = not f_toggle
          last_id = vk.messages.edit(
                    peer_id=event.obj.peer_id,
                    message='Прошу!',
                    conversation_message_id=event.obj.conversation_message_id,
                    keyboard=(keyboard_1 if f_toggle else keyboard_2).get_keyboard() if keyboardOn else None)      
  except KeyboardInterrupt:
    #vk.messages.send(
      #chat_id=2,
      #random_id=get_random_id(),
      #message="Всем покеда!")
    break;
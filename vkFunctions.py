from apiKeys import *

# Запрос текущей погоды
def request_current_weather():
  res = requests.get(weatherKeyYandex, headers={'X-Yandex-API-Key': "74e0d337-e37f-448e-97e3-6efec5ef567c"})
  data = res.json()
  fact = data['fact']
  return(str(fact['temp']) + "\n__Ощущается как:" + str(fact['feels_like'])+"\n__Осадки:" + str(fact['condition']) +"\n__Ветер:" + str(fact['wind_dir']) + ' ' + str(fact['wind_speed']) + ' meters per second\n' + '')

# Запрос погоды на день
def request_day_weather():
  res = requests.get(weatherKeyYandex, headers={'X-Yandex-API-Key': "74e0d337-e37f-448e-97e3-6efec5ef567c"})
  data = res.json()
  fact = data['fact']
  parts = data["forecast"]['parts']
  result = str(fact['temp']) + "\n__Ощущается как: " + str(fact['feels_like'])+"\n__Осадки: " + str(fact['condition']) + "\n"
  for part in parts:
    if part["part_name"] == "morning":
      result = result + "Утром: " + str(part["temp_avg"]) + "\n__Осадки: "+ str(part['condition']) + "\n"
    if part["part_name"] == "day":
      result = result + "Днем: " + str(part["temp_avg"]) + "\n__Осадки: "+ str(part['condition']) + "\n"
    if part["part_name"] == "evening":
      result = result + "Вечером: " + str(part["temp_avg"]) + "\n__Осадки: "+ str(part['condition']) + "\n"
    if part["part_name"] == "night":
      result = result + "Ночью: " + str(part["temp_avg"]) + "\n__Осадки: "+ str(part['condition']) + "\n"
    
  return(result)

def SendNasaPicture():
  res = requests.get(nasaKey)
  data = res.json()
  upload = vk_api.VkUpload(vk)
  urllib.request.urlretrieve(data["url"], "picture.jpg")
  photo = upload.photo_messages("picture.jpg")
  owner_id = photo[0]['owner_id']
  photo_id = photo[0]['id']
  access_key = photo[0]['access_key']
  attachment = f'photo{owner_id}_{photo_id}_{access_key}'
  if str(event.obj.peer_id).startswith('200000000'):
    vk.messages.send(
              chat_id=str(event.obj.peer_id)[-1],
              random_id=get_random_id(),
              message=data["explanation"],
              attachment = attachment)  
  elif hasattr(event, 'chat_id') and event.chat_id:
    vk.messages.send(
              chat_id=event.chat_id,
              random_id=get_random_id(),
              message=data["explanation"],
              attachment = attachment)  
  elif message['from_id']:
    vk.messages.send(
                user_id=message['from_id'],
                random_id=get_random_id(),
                message=data["explanation"],
                attachment = attachment)

def GetQuote():
  res = requests.get(quoteKey)
  root = ET.fromstring(res.text)
  result = root.find('.//quoteText').text
  if root.find('.//quoteAuthor').text:
    result = result + "\n" + str(root.find('.//quoteAuthor').text)
  return result

def GetInsult():
  res = requests.get("https://evilinsult.com/generate_insult.php?lang=ru&type=json")
  data = res.json()
  return data["insult"]

def CheckDate():
  now = datetime.datetime.now()
  res = requests.get("http://numbersapi.com/" + str(now.month) + "/" + str(now.day) + "/date?json")
  data = res.json()
  return data["text"]

def GetCat():
  res = requests.get("https://aws.random.cat/meow")
  try:
    data = res.json()
    url = data["file"]
    format = url[-3:]
    if not url:
      raise JSONDecodeError
  except JSONDecodeError:
    url = "http://theoldreader.com/kittens/600/400/"
    format = "jpg"
  upload = vk_api.VkUpload(vk)
  urllib.request.urlretrieve(url, "picture." + format)
  picture = upload.photo_messages("picture." + format)
  owner_id = picture[0]['owner_id']
  photo_id = picture[0]['id']
  access_key = picture[0]['access_key']
  if "gif" in format:
    peer = message['peer_id']
    result = json.loads(requests.post(vk.docs.getMessagesUploadServer(type='doc', peer_id=peer)['upload_url'],
                                                  files={'file': open('picture.gif', 'rb')}).text)
    jsonAnswer = vk.docs.save(file=result['file'], title='title', tags=[])

    vk.messages.send(
                    peer_id=peer,
                    random_id=0,
                    attachment=f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}"
                )
  else:
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    if event.chat_id:
      vk.messages.send(
                chat_id=event.chat_id,
                random_id=get_random_id(),
                message="",
                attachment = attachment)  
    elif message['from_id']:
      vk.messages.send(
                  user_id=message['from_id'],
                  random_id=get_random_id(),
                  message="",
                  attachment = attachment)

def GetDog():
  res = requests.get("https://random.dog/woof.json")
  try:
    data = res.json()
  except JSONDecodeError:
      if event.chat_id:
          vk.messages.send(
              chat_id=event.chat_id,
              random_id=get_random_id(),
              message="Ошибка загрузки" + str(res.text))  
      elif message['from_id']:
        vk.messages.send(
                user_id=message['from_id'],
                random_id=get_random_id(),
                message="Ошибка загрузки" + str(res.text))
      return
  if "mp4" in data["url"][-3:]:
      if event.chat_id:
          vk.messages.send(
              chat_id=event.chat_id,
              random_id=get_random_id(),
              message="Ошибка загрузки")  
      elif message['from_id']:
        vk.messages.send(
                user_id=message['from_id'],
                random_id=get_random_id(),
                message="Ошибка загрузки")
      return
  upload = vk_api.VkUpload(vk)
  urllib.request.urlretrieve(data["url"], "picture." + data["url"][-3:])
  picture = upload.photo_messages("picture." + data["url"][-3:])
  owner_id = picture[0]['owner_id']
  photo_id = picture[0]['id']
  access_key = picture[0]['access_key']
  if "gif" in data["url"][-3:]:
    peer = message['peer_id']
    result = json.loads(requests.post(vk.docs.getMessagesUploadServer(type='doc', peer_id=peer)['upload_url'],
                                                  files={'file': open('picture.gif', 'rb')}).text)
    jsonAnswer = vk.docs.save(file=result['file'], title='title', tags=[])

    vk.messages.send(
                    peer_id=peer,
                    random_id=0,
                    attachment=f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}"
                )
  else:
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    if event.chat_id:
      vk.messages.send(
                chat_id=event.chat_id,
                random_id=get_random_id(),
                message="",
                attachment = attachment)  
    elif message['from_id']:
      vk.messages.send(
                  user_id=message['from_id'],
                  random_id=get_random_id(),
                  message="",
                  attachment = attachment)

def GetFox():
  res = requests.get("https://randomfox.ca/floof/")
  data = res.json()
  upload = vk_api.VkUpload(vk)
  opener = urllib.request.URLopener()
  opener.addheader('User-Agent', 'whatever')
  filename, headers = opener.retrieve(data["image"], 'picture.jpg')
  photo = upload.photo_messages("picture.jpg")
  owner_id = photo[0]['owner_id']
  photo_id = photo[0]['id']
  access_key = photo[0]['access_key']
  attachment = f'photo{owner_id}_{photo_id}_{access_key}'
  if event.chat_id:
    vk.messages.send(
              chat_id=event.chat_id,
              random_id=get_random_id(),
              message="",
              attachment = attachment)  
  elif message['from_id']:
    vk.messages.send(
                user_id=message['from_id'],
                random_id=get_random_id(),
                message="",
                attachment = attachment)

def GetNewCard():
  res = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1")
  data = res.json()
  cardId = data["deck_id"]
  res = requests.get("https://deckofcardsapi.com/api/deck/" + cardId + "/draw/?count=1")
  data = res.json()
  upload = vk_api.VkUpload(vk)
  opener = urllib.request.URLopener()
  opener.addheader('User-Agent', 'whatever')
  filename, headers = opener.retrieve(data["cards"][0]["image"], 'picture.png')
  photo = upload.photo_messages("picture.png")
  owner_id = photo[0]['owner_id']
  photo_id = photo[0]['id']
  access_key = photo[0]['access_key']
  attachment = f'photo{owner_id}_{photo_id}_{access_key}'
  if event.chat_id:
    vk.messages.send(
              chat_id=event.chat_id,
              random_id=get_random_id(),
              message="",
              attachment = attachment)  
  elif message['from_id']:
    vk.messages.send(
                user_id=message['from_id'],
                random_id=get_random_id(),
                message="",
                attachment = attachment)
  return ""

def GetCard():
  if not cardId:
    GetNewCard()
    return
  res = requests.get("https://deckofcardsapi.com/api/deck/" + cardId + "/draw/?count=1")
  data = res.json()
  upload = vk_api.VkUpload(vk)
  opener = urllib.request.URLopener()
  opener.addheader('User-Agent', 'whatever')
  filename, headers = opener.retrieve(data["cards"][0]["image"], 'picture.png')
  photo = upload.photo_messages("picture.png")
  owner_id = photo[0]['owner_id']
  photo_id = photo[0]['id']
  access_key = photo[0]['access_key']
  attachment = f'photo{owner_id}_{photo_id}_{access_key}'
  if event.chat_id:
    vk.messages.send(
              chat_id=event.chat_id,
              random_id=get_random_id(),
              message="",
              attachment = attachment)  
  elif message['from_id']:
    vk.messages.send(
                user_id=message['from_id'],
                random_id=get_random_id(),
                message="",
                attachment = attachment)
  return ""

def GetMeme(memetype):
  if memetype:
    res = requests.get("https://meme-api.herokuapp.com/gimme/" + memetype)
    data = res.json()
    if 'code' in data.keys():
      if str(event.obj.peer_id).startswith('200000000'):
        vk.messages.send(
                  chat_id=str(event.obj.peer_id)[-1],
                  random_id=get_random_id(),
                  message=data["message"]) 
      elif event.chat_id:
        vk.messages.send(
                  chat_id=event.chat_id,
                  random_id=get_random_id(),
                  message=data["message"])  
      elif message['from_id']:
        vk.messages.send(
                    user_id=message['from_id'],
                    random_id=get_random_id(),
                    message=data["message"])
    else:
      upload = vk_api.VkUpload(vk)
      opener = urllib.request.URLopener()
      opener.addheader('User-Agent', 'whatever')
      filename, headers = opener.retrieve(data["url"], 'picture.jpg')
      photo = upload.photo_messages("picture.jpg")
      owner_id = photo[0]['owner_id']
      photo_id = photo[0]['id']
      access_key = photo[0]['access_key']
      attachment = f'photo{owner_id}_{photo_id}_{access_key}'
      if str(event.obj.peer_id).startswith('200000000'):
        vk.messages.send(
                  chat_id=str(event.obj.peer_id)[-1],
                  random_id=get_random_id(),
                  message=data["title"],
                  attachment = attachment)  
      elif hasattr(event, 'chat_id') and event.chat_id:
        vk.messages.send(
                  chat_id=event.chat_id,
                  random_id=get_random_id(),
                  message=data["title"],
                  attachment = attachment)  
      elif message['from_id']:
        vk.messages.send(
                    user_id=message['from_id'],
                    random_id=get_random_id(),
                    message=data["title"],
                    attachment = attachment)
  else:
    res = requests.get("https://meme-api.herokuapp.com/gimme/1")
    data = res.json()
    upload = vk_api.VkUpload(vk)
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', 'whatever')
    filename, headers = opener.retrieve(data["memes"][0]["url"], 'picture.jpg')
    photo = upload.photo_messages("picture.jpg")
    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    if str(event.obj.peer_id).startswith('200000000'):
        vk.messages.send(
                chat_id=str(event.obj.peer_id)[-1],
                random_id=get_random_id(),
                message="",
                attachment = attachment)  
    elif hasattr(event, 'chat_id') and event.chat_id:
      vk.messages.send(
                chat_id=event.chat_id,
                random_id=get_random_id(),
                message="",
                attachment = attachment)  
    elif message['from_id']:
      vk.messages.send(
                  user_id=message['from_id'],
                  random_id=get_random_id(),
                  message="",
                  attachment = attachment)

def GetPicture(filename):
  upload = vk_api.VkUpload(vk)
  photo = upload.photo_messages(path + filename)
  owner_id = photo[0]['owner_id']
  photo_id = photo[0]['id']
  access_key = photo[0]['access_key']
  attachment = f'photo{owner_id}_{photo_id}_{access_key}'
  if event.chat_id:
    vk.messages.send(
              chat_id=event.chat_id,
              random_id=get_random_id(),
              message="",
              attachment = attachment)  
  elif message['from_id']:
    vk.messages.send(
                user_id=message['from_id'],
                random_id=get_random_id(),
                message="",
                attachment = attachment)

def GetGif(filename):
  upload = vk_api.VkUpload(vk)
  picture = upload.photo_messages(path + filename)
  owner_id = picture[0]['owner_id']
  photo_id = picture[0]['id']
  access_key = picture[0]['access_key']
  peer = message['peer_id']
  result = json.loads(requests.post(vk.docs.getMessagesUploadServer(type='doc', peer_id=peer)['upload_url'],
                                                files={'file': open(path + filename, 'rb')}).text)
  jsonAnswer = vk.docs.save(file=result['file'], title='title', tags=[])

  vk.messages.send(
                  peer_id=peer,
                  random_id=0,
                  attachment=f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}"
              )

def CheckIfTruthUnspoken():
  f = open(path + 'chatList.txt').readlines()
  for id in f:
    if int(id)<10:
      vk.messages.send(
        chat_id=int(id),
        random_id=get_random_id(),
        message="Дооооооброе утро!\n Погода на сегодня:" + request_current_weather())
    else:
      vk.messages.send(
        user_id=int(id),
        random_id=get_random_id(),
        message="Дооооооброе утро!\n Погода на сегодня:" + request_current_weather())
  time.sleep(60)

def SendUsHome():
  vk.messages.send(
    chat_id=2,
    random_id=get_random_id(),
    message="Братцы, пора домой!")
  time.sleep(60)

def GetLatestNews():
  requestText = "https://newsdata.io/api/1/news?apikey=" + newsKey + "&language=ru" + "&country=ru"
  res = requests.get(requestText)
  data = res.json()
  result = "Новости на сегодня:\n"
  for newsData in data["results"]:
    text = str(newsData["description"])
    if text:
      result = result + text.replace("Читать далее", "") + "\n____________\n"
  if not data["results"]:
    result = result + "Отсутствуют"
  return result.replace("\nNone", "")

def CheckAdminMessage(text):
  text = text.lower()
  if(not text):
    return '';
  if "информация" in text:
    if event.chat_id:
      vk.messages.send(
                chat_id=event.chat_id,
                random_id=get_random_id(),
                message=str(event.chat_id))  
    elif message['from_id']:
      vk.messages.send(
                  user_id=message['from_id'],
                  random_id=get_random_id(),
                  message=str(message['from_id']))

def getTestInput(inputMessage, wList, maxLen):
	encoderMessage = np.full((maxLen), wList.index('<pad>'), dtype='int32')
	inputSplit = inputMessage.lower().split()
	for index,word in enumerate(inputSplit):
		try:
			encoderMessage[index] = wList.index(word)
		except ValueError:
			continue
	encoderMessage[index + 1] = wList.index('<EOS>')
	encoderMessage = encoderMessage[::-1]
	encoderMessageList=[]
	for num in encoderMessage:
		encoderMessageList.append([num])
	return encoderMessageList

def idsToSentence(ids, wList):
    EOStokenIndex = wList.index('<EOS>')
    padTokenIndex = wList.index('<pad>')
    myStr = ""
    listOfResponses=[]
    for num in ids:
        if (num[0] == EOStokenIndex or num[0] == padTokenIndex):
            listOfResponses.append(myStr)
            myStr = ""
        else:
            myStr = myStr + wList[num[0]] + " "
    if myStr:
        listOfResponses.append(myStr)
    listOfResponses = [i for i in listOfResponses if i]
    listOfResponses = list(set(listOfResponses))
    chosenString = '. '.join(listOfResponses)
    #chosenString = listOfResponses[0]
    #chosenString = max(listOfResponses, key=len)
    return chosenString


def SendNotificationToTelegram():
    res = requests.get("https://api.telegram.org/" + telegramKey +" /sendMessage?chat_id=794252283&text=Сэр, вас зовут")
    print(event)
    vk.messages.send(
                chat_id=event.chat_id,
                random_id=get_random_id(),
                message="Всё ок, я его позвал")

def ChechMessage(text):
  global keyboardOn
  anonimusPhrases = {"ек макарек", "якорь мне в зад", "ешкин матрешкин", "елки иголки", "японский магнитофон", "едрить его в корень",\
                    "елы палы", "екарный бабай", "етижи пасатижи", "твою дивизию", "укуси меня пчела", "ешкин кот", "екалемене",\
                    "гвоздь мне в кеды", "ексель-моксель", "епарэсэтэ", "етишкин пистолет", "ежки-матрешки", "ядрен батон",\
                    "япона мать", "да чтоб все провалилось", "еперный театр", "едрид мадрид", "срань господня", "в рот мне ноги",\
                     "е мае", "едрена вош", "футы нуты", "блин блинский", "тысяча чертей"}
  ##Тут запихнуть доступ на сервер
  text = text.lower()
  if(not text):
    return '';
  if "выключить клавиатуру" in text:
    keyboardOn = False
    return "Прошу!"
  if "клавиатуру" in text:
    keyboardOn = True
    return "Прошу!"
  if "@ilyalyai" in text:
    SendNotificationToTelegram()
    return ""
  if "что ты умеешь" in text:
    return "Как хорошо, что вы спросили!\n Я умею определять погоду по запросу \"Че там по погоде\"\n"\
    "Могу оценивать что угодно по запросу \"Твоя оценка?\", \"Согласен?\" или \"Какова вероятность?\"\n"\
    "Могу выдать картинку дня NASA по запросу \"Хочу картинку\"\nМогу узнать информацию о сегодняшнем числе по запросу \"Проверь дату\"\n"\
    "Могу выдать цитату по запросу \"Скажи что-нибудь умное\" или оскорбить по запросу \"Оскорби\" (Второе работает по-дурацки)\n"\
    "Могу выдать рандомную карту по запросу \"Выдай карту\"\n Ну и могу выдать картинку песика, лисички, котика или вообще мем по запросу \"Дай ...\"\n"\
    "Ну и новости могу рассказать- просто упомяни \"новости\"";
  if "че там по погоде" in text:
    return request_current_weather();
  if "новости" in text or "в мире творится" in text:
    return GetLatestNews();
  if "дамы и господа!" in text:
    return "Леди и джентельмены!";
  if "сегодня и только сегодня" in text:
    return "Мы представляем вам!";
  if "поздоровайся со всеми" in text or ("скажи" in text and "привет" in text):
    if event.chat_id:
      vk.messages.send(
                chat_id=event.chat_id,
                random_id=get_random_id(),
                sticker_id = 3871)  
    elif message['from_id']:
      vk.messages.send(
                  user_id=message['from_id'],
                  random_id=get_random_id(),
                  sticker_id = 3871)
  if ("спасибо" in text and "лапочка" in text) or ("мой" in text and "хороший" in text):
    if event.chat_id:
      vk.messages.send(
                chat_id=event.chat_id,
                random_id=get_random_id(),
                sticker_id = 3892)  
    elif message['from_id']:
      vk.messages.send(
                  user_id=message['from_id'],
                  random_id=get_random_id(),
                  sticker_id = 3892)
  if "хочу картинку" in text:
    SendNasaPicture()
    return "";
  if "ты тут?" in text:
    return "А как же"
  if "оскорби" in text:
    return GetInsult()
  if "скажи" in text and "умное" in text:
    return GetQuote();
  if "дай" in text and "котика" in text:
    GetCat();
  if "really" in text:
    GetGif("rockSus.gif");
  if "реально?" in text:
    GetPicture("really.jpg");
    return "";
  if "дай" in text and "лисичку" in text:
    GetFox();
  if "дай" in text and "мем" in text:
    if "милый" in text:
      GetMeme("wholesome");
    elif not '"' in text:
      GetMeme("");
    else:
      list = text.split('"')
      GetMeme(list[1]);
  if "дай" in text and "песика" in text:
    GetDog();
  if "дай" in text and "манки" in text:
    GetPicture("monkey.jpg");
  if "проверь" in text and "дату" in text:
    return CheckDate()
  if "погода на день" in text:
    return request_day_weather();
  if "твоя оценка" in text:
    return str(random.randint(0, 10)) + " из 10";
  if "выдай карту" in text:
    GetNewCard()
  if "это твоя карта" in text or "выдай новую карту" in text:
    GetCard()
  if "вероятность этого" in text:
    return str(random.randint(0, 100)) + "%";
  if "согласен" in text:
    foo = ['Да', 'Нет', 'Ни в коем случае', 'На все сто', 'Я не буду даже рассуждать об этом']
    return random.choice(foo);
  if "включить напоминание" in text:
    f = open(path + 'chatList.txt', 'a')
    if event.chat_id:
      f.write(str(event.chat_id) + "\n")
    elif message['from_id']:
      f.write(str(message['from_id']) + "\n")
    f.flush()
    return "Готово!";
  if "отключить напоминание" in text:
    f = open(path + 'chatList.txt', 'w+')
    if event.chat_id:
      f = f.replace(str(event.chat_id) + '\n','')
    elif message['from_id']:
      f = f.replace(str(message['from_id']) + '\n','')
    f.flush()
    return "Есть!"
  for anonimusPhrase in anonimusPhrases:
    if anonimusPhrase in text.replace('ё','е'):
      pictureName = str(random.randint(1, 30))
      GetPicture("anonimus/anonimus" + pictureName + ".jpg");
      return ""
  #это когда подключу нейросеть
  '''
    if "фибли" in text or "[club181731504|@fibli]" in text:
    try:
      newText = message['text'].replace('[club181731504|@fibli]', '')
      newText = message['text'].replace('фибли, ', '')     
      res = pred(newText)
      return res;
    except JSONDecodeError:
      return ""
  '''

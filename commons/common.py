

from typing import Dict, Any, Optional


def use_config(file: str, section: str, save_config: Dict[str, Any] = {} ) -> Dict[str, Any]:
  import configparser, os
  config_path = os.path.join(os.getcwd(), file)
  config = configparser.ConfigParser()
  
  try:
    config.read(config_path, encoding='utf-8')
    if not config.has_section(section):
      config.add_section(section)
    dict_config = dict(config[section])
  except Exception as e:
    print(f"Ошибка: {e}")

  # Обновляем dict_config значениями из save_config (заменяем или добавляем новые ключи)
  if save_config:
    dict_config.update(save_config)
    for key, value in dict_config.items():
      config[section][key] = str(value)
    try:
      with open(config_path, 'w', encoding='utf-8') as f:
        config.write(f)
      return True
    except Exception:
      return False
  return dict_config # ===============
  """
  мы попробовали получить конфиг
  функция с 3 параметрами и конфиг есть, нужно сохранять, добавляем/заменяем в полученном конфиге переданный словарь
  функция с 3 параметрами и конфига нет, нужно нужно сохранять, добавляем/заменяем в полученном конфиге переданный словарь
  функция с 2 параметрами и конфиг есть, вернуть конфиг
  функция с 2 параметрами и конфига нет, вернуть false 
  """

  
async def main_auth(client, project_name: str) -> bool:
  import telethon
  from telethon import TelegramClient
  def get_input(field, value):
    if "sent_code" in field:
      while True: 
        new_value = input(f'  ❔ Введите полуенный код, 5 цифр: ').strip()
        if str(new_value) == str(value):
          print(f"  ❓ Новое значение не должно совпадать с предыдущим.")
          continue
        if not new_value.isdigit():
          print(f"  ❓ Введите только цифры.")
          continue
        if not len(new_value) == 5:
          print(f"  ❓ Введите 5 цифр.")
          continue
        break
      return int(new_value)               
    int_arr = ["api_id", "phone"]
    if field in int_arr:
      prompt = f"  ❔ {field} (состоит из цифр), текущее - [{value}] : "   
      integer = True
    else:
      integer = False
      prompt = f"  ❔ {field}, текущее - [{value}] : "   
    while True:
      new_value = input(prompt).strip()
      if new_value: # Пользователь ввел новое значение
        if integer and new_value.isdigit() or not integer:
          return new_value
      elif value:   # Пользователь нажал Enter и есть текущее значение - оставляем его
        if integer and value.isdigit() or not integer:
          return value
      else:         # Пользователь нажал Enter но нет текущего значения - запросить снова
        print(f"  ❓ Поле {field} обязательно для заполнения")
  debug = False
  print(f"⚠️ Попытка подключения к текущей сессии...")
  await client.connect()  # может быть ошибка при отсутствии интернета 
  if client.is_connected() and await client.is_user_authorized():
    print(f"  ✅ Подключение с текущим файлом сессии успешно")
  else:
    await client.disconnect() # отключаемся от сессии что бы освободить для другого экземпляра
    print(f"  ❌ Не удалось подключиться к текущей сессии")
    api_id = None
    api_hash = None
    phone = None
    password = None
    need_pass = False
    sent_code = None
    n_try = 3
    for i in range(0, n_try + 1): 
      """
        этапы авторизации, 
        1) берем id, hash, phone и делаем sign_in(phone)
        - если ошибка, то остаемся на 1 этапе и пробуем обновить/валидировать id, hash, phone
        - если Ок то получаем и сохраняем код и переходим на новый этап.
        2) берем Phone, Code и делаем sign_in(phone, code, phone_code_hash)
        - если ошибка то проблема с неверным кодом - пытаемс исправить, или требует пароль для следующего этапа
        - если Ок, то авторизация закончена и нужно запусскать клиент
        3) берем Password  и пробуем войти, 
        - если ошибка то, проверяем пароль и код
        - если ОК, то авторизация закончена и нужно запусскать клиент
        попробовать пароль ввести через 40 минут когда код будет не валидным
        
        need_pass = true - нужен пароль
        1)  not sent_code = true, not need_pass = true
        2)  sent_code = true, not need_pass = true
        3)  sent_code = true, need_pass = true
      """
      if debug: print(f"❕  Цикл, проход: {i}/{n_try}") # DEBUG
      try:
        if i == 0: # Перывй проход, пробуем получить параметры из конфига.
          config = use_config('creds.ini', project_name)
          print(f"⚠️ Попытка подключения с помощью конфига...\n  {config}")
          api_id = config.get('api_id')
          api_hash = config.get('api_hash') 
          phone = config.get('phone')
          password = config.get('password')
        # Валидация параметров.
        if not api_id or not api_id.isdigit():
          api_id = get_input("api_id", api_id)
        if not api_hash:
          api_hash = get_input("api_hash", api_hash)
        if not phone or not phone.isdigit():
          phone = get_input("phone", phone)
      except Exception as e: # Этой ошибки не должно возникнуть
        print(f"  ⁉️ Error type: {type(e)}")
        print(f"  ❓ - Error: {e}")
        pass    
      if debug: print(f"❕  check client_tmp.connect() and dell") # DEBUG
      try:
        if client_tmp.is_connected(): 
          await client_tmp.disconnect()
          del client_tmp
      except:
        pass
        if debug: print(f"❕  check client_tmp.connect() and dell except") # DEBUG
      try:
        if debug: print(f"❕  client_tmp.connect()") # DEBUG
        if i >= 1: print(f"⚠️  Попытка: {i}/{n_try}")
        client_tmp = TelegramClient(project_name, api_id, api_hash)
        await client_tmp.connect() 
      except ValueError as e:
          # Этой ошибки не должно возникнуть т.к. валидация выполняется в функции
          print(f"  ‼️ Ошибка API ID и Hash:\n    - {e}")
          #api_id = int(get_input("api_id", api_id)) # api id установили выше
          #api_hash = get_input("api_hash", api_hash)
          continue
      except ConnectionError as e:
        print(f"  ‼️ Проверьте ваше интернет-соединение. Ошибка подключения к сети:\n{e}")
        return
      except Exception as e: # Этой ошибки не должно возникнуть
        print(f"  ⁉️ Error type: {type(e)}")
        print(f"  ❓ - Error: {e}")
        pass      
      if debug: print(f"❕  client_tmp.sign_in()") # DEBUG  
      try:            
        if not sent_code:       # await client_tmp.send_code_request(phone, force_sms=True)
          if debug: print(f"❕  sent_code") # DEBUG
          sent_code_obj = await client_tmp.sign_in(phone) # SentCode(type=SentCodeTypeApp(length=5), phone_code_hash='58aa1e1ac7808df17e', next_type=None, timeout=None)
          sent_code = get_input("sent_code", sent_code)
        if not need_pass: # выбило ошибку на запрос пароля, не запрашиваем повторно код
          if debug: print(f"❕  client_tmp.sign_in(phone, sent_code)") # DEBUG 
          await client_tmp.sign_in(phone=phone, code=sent_code, phone_code_hash=sent_code_obj.phone_code_hash) # Возможно стоит делать в другом блоке, т.к. если нужен пароль то будет еще его обработка
      # ✅ Обработка валидноссти api_id/api_hash
      except telethon.errors.rpcerrorlist.ApiIdInvalidError as e:
        # The api_id/api_hash combination is invalid (caused by SendCodeRequest)
        print(f"  ‼️ Ваш API ID или API Hash неверны.\n    - {e}")
        api_id = get_input("api_id", api_id)
        api_hash = get_input("api_hash", api_hash)
        continue
      except telethon.errors.rpcerrorlist.ApiIdPublishedFloodError as e:
        print(f"  ‼️ Ваш API ID или API Hash отозваны.\n    - {e}")
        api_id = int(get_input("api_id", api_id))
        api_hash = get_input("api_hash", api_hash)
        continue
      # ✅ Обраотка отправки кода
      except telethon.errors.rpcerrorlist.SendCodeUnavailableError as e:
        print(f"  ‼️ Ошибка отправки кода для авторизации\n    - {e}")
        return
      except telethon.errors.rpcerrorlist.PhoneCodeExpiredError as e: # Нужен новый код
        print(f"  ‼️ Истек срок действия кода.:\n    - {e}")
        sent_code = None # нужен запрос нового кода
        continue
      except telethon.errors.rpcerrorlist.PhoneCodeInvalidError as e: # Нужен новый код 
        print(f"  ‼️ Неверный код авторизации:\n    - {e}")
        sent_code = get_input("sent_code", sent_code) # здесь надо новый код просить
        continue
      # ✅ Обработка ошибок с номером телефона
      except telethon.errors.rpcerrorlist.PhoneNumberBannedError as e:
        print(f"  ‼️ Номер телефона '{phone}' заблокирован в Telegram.\n    - {e}")
        phone = None
        continue
      except telethon.errors.rpcerrorlist.PhoneNumberInvalidError as e:
        print(f"  ‼️ Не верный phone number\n    - {e}")
        phone = None
        #phone = int(get_input("phone", phone))
        continue
      except telethon.errors.rpcerrorlist.PhoneNumberUnoccupiedError as e:
        print(f"  ‼️ Указанный номер телефона не зарегистрирован в Telegram:\n    - {e}")
        phone = None
        continue
      except telethon.errors.rpcerrorlist.AuthKeyUnregisteredError as e: # в клиенте отключена сессия
        return
      # ✅ флуд обработка
      except telethon.errors.rpcerrorlist.FloodWaitError as e:
        print(f"  ‼️ Ошибка: Слишком много попыток. Пожалуйста, подождите {e.seconds} секунд и попробуйте снова:\n    - {e}")
        return
      # ✅ авотризация с паролем
      except telethon.errors.rpcerrorlist.SessionPasswordNeededError as e:
        print(f"  ‼️ Требуется двухфакторная аутентификация (2FA):\n    - {e}")
        need_pass = True # пропускаем запрос кода для авторизации 
      except Exception as e:
        print(f"  ⁉️ Error type: {type(e)}")
        print(f"  ❓ - Error: {e}")      
      if need_pass:
        if not password: password = get_input("password", password)
        if debug: print(f"❕  3) client_tmp.sign_in(password={password})") # DEBUG  # проверка с паролем
        try: # Обработка для ввода пароля 
          await client_tmp.sign_in(password=password)
          print("  ✅ Успешный вход с паролем 2FA!")
        except telethon.errors.rpcerrorlist.PasswordHashInvalidError as e:
          print(f"  ‼️ Ошибка: Введен неверный пароль 2FA.\n    - {e}")
          if i < n_try: password = get_input("password", password) # на последнеим круге не спрашивать, т.к. мы уже находимся после авторизации 
          #await client.disconnect() # ИИ говорит что это обязательно
        except Exception as e:
          print(f"  ‼️ Ошибка 2FA type: [{type(e)}]:\n    - {e}")
          if i < n_try: password = get_input("password", password) # на последнеим круге не спрашивать, т.к. мы уже находимся после авторизации 
          #await client.disconnect() # ИИ говорит что это обязательно
          continue
      # Далее логика авторизации, если подключение успешно
      if client_tmp.is_connected() and await client_tmp.is_user_authorized():
        if i == 0: # С первого раза подключились параметрами из файла
          print(f"✅ Авторизация конфигом успешна")
        else:
          print(f"✅ Авторизация введеных данных успешна")   
        # Наэтом этапе делать реконект  
        if debug: print(f"Проверка покдлючения клиентов")
        if debug and client_tmp.is_connected(): print(f"❕  client_tmp.is_connected") # DEBUG
        if debug and client.is_connected(): print(f"❕  client.is_connected") # DEBUG 
        # Делаем reconnect для запуска первого клиента на котором висят декораторы.
        await client_tmp.disconnect() # Отключаемся от сессии
        del client_tmp # Удаляем экземпляр
        await client.connect() # Подключаем клиент который должен работать
        # здесь нужно сохранить данные успешной авторизации в файл ессли они изменились
        new_config = {'api_id': api_id, 'api_hash': api_hash} 
        # new_config = {'api_id': api_id, 'api_hash': api_hash, 'phone': phone, 'password': password}
        #if password: new_config['password'] = password      
        if new_config == config:
          print(f"  ✅ config не изменился")
        else: # конфиг изменился, сохранить данные в файл
          if use_config('creds.ini', project_name, new_config):  
            print(f"  ✅ данные записаны в файл")
          else:
            print(f"  ❌ Неудалось записать в файл")      
        break # Выход из цикла, авторизация успешна.
  if debug: # DEBUG
    print(f"❕  Здесь должен остаться подключенным только client")
    try:
      # Не должно быть, может бить при неудачных вводах, но клиент не запуститься и код закончится.
      if client_tmp.is_connected(): print(f"❕  client_tmp.is_connected") # DEBUG
    except:
      print(f"❕  client_tmp.is_connected - error") # DEBUG
    finally:
      if client.is_connected(): print(f"❕  client.is_connected") # DEBUG
  if client.is_connected() and await client.is_user_authorized(): # если client подключен, запустить парсинг сообщений, если не подключен - выйти
    client_auth = await client.get_me()
    print(f"📜 Подключен как: [@{client_auth.username}] {client_auth.first_name} {client_auth.last_name}")
    await client.run_until_disconnected()
  else:
    print("❌ Не удалось подключиться, попробуйте снова")
    return
  
   
def debug(event, event_type='new', debug_set=[], reply_markup=None):
  print(f"--------------------------------{event_type}--------------------------------------------")
  print(debug_set)
  line = []
  if 'sender' in debug_set: 
    if event.sender is not None:
      line.append(event.sender.id) 
    elif event.from_id is not None:
      line.append(event.from_id.user_id) 
    else:
      line.append('00000000') 
  if 'id' in debug_set:
    line.append(event.id)
  if 'date' in debug_set:
    line.append(event.date)
  if line:
    print('|'.join(str(x) for x in line))
  if 'text' in debug_set:
    #print('--------------------------------text--------------------------------------------')
    print(event.text)  
  if 'buttons' in debug_set:
    if event.buttons and type(event.reply_markup).__name__ == 'ReplyInlineMarkup':
      print('==========================ReplyInlineMarkup=====================================')
      for row in event.buttons:
        for button in row:
          print(f"[{button.text}]", end=' ')
        print('')
    if reply_markup:
      print('++++++++++++++++++++++++++ReplyKeyboardMarkup+++++++++++++++++++++++++++++++++++')
      for row in reply_markup:
        for button in row:
          print(f"[{button.text}]", end=' ')
        print('')
    print('--------------------------------------------------------------------------------')
  if 'buttons_raw' in debug_set and event.buttons:
    for row in event.reply_markup.rows:
      for button in row.buttons:
        print(button)
      print('---')
  if 'raw' in debug_set:
    print(event)
  if False: # Пример работы с датой
    date_ts = int(event.date.timestamp())
    date_norm = str(event.date.fromtimestamp(date_ts))
  #print('----------------------------end debug-------------------------------------------')
  DEFAULT_SETS = {
    'default_debug': [
      'sender',
      'id',
      'date',
      'text',
      'buttons',
      'buttons_raw', 
      'raw'
    ],
    'default_reply_markup': None,
    'default_chats': [93372553] # bot father
  }
  return


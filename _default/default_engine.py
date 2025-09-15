import asyncio
try:  # Попытка импортировать реальные функции из модуля
  from commons.common import debug, use_config, main_auth
  print("✅ Успешный импорт функций из 'commons'")
except ImportError as e:
  # Если импорт не удался, создаем функции-заглушки
  print(f" ‼️ Ошибка импорта: {e}. Создаем функции-заглушки.")
  def debug(*args, **kwargs): print("debug(emty)")
  def use_config(*args, **kwargs): return False
  async def main_auth(*args, **kwargs): return False

project_name = '_default'
if True: # Получаем настройки для debug
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
  default_sets = use_config('debug.ini', project_name)
  if not default_sets:
    # конфиг не получен, записать новый
    use_config('debug.ini', project_name, DEFAULT_SETS )
    default_sets = DEFAULT_SETS
  import ast # Конвертация строки в список, если нужно
  if isinstance(default_sets['default_chats'], str):
    default_sets['default_chats'] = ast.literal_eval(default_sets['default_chats'])
  default_reply_markup = default_sets['default_reply_markup']


async def default_engine(event, event_type='new'):  
  """Нижние кнопки"""
  def down_keyboard(event, default_reply_markup):
    if event.reply_markup:
      types = {
        'ReplyKeyboardMarkup': event.buttons,
        'ReplyKeyboardHide': None, 
        'replyKeyboardForceReply': None,
        'ReplyInlineMarkup': default_reply_markup
      }
      return types[type(event.reply_markup).__name__]
    return default_reply_markup
  global default_reply_markup 
  default_reply_markup = down_keyboard(event, default_reply_markup) # держит в переменной default_reply_markup, актуальные нижние кнопки  
  """Дебаг чата"""
  debug(event, event_type, default_sets.get('default_debug', []), default_reply_markup)# событие, тип (новое, редактированое, колбак...), настройки, нижние кнопки
  """Выполнение кода"""
  pass
  """END"""




  
if True: # Получаем настройки для telethon и делаем авторизацию:
  import platform, telethon
  system_version=f"{platform.uname().version}-{platform.uname().system}"
  device_model=f"{platform.uname().machine}{project_name}"
  app_version=telethon.__version__
from telethon import TelegramClient, events
client = TelegramClient(project_name, '1', '1', 
  system_version=system_version, 
  device_model=device_model, 
  app_version=app_version
  )


@client.on(events.NewMessage(chats = default_sets['default_chats'])) # from_users=
async def default_new_mess_from(event):
  await default_engine(event, 'new')
@client.on(events.MessageEdited(chats = default_sets['default_chats'])) # from_users=
async def default_edit_mess_from(event):
  await default_engine(event, 'edit')


if __name__ == "__main__":
  try:
    asyncio.run(main_auth(client, project_name))
  except KeyboardInterrupt:
    print("\n⏹️  Остановка по Ctrl+C")
  except Exception as e:
    print(type(e))
    print(f"!!! {e}")






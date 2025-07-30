from telethon import TelegramClient, events
# Общие настройки
client = TelegramClient(
  '_autonomous',
  api_id = 12456789,                              # Вставить свои данные.
  api_hash = 'ddddd55555eeeee666666fffff777770',  # Вставить свои данные.
  system_version='4.12.30-xCUSTOM',
  device_model='MyDeviceModel1',
  app_version='2.0.0'
)

default_sets = {
  'default_debug': [
    'sender',
    'id',
    'date',
  ],
  'default_reply_markup': None,
  'default_chats': [93372553]
}
default_reply_markup = default_sets['default_reply_markup']

 
""" @BotFather
  /mybots - inline_markup
  /newbot - remove_markup
  /newapp - reply_markup
  # from_users=
"""

  
@client.on(events.NewMessage(chats = default_sets['default_chats'])) 
async def default_new_mess_from(event):
  await default_engine(event, 'new')
@client.on(events.MessageEdited(chats = default_sets['default_chats']))
async def default_edit_mess_from(event):
  await default_engine(event, 'edit')


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
  
  debug(event, event_type, default_sets.get('default_debug', []), default_reply_markup)# событие, тип (новое, редактированое, колбак...), настройки, нижние кнопки
  """Code"""
  
  """END"""
  
  
def debug(event, event_type='new', debug_set=[], reply_markup=None):
  print(f"--------------------------------{event_type}--------------------------------------------")
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
  if True:
    date_ts = int(event.date.timestamp())
    date_norm = str(event.date.fromtimestamp(date_ts))
  #print('----------------------------end debug-------------------------------------------')
  return
  

if __name__ == "__main__":
  #async def conn_client():
  #  await client.connect()
  #  await client.run_until_disconnected()
  #import asyncio
  #asyncio.run(conn_client())
  client.start()
  print(f"📜 Подключен как: _autonomous")
  client.run_until_disconnected()


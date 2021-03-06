import telebot
import requests

api_tele='YOUR TELEGRAM BOT API'
bot =telebot.TeleBot(api_tele)

stats=[
            ("hi", "hey!"),
            ("apa yang bisa bot ini lakukan?", "Bot ini bisa mengubah text bahasa indonesia menjadi voice dalam bahasa inggris dan juga dapat mengubah voice dalam bahasa inggris menjadi text dalam bahasa indonesia"),
            ("apa yg bisa kamu lakukan?", "Bot ini bisa mengubah text bahasa indonesia menjadi voice dalam bahasa inggris dan juga dapat mengubah voice dalam bahasa inggris menjadi text dalam bahasa indonesia")
]

def getResponse(input):
    for stat in stats:
        if input.text.lower() == stat[0]:
            return stat[1]
    else:    
        tts(input)
        return "ini hasil translate nya."
    # return "Saya tidak mengerti apa yang anda maksud"

@bot.message_handler(func=lambda message: message.entities == None)
def post(message):
    id = message.chat.id
    input = message

    bot_output = getResponse(input)

    url = "https://api.telegram.org/bot1123336681:AAHRtAKrXBx5znWDgafdHtHLdVoVMhlx9kM/sendMessage"

    r = requests.post(url =url, params = {'chat_id': id, 'text': bot_output})
    rj = r.json()

def to_audio(text):
    print('start tts')
    somestr = '{"text":'
    b = somestr+'"'+text+'"'+'}'
    r = requests.post(url = 'https://api.jp-tok.text-to-speech.watson.cloud.ibm.com/instances/a004e258-6b11-474b-b2d0-220b544a86cf/v1/synthesize?voice=en-US_LisaV3Voice', auth = ('apikey', 'AmRMHRsrnuuARxZmHWLFn876io_-w7akmzV63TYwDYdB'), headers = {"Content-Type" : "application/json", "Accept" : "audio/ogg"}, data = b, stream = True)
    
    with open('filetts.ogg', 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    print('tts success')

def to_text(fileloc):
    print('start stt')
    b = open(fileloc, 'rb')
    r = requests.post(url = 'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/8115af27-42c1-4625-842d-84191965429e/v1/recognize', auth = ('apikey','wSYCk7wMGyom-5SGeeBXwbj7x0hfPUrbXJSzrfelhkQp'), headers = {"Content-Type": "audio/ogg"}, data = b)
    rj = r.json()
    a=[]
    c=""
    for i in rj['results']:
        a.append (i['alternatives'][0]['transcript'])
    for i in a:
        c+=i
    print('stt success')
    return c

def translateid(text):
    print('start tid')
    somestr = '{"text":'
    b = somestr+'["'+text+'"]'+',"model_id":"id-en"'+'}'
    r = requests.post(url = 'https://api.jp-tok.language-translator.watson.cloud.ibm.com/instances/b6c85ded-6ffb-48a6-b2d1-20faecaefb33/v3/translate?version=2018-05-01', auth = ('apikey', 'J9XNdjEYMmLsgSmwzC9Z5RrLvtYx9BpREdF4xeiZLW-z'), headers = {"Content-Type": "application/json"}, data = b)    
    rj = r.json()
    print('tid success')
    print (rj['translations'][0]['translation'])

    return (rj['translations'][0]['translation'])
    

def translateen(text):
    somestr = '{"text":'
    b = somestr+'["'+text+'"]'+',"model_id":"en-id"'+'}'
    r = requests.post(url = 'https://api.jp-tok.language-translator.watson.cloud.ibm.com/instances/b6c85ded-6ffb-48a6-b2d1-20faecaefb33/v3/translate?version=2018-05-01', auth = ('apikey', 'J9XNdjEYMmLsgSmwzC9Z5RrLvtYx9BpREdF4xeiZLW-z'), headers = {"Content-Type": "application/json"}, data = b)    
    rj = r.json()
    print('ted success')
    print (rj['translations'][0]['translation'])

    return (rj['translations'][0]['translation'])
    

# @bot.message_handler(content_types=['text'])
def tts(message):
    print('handler tts')
    text = message.text
    id = message.chat.id
    
    text = text[5:]
    print('translate text')
    sentence = translateid(text)
    print('convert text to voice')
    to_audio(sentence)
    c = open('filetts.ogg', 'rb')
    bot.send_voice(chat_id = id, voice = c, reply_to_message_id= message.message_id)
    print('voice sended')

@bot.message_handler(content_types=['voice'])
def stt(message):
    print('handler stt')
    file_ids = bot.get_file(message.voice.file_id)
    df = bot.download_file(file_ids.file_path)
    with open('filestt.ogg', 'wb') as new_file:
        new_file.write(df)
    print('file downloaded')
    print('convert voice to text')
    sentence = to_text('filestt.ogg')
    print('translate texzt')
    sentence_trans = translateen(sentence)
    bot.reply_to(message, sentence_trans)
    print('text sended')


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, '''
Selamat datang di cbapi_18081010071_bot
Apa yang bisa saya lakukan?
    ''')

bot.polling()


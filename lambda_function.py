#lambda_funktion.py
 
import requests
import json
import os
import urllib.request
import datetime
import dict
import random
 
TOKEN = os.getenv('TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
url = "https://blockchain.info/ticker"
url2 = "https://www.satochi.co/latest-block"
 
        
def btc_price():
    rawdata = urllib.request.urlopen(url)
    data = rawdata.read()
    data = data[21:28]
    data = "The price of one Bitcoin is " + data.decode("utf-8") + "$"
    return data
    
def btc_block():
    req = urllib.request.Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
    data = urllib.request.urlopen(req).read()
    data = "The latest mined block on the Bitcoin-Blockchain is Block: " + data.decode("utf-8")
    return data
    
def random_fact():
    return random.choice(list(dict.dict.values()))
    
 
def is_callback(button_dict):
    if 'callback_query' in button_dict:
        return True
        
        
def lambda_handler(event, context):
    try:
 
        data = json.loads(event["body"])
        
        #prozedur wenn ein button gedrueckt wurde
        if is_callback(data) == True:
            message = str(data["callback_query"]["message"]["text"])
            first_name = data["callback_query"]["message"]["chat"]["first_name"]
            chat_id = data["callback_query"]["message"]["chat"]["id"]
            callback_data = data["callback_query"]["data"]
            
            if callback_data == "/price":
                t1 = btc_price()
                requests.post(f"{BASE_URL}/sendMessage?chat_id={str(chat_id)}&text={t1}")
            
            elif callback_data == "/block":
                t1 = btc_block()
                requests.post(f"{BASE_URL}/sendMessage?chat_id={str(chat_id)}&text={t1}")
                
            elif callback_data == "/random_fact":
                t1 = random_fact()
                requests.post(f"{BASE_URL}/sendMessage?chat_id={str(chat_id)}&text={t1}")
        
        # wenn kein button gedrueckt wurde       
        else : 
            message = str(data["message"]["text"])
            first_name = data["message"]["chat"]["first_name"]
            chat_id = data["message"]["chat"]["id"]
            response = {"chat_id": chat_id, }
 
            # Reagiere auf die Eingabe
            # Fallunterscheidung
            if message.startswith('/start'):
                response['text'] = f"""Hey {first_name}, nice to see you!
Try /buttons to explore my functions.""".encode("utf8")
                requests.post(f"{BASE_URL}/sendMessage", response)
    
            elif message.startswith('/price'):
                response['text'] = btc_price()
                requests.post(f"{BASE_URL}/sendMessage", response)
            
            elif message.startswith('/block'):
                response['text'] = btc_block()
                requests.post(f"{BASE_URL}/sendMessage", response)
                
            elif message.startswith('/time'):
                response['text'] = str(datetime.datetime.now())[10:16] +" Uhr"
                requests.post(f"{BASE_URL}/sendMessage", response)
                
            elif message.startswith('/date'):
                response['text'] = datetime.datetime.now().strftime("%d.%m.%Y")
                requests.post(f"{BASE_URL}/sendMessage", response)
            
            #random facts aus dem dict
            elif message.startswith('/random_fact'):
                response['text'] = random_fact()
                requests.post(f"{BASE_URL}/sendMessage", response)
                
            #hole fragen aus dem dictonary
            elif message in dict.dict:
                response['text'] = dict.dict[message]
                requests.post(f"{BASE_URL}/sendMessage", response)
                
            #easter eggs
            elif message in dict.eastereggs:
                response['text'] = dict.eastereggs[message]
                requests.post(f"{BASE_URL}/sendMessage", response)
            
            #butt
            elif message.startswith('/buttons'):
                button1_dict = {'text' : "/price", 'callback_data':'/price'}
                button2_dict = {'text' : "/block", 'callback_data':'/block'}
                button3_dict = {'text' : "/random_fact",'callback_data':'/random_fact'}
                button_array = {'inline_keyboard': [[button1_dict,button2_dict], [button3_dict]]}
                but_text = "Here some of my most important functions."
                requests.post(f"{BASE_URL}/sendMessage?chat_id={str(chat_id)}&reply_markup={json.dumps(button_array)}&text={but_text}")
            
            # Hier können jetzt noch weitere Kommandos eingetragen werden
    
            else:
                response['text'] = f"""{first_name}, try /start, /buttons, /price, /block, or /random_fact.
                You can also ask questions, e.g. 'what is bitcoin?'""".encode("utf8")
                requests.post(f"{BASE_URL}/sendMessage", response)
 
    except Exception as e:
        print(e)
 
    return {"statusCode": 200}

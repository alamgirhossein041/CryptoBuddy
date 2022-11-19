from concurrent.futures import process
from django.http import HttpResponse
from django.shortcuts import render
from binance.spot import Spot
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
from sympy import round_two
from Report.models import listOfCoins
import json, requests
import pandas as pd



#from django.http import HttpResponse
# Create your views here.
API_KEY=''
API_SECRET=''

client = Spot(API_KEY,API_SECRET)
#client.API_URL = 'https://testnet.binance.vision/api'
#def home(request):
#    return render(request ,"Report/index.html")

def dashboard(request):
    return render(request,"Report/dashboard.html")

def temp(request):
    return render(request,"Report/temp.html")

def wallet(request):
    return render(request,"Report/wallet.html")

def tax(request):
    return render(request,"Report/tax.html")

def news(request):
    return render(request,"Report/crypto_news.html")

def history(request,coin_name=None):
    candlesticks=client.klines(coin_name+"USDT","1m")
    #candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "1 Aug, 2022", "3 Jul, 2022")
    processed_candlesticks = []

    for data in candlesticks:
        candlestick = { 
            "time": (data[0] / 1000)+19800, 
            "open": data[1],
            "high": data[2], 
            "low": data[3], 
            "close": data[4]
        }
        processed_candlesticks.append(candlestick)
    
    return JsonResponse(processed_candlesticks,safe=False)
    #return HttpResponse('<h1>Hello world</h1>')
def list_of_coins(request):
    info = client.account_snapshot("SPOT")
    info=info["snapshotVos"][2]["data"]["balances"]
    processed_info=[]
    for data in info:
        processed_info.append(data["asset"])
        #modelObject=listOfCoins(coinName=data["asset"],priceUSD=0.0)
        #modelObject.save()
    return JsonResponse(processed_info,safe=False)

def prices():
    processed_info=list(listOfCoins.objects.values())
    info=[]
    print(len(processed_info))
    for data in processed_info:
        try:
            price=client.ticker_price(data["coinName"]+"USDT")["price"]
            info.append({"coinName":data["coinName"],"price":price})
        except:
            try:
                price=client.ticker_price(data["coinName"])["price"]
                info.append({"coinName":data["coinName"],"price":price})
            except:
                #print(data["coinName"])
                continue
    return info

def test(request):
    trades = client.asset_dividend_record()
    #trades=client.exchange_info()
    #trades=[]
    #exchange_info = client.exchange_info()
    #for s in exchange_info['symbols']:
    #    trades.append(s['symbol'])
    return JsonResponse(trades,safe=False)
    
def balances(request):
    info = client.account_snapshot("SPOT")["snapshotVos"][-2]["data"]["balances"]
    #info=info["snapshotVos"][2]["data"]["balances"]
    #trades = client.get_orders(symbol='BNB')
    #print(trades)
    processed_info=[]
    for i in range(0,len(info)):
        data=info[i]
        if(float(data["free"])>0):
            try:
                data["value"]=float(data["free"])*float(client.ticker_price(data["asset"]+"USDT")["price"])
            except:
                data["value"]=-1
            try:
                data["original_Price"]=float(client.my_trades(symbol=data["asset"]+"USDT")[0]["price"])
                data["bought_Price"]=float(data["free"])*float(data["original_Price"])
                data["ROI"]=round(((data["value"]-data["bought_Price"])/data["bought_Price"])*100,2)
                
            except:
                data["original_Price"]=0
                data["bought_Price"]=0
                data["ROI"]=round(((data["value"]-data["bought_Price"]))*100,2)
            #print(i,data)
            #price=(lambda x:client.ticker_price(x+"USDT")["price"])(data["asset"])
            #for price in price_of_coins:
            #    if(price["coinName"]==data["asset"]):
            #        data["value"]=float(data["free"])*float(price["price"])
            #        break
            #    else:
            #        data["value"]=-1
            processed_info.append(data)
    #print(processed_info)
    #return JsonResponse({"1":str(type(info))},safe=False)
    return JsonResponse(processed_info,safe=False)


def marketCap(request):
    market_cap__url="https://coinmarketcap.com/"
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
    try:
        page=requests.get(market_cap__url,headers=header)
        doc = BeautifulSoup(page.content, 'html.parser')
        coin_list = doc.find_all('tr')
        coin_list=list(coin_list)
    except:
        coin_list=[]
    return JsonResponse(str(coin_list[:11]),safe=False)



def bestCryptos(request):
    market_cap__url="https://coinmarketcap.com/best-cryptos/"
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
    try:
        page=requests.get(market_cap__url,headers=header)
        doc = BeautifulSoup(page.content, 'html.parser')
        coin_list = doc.find_all('tr')
        coin_list=list(coin_list)
        list_of_coins=[]
        list_of_coins.append(str(coin_list[:11]))
        list_of_coins.append(str(coin_list[11:22]))
        list_of_coins.append(str(coin_list[22:33]))
        list_of_coins.append(str(coin_list[33:44]))
        list_of_coins.append(str(coin_list[44:55]))
    except:
        coin_list=[]
    return JsonResponse(list_of_coins,safe=False)

def exchanges(request):
    market_cap__url="https://coinmarketcap.com/rankings/exchanges/"
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
    try:
        page=requests.get(market_cap__url,headers=header)
        doc = BeautifulSoup(page.content, 'html.parser')
        coin_list = doc.find_all('tr')
        coin_list=list(coin_list)
    except:
        coin_list=[]
    return JsonResponse(str(coin_list[:11]),safe=False)


def crypto_news(request):
    crypto_news_url="https://economictimes.indiatimes.com/newslist/82519373.cms"
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
    try:
        page=requests.get(crypto_news_url,headers=header)
        doc = BeautifulSoup(page.content, 'html.parser')
        selection_class= "eachStory"
        news_list = doc.find_all('div',{'class':selection_class})
        #news_list=list(news_list)
    except:
        news_list=[]
    return JsonResponse(str(news_list),safe=False)

def price_recommend(request):

    base_url = "https://api.gemini.com/v1"
    info=prices()

    response = requests.get(base_url + "/symbols/details/BTCUSD")
    symbols = response.json()

    base_url = "https://api.gemini.com/v2"
    response = requests.get(base_url + "/ticker/btcusd")
    btc_data = response.json()
    print(btc_data["close"])
    return JsonResponse(btc_data,safe=False)

    
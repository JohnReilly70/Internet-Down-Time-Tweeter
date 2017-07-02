import socket
import logging 
import datetime
import time
from TwitterAPI import TwitterAPI

logging.basicConfig(filename='InternetDowntime.log',level=logging.CRITICAL)

def internet_connection():

    
    addresses = ["www.bbc.co.uk","www.google.co.uk",
                 "www.virginmedia.com","www.youtube.com"]
    unreachable = 0
    
    for address in addresses:
        try:
            host = socket.gethostbyname(address)
            s = socket.create_connection((host,80), 2)
        except:
            unreachable += 1
            
  
    logging.debug("\nUnreachable Websites:{}".format(unreachable))
    if unreachable == len(addresses):
        return False
    return True


def tweeting(time_delta):


    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    ACCESS_TOKEN_KEY = ''
    ACCESS_TOKEN_SECRET = ''
    api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

    tweet_text = 'virginmedia Why has my internet been down for'

    if time_delta.hour == 1:
        tweet_text += ' 1 hour'
    elif time_delta.hour > 1:
        tweet_text += ' {} hours'.format(time_delta.hour)

    if time_delta.minute == 1:
        tweet_text += ' 1 minute'
    elif time_delta.minute > 1:
        tweet_text += ' {} minutes'.format(time_delta.minute)

    r = api.request('statuses/update',
                    {'status': tweet_text})

    print(r.status_code)

def main():


    previous_connection = True
    cycle = 0

    while True:
        cycle += 1

        if not internet_connection() and previous_connection:
            logging.info("Disconnected")
            start_time = datetime.datetime.now()
            previous_connection = False

        elif internet_connection() and not previous_connection:
            logging.info("Reconnected")
            stop_time = datetime.datetime.now()
            time_delta = stop_time - start_time
            logging.info("\nTime Delta of Down Time: {}".format(time_delta))
            previous_connection = True
            tweeting(time_delta)



        time.sleep(60) #only state hours and minutes in tweet!!
        logging.info("\nCycle:{}\nTIME: {}\nint con: {}\nprev con: {}".format(cycle,datetime.datetime.now(),internet_connection(),previous_connection))


if __name__ == "__main__":
    main()









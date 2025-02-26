
import google.generativeai as genai
import textwrap
import re
import sys
import time
import threading
import logging
import os
from dotenv import load_dotenv
import click

load_dotenv()

api_key=os.getenv("APIKEY")

def loader():
        dot_count = 0
        while not done:
            sys.stdout.write(f'\r{" "*20}')
            sys.stdout.write(f'\rthinking 🤔 {dots[dot_count]}')
            sys.stdout.flush()
            dot_count = (dot_count + 1) % len(dots)
            time.sleep(0.5)

# def exitloader():
#         dot_count = 0
#         while not done:
#             sys.stdout.write(f'\r{" "*20}')
#             sys.stdout.write(f'\r Exiting 🙏 {dots[dot_count]}')
#             sys.stdout.flush()
#             dot_count = (dot_count + 1) % len(dots)
#             time.sleep(0.5)

done = False
dots = ['.', '..', '...']
color='cyan'

logging.basicConfig(
    filename="chatlog.txt",
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
)

def color_text(text,color):
    colors={
        'red': '\033[31m',
        'cyan':'\033[36m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'reset': '\033[0m',
        }
    return  f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"



def start_chat():

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    chat = model.start_chat(history=[])


    while True:
        try:
            userpromt=input("You: ")

            if userpromt.lower()=="exit":
                    print("exiting...")
                    break

            logging.info(f'User: {userpromt}')
            global done
            done=False
            laoding=threading.Thread(target=loader)
            laoding.start()

            # exiting=threading.Thread(target=exitloader)
            # exiting.daemon=True

            respone=chat.send_message(userpromt)
            done=True
            laoding.join()

            formattedres=re.sub(r'\n','\n',respone.text)
            formattedres = formattedres.replace("**", "\033[1m").replace("__", "\033[0m")
            formattedres = formattedres.replace("*", "\033[3m").replace("_", "\033[0m")
            formattedres=color_text(formattedres,color)
            formattedres=textwrap.fill(formattedres,width=120)
            logging.info(f'AI : {respone.text.strip()}')
            done=False
            print('\n',formattedres)
            laoding.join()
        except KeyboardInterrupt:
            print("/Exiting chat...")
            break
        except Exception as e:
            print("Exiting...")
            # exiting.start()
            logging.info(f'Error : {e}')

@click.command()
def main():
    start_chat()

if __name__=='__main__':
    main()

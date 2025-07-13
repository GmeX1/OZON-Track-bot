from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN', '')
TRACK_ID = os.getenv('TRACK_ID', '')
TG_ID = os.getenv('TG_ID', '')

import os
from dotenv import load_dotenv

load_dotenv('./.env')

open_api_config = {
    'key': os.environ.get('OPEN_API_KEY'),
    'org': os.environ.get('OPEN_API_ORG'),
    'endpoint': 'https://api.openai.com/v1'
}

line_config = {
    'token': os.environ.get('LINE_ACCESS_TOKEN'),
    'secret': os.environ.get('LINE_SECRET')
}

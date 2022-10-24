from typing import List, Dict, Union

from django.conf import settings


def validate_ticker_name(ticker: str) -> bool:
    return ticker in settings.POLYGON_TICKERS


def get_ticker(messages: List[Dict[str, Union[str, int, float]]]) -> str:
    return f'{messages[0].get("ev")}.{messages[0].get("pair")}'


def get_messages(messages: List[Dict[str, Union[str, int, float]]]) -> List[Dict[str, Union[str, float]]]:
    if messages[0]['ev'] in [ticker.split('.')[0] for ticker in settings.POLYGON_TICKERS]:
        return [
            {"name": ''.join(message['pair'].split('-')), 'bid': message['bp'], 'ask': message['ap']}
            for message in messages
        ]
    else:
        return messages

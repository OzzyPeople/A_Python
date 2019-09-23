import pytest

from datetime import datetime

from protocol import make_400



ACTION = ''
CODE = 400
TIME = datetime.now().timestamp()
DATA = 'some client data'

#имитация неправильного ответа
REQUEST = {
    'action': ACTION,
    'time': TIME,
    'data': 'some client data'
}

def test_action_make_400():
    response = make_400(REQUEST, data=DATA, date=TIME)
    action = response.get('code')
    assert action == CODE
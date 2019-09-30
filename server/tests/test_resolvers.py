import pytest

from resolvers import find_server_action

ACTION = 'echo'
echo=__import__('echo.routes')
actionmapping = echo.routes.actionmapping



def test_find_server_action():
    action_mapping = find_server_action()
    action = action_mapping.get(ACTION)
    assert action == actionmapping[0].get('controller')
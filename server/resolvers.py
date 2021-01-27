from functools import reduce

from settings import INSTALLED_APPS

def find_server_action():

    #application - список модулей: echo, servertime, etc.
    application = reduce(
        lambda value, item: value + [__import__(f'{item}.routes')],
        INSTALLED_APPS, []
    )
    #getattr - позволяет извлекать подмодуль routes из item
    #если routes нет, возвращаем значение None
    routes = reduce(
        lambda value, item: value + [getattr(item, 'routes', None)],
        application, []
    )
    mapping = reduce(
        lambda value, item: value + getattr(item, 'actionmapping', []),
        routes, []
    )
    return {item.get('action'):item.get('controller') for item in mapping if item}

#__import__ потому что просто import модуля обычный это не может сделать, но есть функции _import__ ,
#которая позволяет это сделать
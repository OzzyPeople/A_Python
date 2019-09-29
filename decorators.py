import logging
from functools import wraps

# Создаем кастомный логгер, чтобы дальше можно его было как-т отдельно конфигурировать от базовой конфигруации
logger = logging.getLogger('controllers')


def logged(log_format):
    def decorator(func):
        @wraps(func)
        #добавляем аргумент request, так как это обязательный аргумент функции контролера
        def wrapper(request, *args, **kwargs):
            result = func(request, *args, **kwargs)
            #создаем запись в нашем логе
            # включаем аргумент request в список переменных
            #вмечто print фиксируем наши сообщения через логгер - наш журнал
            logger.debug(
                log_format % {'name': func.__name__, 'request':request, 'type data': type(request.get('data')),'args': args, 'kwargs': kwargs, 'result': result}
            )
            return result
        return wrapper
    return decorator



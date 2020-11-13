import signal


class TimedOutExc(Exception):
    pass

def timeout(func):
    '''Function wrapper which sets a timeout to the wrapped function.
    The wrapped function has to be invoked with a kwargs `timeout`
    '''
    def decorate(*args, **kwargs):
        def handler(signum, frame):
            raise TimedOutExc()
        
        to = kwargs.pop('timeout')
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(to)
        return func(*args, timeout=to)
        signal.alarm(0) 
        
    return decorate

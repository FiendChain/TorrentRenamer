class AppError(Exception):
    def __init__(self, msg, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.msg = msg

class AppWarning(Exception):
    def __init__(self, msg, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.msg = msg
        
def catch_errors(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except AppError as ex:
            self.onError.emit(ex.msg)
        except AppWarning as ex:
            self.onError.emit(ex.msg)
    return wrapper 
    
    
class __Const_ServerConfig:
    def __setattr__(self, *x):
        raise TypeError
    # set something (TO-DO)
    HOST = '0.0.0.0'
    PORT = '5000'
    DEBUG = False
    MAX_REQUEST_LENGTH = 2 * 1024 * 1024 # bytes
    DEFAULT_RESPONSE_HEADER = {'Cache-Control': 'no-cache, no-store, must-revalidate',
                               'Expires': 'Sat, 01 Jan 2000 01:00:00 GMT',
                               'Pragma': 'no-cache'}
    ADMIN_ID = 'id'
    ADMIN_PASSWORD = 'password'
    TOKEN_HEADER = '{"alg":"HS256","typ":"JWT"}'
    TOKEN_SERVER_KEY = 'THE_BEST_KEY'
    TOKEN_DURATION = 30 * 60  # seconds


class __Const_MotorConfig:
    def __setattr__(self, *x):
        raise TypeError
    # set something (TO-DO)
    MAX_SINGLE_MOVE = 180 # degrees
    MAX_MOVE_TASK_DURATION = 20 # seconds
    UNIT_OF_TASK = 2 # degrees
    TICK_OF_TASK = 0.1 # seconds


class __Const_StreamConfig:
    def __setattr__(self, *x):
        raise TypeError
    # set something (TO-DO)
    QUALITY = 75 # 0 ~ 100
    TIMEOUT = 30 # seconds
    THREAD_TIMEOUT = 5 # seconds
    PLACEHOLDER = 'server/not-found.jpg'


serverConfig = __Const_ServerConfig()
motorConfig = __Const_MotorConfig()
streamConfig = __Const_StreamConfig()
from flask import request
from flask_restful import Resource, reqparse
from werkzeug.exceptions import HTTPException
from datetime import datetime
from .setting import serverConfig
from .crypt import HMAC_SHA256, Base64Encode, Base64Decode
import flask_restful, json

def WriteToken(id):
    try:
        expired = int(datetime.utcnow().timestamp()) + serverConfig.TOKEN_DURATION
        header = Base64Encode(serverConfig.TOKEN_HEADER, urlSafe=True, ignorePadding=True)
        payload = Base64Encode(json.dumps({
            'id': id,
            'exp': expired
        }, separators=(',',':')), urlSafe=True, ignorePadding=True)
        signature = Base64Encode(HMAC_SHA256(serverConfig.TOKEN_SERVER_KEY,
                                             header + '.' + payload),
                                 urlSafe=True, ignorePadding=True)

        return {'token': header + '.' + payload + '.' + signature, 'expired': expired}
    except:
        raise Exception('fail to make token')


def CheckToken(tokenString):
    try:
        header, payload, signature = tokenString.split('.')

        if signature != Base64Encode(HMAC_SHA256(serverConfig.TOKEN_SERVER_KEY,
                                                 header + '.' + payload),
                                     urlSafe=True, ignorePadding=True):
            return {'result': False, 'message': 'signature error'}

        header = json.loads(Base64Decode(header, urlSafe=True))
        payload = json.loads(Base64Decode(payload, urlSafe=True))

        if header != json.loads(serverConfig.TOKEN_HEADER):
            return {'result': False, 'message': 'header error'}
        elif int(datetime.utcnow().timestamp()) > int(payload['exp']):
            return {'result': False, 'message': 'expired'}
        else:
            return {'result': True, 'message': 'success', 'data': payload}
    except:
        return {'result': False, 'message': 'parsing error'}


def Auth(idList=None):
    try:
        headToken = request.headers.get('x-access-token')
        if headToken:
            authDict = CheckToken(headToken)
        else:
            authDict = CheckToken(request.args.get('x-access-token'))
    
        if (authDict.get('result') == True and
            (idList == None or authDict['data'].get('id') in idList)):
            return True
        else:
            # ONLY FOR TESTING
            print('Auth Fail')
            return False
    except:
        return False


class Token(Resource):
    def get(self):
        try:
            headToken = request.headers.get('x-access-token')
            if not headToken:
                headToken = request.args.get('x-access-token')
            result = CheckToken(headToken)
            return result, 200, serverConfig.DEFAULT_RESPONSE_HEADER
        except:
            return ({'result': 'error', 'message': 'unknown error'},
                    500, serverConfig.DEFAULT_RESPONSE_HEADER)

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str, required=True, nullable=False,
                                case_sensitive=False, trim=True)
            parser.add_argument('password', type=str, required=True, nullable=False, trim=True)
            args = parser.parse_args()

            if (args['id'] != serverConfig.ADMIN_ID or args['password'] != serverConfig.ADMIN_PASSWORD): # should change in future
                flask_restful.abort(400)
            else:
                return ({'result': 'success', 'message': 'MakeToken: success', 'data': WriteToken(args['id'])},
                        200, serverConfig.DEFAULT_RESPONSE_HEADER)
        except HTTPException as e:
            return ({'result': 'error', 'message': str(e)},
                    e.code, serverConfig.DEFAULT_RESPONSE_HEADER)
        except:
            return ({'result': 'error', 'message': 'unknown error'},
                    500, serverConfig.DEFAULT_RESPONSE_HEADER)
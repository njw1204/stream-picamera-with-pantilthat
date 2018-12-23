from flask import abort
from flask_restful import Resource, reqparse
from werkzeug.exceptions import HTTPException
from .setting import serverConfig, motorConfig
from .tokenManager import Auth
from . import pantilt
import flask_restful

class SingleMovement(Resource):
    def post(self):
        try:
            if not Auth([serverConfig.ADMIN_ID]):
                flask_restful.abort(403)

            parser = reqparse.RequestParser()
            parser.add_argument('dir', type=str, required=True, nullable=False,
                                case_sensitive=False, trim=True)
            parser.add_argument('value', type=int, required=True, nullable=False)
            args = parser.parse_args()

            if (args['dir'] not in ['up','down','left','right'] or
                not 0 < args['value'] <= motorConfig.MAX_SINGLE_MOVE):
                flask_restful.abort(400)
            else:
                pantilt.moveRelative(args['dir'], args['value'])
                return ({'result': 'success', 'message': 'SingleMovement: '
                         + args['dir'] + ' ' + str(args['value'])},
                        200, serverConfig.DEFAULT_RESPONSE_HEADER)
        except HTTPException as e:
            return ({'result': 'error', 'message': str(e)},
                    e.code, serverConfig.DEFAULT_RESPONSE_HEADER)
        except:
            return ({'result': 'error', 'message': 'unknown error'},
                    500, serverConfig.DEFAULT_RESPONSE_HEADER)


class MovementTask(Resource):
    def post(self):
        try:
            if not Auth([serverConfig.ADMIN_ID]):
                flask_restful.abort(403)

            parser = reqparse.RequestParser()
            parser.add_argument('dir', type=str, required=True, nullable=False,
                                case_sensitive=False, trim=True)
            parser.add_argument('value', type=int, required=True, nullable=False)
            parser.add_argument('force', type=bool)
            args = parser.parse_args()

            if (args['dir'] not in ['up','down','left','right'] or
                not 0 < args['value'] <= motorConfig.MAX_MOVE_TASK_DURATION):
                flask_restful.abort(400)
            elif pantilt.startTask(args['dir'], args['value'], args['force']) == False:
                flask_restful.abort(409)
            else:
                return ({'result': 'success', 'message': 'MovementTask: start '
                         + args['dir'] + ' ' + str(args['value'])},
                        200, serverConfig.DEFAULT_RESPONSE_HEADER)
        except HTTPException as e:
            return ({'result': 'error', 'message': str(e)},
                    e.code, serverConfig.DEFAULT_RESPONSE_HEADER)
        except:
            return ({'result': 'error', 'message': 'unknown error'},
                    500, serverConfig.DEFAULT_RESPONSE_HEADER)

    def delete(self):
        try:
            if not Auth([serverConfig.ADMIN_ID]):
                flask_restful.abort(403)

            pantilt.stopTask()

            return ({'result': 'success', 'message': 'MovementTask: stop'},
                    200, serverConfig.DEFAULT_RESPONSE_HEADER)
        except HTTPException as e:
            return ({'result': 'error', 'message': str(e)},
                    e.code, serverConfig.DEFAULT_RESPONSE_HEADER)
        except:
            return ({'result': 'error', 'message': 'unknown error'},
                    500, serverConfig.DEFAULT_RESPONSE_HEADER)
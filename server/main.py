from flask import Flask, render_template, request, make_response, redirect, send_from_directory
from flask_restful import Api
from .setting import serverConfig
from . import motorManager, tokenManager, videoManager


def WebMain():
    r = make_response(render_template('sample.html', token=request.form.get('token', '')))
    for k, v in serverConfig.DEFAULT_RESPONSE_HEADER.items():
        r.headers.set(k, v)
    return r


def Login():
    r = make_response(render_template('login.html'))
    for k, v in serverConfig.DEFAULT_RESPONSE_HEADER.items():
        r.headers.set(k, v)
    return r


def Root():
    return redirect('/login')


def send_js(path):
    return send_from_directory('js', path)


def send_css(path):
    return send_from_directory('css', path)


def send_webfonts(path):
    return send_from_directory('webfonts', path)


def run():
    app = Flask('server')
    app.config['MAX_CONTENT_LENGTH'] = serverConfig.MAX_REQUEST_LENGTH
    api = Api(app)

    # GET : 토큰 체크, POST : 토큰 생성
    api.add_resource(tokenManager.Token, '/token')

    # POST : 단일 Move 이벤트 생성
    api.add_resource(motorManager.SingleMovement, '/move')

    # POST : 지속 Move 테스크 생성, DELETE : 지속 Move 테스크 제거
    api.add_resource(motorManager.MovementTask, '/move-task')

    # GET : 라이브 비디오 스트림 (MJPEG 포맷)
    app.add_url_rule('/stream', 'Stream', videoManager.Stream)

    # POST : 관리자 웹 페이지
    app.add_url_rule('/web/main', 'WebMain', WebMain, methods=['POST'])

    # GET : 로그인 웹 페이지
    app.add_url_rule('/login', 'Login', Login)

    # GET : 메인
    app.add_url_rule('/', 'Root', Root)

    # 정적 파일
    app.add_url_rule('/js/<path:path>', 'send_js', send_js)
    app.add_url_rule('/css/<path:path>', 'send_css', send_css)
    app.add_url_rule('/webfonts/<path:path>', 'send_webfonts', send_webfonts)

    app.run(host=serverConfig.HOST, port=serverConfig.PORT, debug=serverConfig.DEBUG,
            threaded=True)
# stream-picamera-with-pantilthat
웹 페이지에서 CCTV를 실시간으로 보면서 (picamera), CCTV를 움직일 수 있습니다 (pantilthat).  
물론 아무나 보면 안 되니까 로그인 절차가 포함되어 있습니다.  
방화벽 설정만 하면 외부 네트워크에서 접속도 가능합니다.

## 사용법
- `pip3 install -r requirements.txt`
- `sudo python3 app.py`
- URL : http://127.0.0.1:5000

## 주의사항
- 관리자 아이디와 비밀번호는 server/setting.py 에서 설정<br/>
(ADMIN_ID, ADMIN_PASSWORD)

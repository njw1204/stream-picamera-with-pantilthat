# API Document

## 1. 토큰

### 1.1. 토큰 생성 API
사용자 또는 관리자의 계정 정보를 받아 토큰을 생성합니다.<br/>
사용자 계정 생성 API는 아직 없으니 관리자 계정을 이용하세요.<br/>
관리자의 계정 정보는 현재 setting.py에 저장되어 있습니다.<br/>
토큰은 사용자 인증이 필요한 API에서 이용합니다.<br/>
토큰에는 만료일이 있으며, 만료되면 새로 생성해야 합니다.<br/>
<br/>

#### 1) Request
* **URL** : `/token`
* **Method** : `POST`
* **Content-Type** : `application/json`
* **Data constraints**
```json
{
    "id": "토큰을 발급받을 사용자 또는 관리자의 아이디 [string, required]",
    "password": "사용자 또는 관리자의 비밀번호 [string, required]"
}
```
* **Data example**
```json
{
    "id": "id",
    "password": "password"
}
```
<br/>

#### 2) Response
성공하면 result 필드에 success, 실패하면 error가 저장됩니다.<br/>
data 객체의 token 필드에 생성된 토큰이 들어갑니다.<br/>
클라이언트에 저장 후 필요할 때 사용하면 됩니다.<br/>
expired 필드는 토큰의 만료일을 나타내는 UTC 타임스탬프 값입니다.
* **Content example**
```json
{
    "result": "success",
    "message": "MakeToken: success",
    "data": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImlkIiwiZXhwIjoxNTMzNDkyOTU1fQ.vp07Tc4imKgR5dXXnKDW5cZR65H_m9i7mKXOUHE5Gp8",
        "expired": 1533492955
    }
}
```
<br/>

### 1.2. 토큰 검증 API
클라이언트가 소유한 토큰의 유효성을 체크합니다.<br/>
토큰은 기본적으로 헤더로 입력하지만, 테스트 용도로 URL 쿼리 스트링으로 입력할 수 있습니다.<br/>
예시 : `/token?x-access-token=ebvT07c5ZhXOpey`<br/>
<br/>

#### 1) Request
* **URL** : `/token`
* **Method** : `GET`
* **Header constraints**
```
x-access-token: 사용자의 토큰값 [required]
```
* **Header example**
```
x-access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImlkIiwiZXhwIjoxNTMzNDkyOTU1fQ.vp07Tc4imKgR5dXXnKDW5cZR65H_m9i7mKXOUHE5Gp8
```
<br/>

#### 2) Response
result 필드가 true이면 토큰이 유효한 것이고, false이면 유효하지 않습니다.<br/>
토큰이 유효하면 토큰의 정보가 data 객체에 저장되어 반환됩니다.<br/>
유효하지 않을 시 message 필드에 원인이 저장됩니다.
* **Content example 1**
```json
{
    "result": true,
    "message": "success",
    "data": {
        "id": "id",
        "exp": 1533494845
    }
}
```
* **Content example 2**
```json
{
    "result": false,
    "message": "expired"
}
```
<br/>

## 2. 스트리밍

### 2.1. 라이브 스트리밍 시청 API (Non-REST)
CCTV의 현재 화면을 라이브로 볼 수 있는 스트리밍 API 입니다.<br/>
스트리밍 데이터는 MJPEG 포맷으로 반환됩니다.<br/>
<br/>
또한 사용자 인증을 위해 토큰을 입력받습니다.<br/>
현재는 관리자의 토큰만 허용합니다.<br/>
토큰은 기본적으로 헤더로 입력하지만, 테스트 용도로 URL 쿼리 스트링으로 입력할 수 있습니다.<br/>
예시 : `/stream?x-access-token=ebvT07c5ZhXOpey`<br/>
<br/>

#### 1) Request
* **URL** : `/stream`
* **Method** : `GET`
* **Header constraints**
```
x-access-token: 사용자의 토큰값 [required]
```
* **Header example**
```
x-access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImlkIiwiZXhwIjoxNTMzNDkyOTU1fQ.vp07Tc4imKgR5dXXnKDW5cZR65H_m9i7mKXOUHE5Gp8
```
<br/>

#### 2) Response
MJPEG 데이터가 지속적으로 반환됩니다.<br/>
연결을 종료하지 않으면 Response data가 계속 생성되니 주의해주세요.
* **Content example**
```http
HTTP/1.1 200 OK
Content-Type: multipart/x-mixed-replace;boundary=frame

--frame
Content-Type: image/jpeg

[JPEG-DATA]
--frame
Content-Type: image/jpeg

[JPEG-DATA]
--frame
Content-Type: image/jpeg

[JPEG-DATA]
```
<br/>

## 3. 이벤트

### 3.1. 카메라 Single Movement 이벤트 생성 API
카메라를 1회 움직이는 이벤트를 생성합니다.<br/>
카메라를 움직일 방향과 이동 크기를 입력받습니다.<br/>
방향은 up, down, left, right 4개 중 하나를 입력해야 하며<br/>
이동 크기는 setting.py에 정의된 MAX_SINGLE_MOVE 이하로 입력해야 합니다.<br/>
<br/>
또한 사용자 인증을 위해 토큰을 입력받습니다.<br/>
현재는 관리자의 토큰만 허용합니다.<br/>
토큰은 기본적으로 헤더로 입력하지만, 테스트 용도로 URL 쿼리 스트링으로 입력할 수 있습니다.<br/>
예시 : `/move?x-access-token=ebvT07c5ZhXOpey`<br/>
<br/>

#### 1) Request
* **URL** : `/move`
* **Method** : `POST`
* **Content-Type** : `application/json`
* **Header constraints**
```
x-access-token: 사용자의 토큰값 [required]
```
* **Header example**
```
x-access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImlkIiwiZXhwIjoxNTMzNDkyOTU1fQ.vp07Tc4imKgR5dXXnKDW5cZR65H_m9i7mKXOUHE5Gp8
```
* **Data constraints**
```json
{
    "dir": "카메라 이동 방향 (up,down,left,right 중 하나) [string, required]",
    "value": "카메라 이동 크기 (MAX_SINGLE_MOVE 이하) [int, required]"
}
```
* **Data example**
```json
{
    "dir": "right",
    "value": 3
}
```
<br/>

#### 2) Response
성공하면 result 필드에 success, 실패하면 error가 저장됩니다.
* **Content example**
```json
{
    "result": "success",
    "message": "SingleMovement: right 3"
}
```
<br/>

### 3.2. 카메라 Movement Task 이벤트 생성 API
카메라를 지속적으로 움직이는 스케쥴링 이벤트를 생성합니다.<br/>
카메라를 움직일 방향과 작업 시간을 입력받습니다.<br/>
방향은 up, down, left, right 4개 중 하나를 입력해야 하며<br/>
작업 시간은 setting.py에 정의된 MAX_MOVE_TASK_DURATION 이하로 입력해야 합니다.<br/>
작업 시간 동안 카메라가 지속적으로 움직이고, 시간이 끝나면 Task가 제거됩니다.<br/>
한번에 하나의 Task만 돌아갈 수 있다는 점을 주의하세요.<br/>
<br/>
또한 사용자 인증을 위해 토큰을 입력받습니다.<br/>
현재는 관리자의 토큰만 허용합니다.<br/>
토큰은 기본적으로 헤더로 입력하지만, 테스트 용도로 URL 쿼리 스트링으로 입력할 수 있습니다.<br/>
예시 : `/move-task?x-access-token=ebvT07c5ZhXOpey`<br/>
<br/>

#### 1) Request
* **URL** : `/move-task`
* **Method** : `POST`
* **Content-Type** : `application/json`
* **Header constraints**
```
x-access-token: 사용자의 토큰값 [required]
```
* **Header example**
```
x-access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImlkIiwiZXhwIjoxNTMzNDkyOTU1fQ.vp07Tc4imKgR5dXXnKDW5cZR65H_m9i7mKXOUHE5Gp8
```
* **Data constraints**
```json
{
    "dir": "카메라 이동 방향 (up,down,left,right 중 하나) [string, required]",
    "value": "작업 시간 (MAX_MOVE_TASK_DURATION 이하) [int, required]",
    "force": "기존 task가 있다면 강제로 중지할지 선택 [bool, optional]"
}
```
* **Data example**
```json
{
    "dir": "up",
    "value": 5,
    "force": true
}
```
<br/>

#### 2) Response
성공하면 result 필드에 success, 실패하면 error가 저장됩니다.<br/>
이때 기존의 작업이 동작 중이여서 실패하면 409 Conflict 코드가 반환됩니다.<br/>
이를 방지하기 위해선 force 인자에 true 값을 보내면 됩니다.
* **Content example**
```json
{
    "result": "success",
    "message": "MovementTask: start up 5"
}
```
<br/>

### 3.3. 카메라 Movement Task 이벤트 제거 API
현재 작업 중인 카메라 Movement Task를 제거합니다.<br/>
작업 중인 Task가 없다면 무시됩니다.<br/>
<br/>
또한 사용자 인증을 위해 토큰을 입력받습니다.<br/>
현재는 관리자의 토큰만 허용합니다.<br/>
토큰은 기본적으로 헤더로 입력하지만, 테스트 용도로 URL 쿼리 스트링으로 입력할 수 있습니다.<br/>
예시 : `/move-task?x-access-token=ebvT07c5ZhXOpey`<br/>
<br/>

#### 1) Request
* **URL** : `/move-task`
* **Method** : `DELETE`
* **Header constraints**
```
x-access-token: 사용자의 토큰값 [required]
```
* **Header example**
```
x-access-token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImlkIiwiZXhwIjoxNTMzNDkyOTU1fQ.vp07Tc4imKgR5dXXnKDW5cZR65H_m9i7mKXOUHE5Gp8
```
<br/>

#### 2) Response
성공하면 result 필드에 success, 실패하면 error가 저장됩니다.
* **Content example**
```json
{
    "result": "success",
    "message": "MovementTask: stop"
}
```

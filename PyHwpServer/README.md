# PyHwp-Server

## 기본 컨셉

    json을 일정한 형식을 갖추어 만들어 string으로 만들어 post로 전달하면 한글 작성되는 형식


### json 형식

1. 파일명 전달
    ```json
    {"meta": {
        "filename": "{파일명}"
    }}
    ```
    json 최상단에 meta 라는 key값을 가진 항목을 만들고 하위 항목에 filename이라는 key값에 파일명을 전달하면 됨.


2. text type
    ```json
    {"key string": "value string"}
    ```
    전달되는 json에 string: string 형태가 있다면 어디에 위치하든 찾아서 
    한글문서에서 "key string"의 누름틀을 찾아 "value string"값을 넣음


3. table type
    ```json
    {"key string": [["value string1", "value string2"], ["value string1", "value string2"], ]}
    ```
    전달되는 json이 string: [["string"]] 이런 형식으로 2차원 배열인 경우, 
    마찬가지로 json 내부에 어디에 위치해 있든 찾아서
    한글 문서의 key string의 누름틀을 찾아 표 작성


### 실행 방법

1. starter.bat을 실행시킨다. 
두가지 서버를 10초 간격으로 실행시키게 되어 있음. pc가 느려서 잘 안되는것 같다면 10초를 20초나 30초로 늘려볼것

2. uvicorn app:app --host `원하는 ip` --port `원하는 포트` 로 서버를 실행시킨다.

3. 서버 돌리기
- host:port/run 으로 GET method 요청
    ```cmd
    curl -X GET http://localhost:8000/run
    ```

4. 원하는 작업 전송: 

- host:port/ 로 POST {"payload": "json string"}을 전달한다.

- 예시-cmd : 
    ```cmd
    curl -X POST http://localhost:8000/ -H "Content-Type: application/json; charset=UTF-8" --data-raw "{\"payload\": \"{\\\"meta\\\": {\\\"filename\\\": \\\"여름 휴가 안내문.hwp\\\"}, \\\"company_name\\\": \\\"새라아이씨티\\\", \\\"date_info\\\": {\\\"year\\\": \\\"2024\\\", \\\"month\\\": \\\"08\\\", \\\"day\\\": \\\"01\\\"}, \\\"end_date_info\\\": {\\\"end_year\\\": \\\"2025\\\", \\\"end_month\\\": \\\"09\\\", \\\"end_day\\\": \\\"99\\\"}, \\\"tables\\\": {\\\"table_01\\\": [[\\\"책임기술자\\\", \\\"홍길 동\\\", \\\"특급기술자\\\", \\\"2024.01.31\\r\\n~\\r\\n2024.02.03\\\", \\\"보고서 검토 및 현장책임\\\", \\\"-\\\"], [\\\"참여기술자\\\", \\\"임꺽정\\\", \\\"중급기술자\\\", \\\"2024.01.31\\r\\n~\\r\\n2024.02.03\\\", \\\"보고서 작성 및 현장조사\\\", \\\"-\\\"]]}}\"}"
    ```

 - json 형태
    ```json
    {
        "payload":{
            "meta": {
                "filename": "여름 휴가 안내문.hwp"
            }, 
            "company_name": "새라아이씨티", 
            "date_info": {
                "year": "2024", 
                "month": "08", 
                "day": "01"
            }, 
            "end_date_info": {
                "end_year": "2025", 
                "end_month": "09", 
                "end_day": "99"
            }, 
            "tables": {
                "table_01": [
                    ["책임기술자", "홍길 동", "특급기술자", "2024.01.31rn~rn2024.02.03", "보고서 검토 및 현장책임", "-"], 
                    ["참여기술자", "임꺽정", "중급기술자", "2024.01.31rn~rn2024.02.03", "보고서 작성 및 현장조사", "-"]
                ]
            }
        }
    }
    ```
    * json은 string으로 변환하여 payload 뒤에 넣는다. 위의 예시는 CMD 에서 자동으로 이스케이프 문자열인 \를 무시하므로 \\두개씩 써야 처리되기 때문에 저렇게 난잡하게 된 건데, powershell이나 다른 버전의 cmd는 다를 수도 있으니 형편에 맞게 사용한다.
    * meta에 들어있는 정보는 한글 문서에 들어가지 않는다. 따라서 filename이나 기타 생성관련되지 않은 정보는 meta안에 넣는다.
    * nested한 json은 가장 안쪽의 형태만을 취급한다. 예를들어 `"date_info": { "year": "2024", "month": "08", "day": "01" }` 이렇게 nested한 내용도 최종 key:value 형태인 `"year": "2024", "month": "08", "day": "01"` 만을 찾아서 해당 누름틀에 입력한다. 즉, `"date_info"`라는 값은 무시된다.


5. 멈추고 싶으면 host:port/stop으로 요청
    ```cmd
    curl -X GET http://localhost:8000/stop
    ```
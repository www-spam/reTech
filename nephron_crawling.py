import requests
import json

url = "https://www.superbin.co.kr/map"

response = requests.get(url)
if response.status_code == 200:
    content = response.text
    start = content.find('<script id="__NEXT_DATA__" type="application/json">')
    end = content.find('</script>', start)
    
    if start != -1 and end != -1:
        json_data = content[start + len('<script id="__NEXT_DATA__" type="application/json">'):end]
        
        # Parse the JSON data
        data = json.loads(json_data)

        # Save the data as a JSON file
        with open('nephron_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print("JSON 데이터가 추출되어 nephron_data 파일로 저장됨.")
    else:
        print("스크립트 태그를 찾을 수 없음.")
else:
    print("웹 페이지를 가져오는데 실패.")

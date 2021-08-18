openpyxl 사용하기
===============


새 워크 북 생성
```python
from openpyxl import Workbook

wb = openpyxl.Workbook()
ws = wb.activate
```

기존 워크북 불러오기
```python
from openpyxl import load_workbook

wb = load_workbook(filename = 'filename.xlsx')

# 활성화 되어있는 시트 가져오기
ws = wb.activate

# 시트명으로 가져오기
ws = wb['Sheet4']
```

워크시트 생성
```python
wb.create_sheet('시트 이름', 0)
# 0 시트가 위치하는 순서
```

워크시트 속성
```python
worksheet.max_row  #활성화 된 row 갯수
worksheet.max_column #활성화된 column 갯구
```



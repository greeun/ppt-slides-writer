# 스타일 가이드

## 색상 팔레트

### 역할별 색상

| 역할 | fillColor | strokeColor | fontColor |
|------|-----------|-------------|-----------|
| Client/UI | #fff2cc | #d6b656 | black |
| API/Gateway | #e1d5e7 | #9673a6 | black |
| Service | #f8cecc | #b85450 | black |
| AI/Core | #0050ef | #001DBC | #ffffff |
| Database | #60a917 | #2D7600 | #ffffff |
| Infrastructure | #b0e3e6 | #0e8088 | black |
| External | #e6d0de | #996185 | black |
| Workflow/Success | #d5e8d4 | #82b366 | black |
| Warning/Alert | #ffe6cc | #d79b00 | black |
| Background/Layer | #f5f5f5 | #666666 | black |

### 브랜드 색상

| 서비스 | fillColor | strokeColor |
|--------|-----------|-------------|
| AWS | #FF9900 | #cc7a00 |
| Kubernetes | #326ce5 | #1a4db3 |
| Docker | #2496ED | #1a6db3 |

## 폰트 규칙

```xml
style="fontSize=10;fontStyle=1;fontColor=#333333"
```

| fontStyle 값 | 의미 | 용도 |
|--------------|------|------|
| 0 | Normal | 일반 텍스트 |
| 1 | Bold | 레이블, 제목 |
| 2 | Italic | 플로우 설명, 주석 |
| 3 | Bold + Italic | 강조 (거의 안 씀) |

줄바꿈: `value="Line1&#xa;Line2"`
텍스트 정렬: `align=left;verticalAlign=top` (좌상단) / `align=center;verticalAlign=middle` (중앙, 기본)

## 요소 XML 패턴

### 박스 (라운드)
```xml
<mxCell id="box1" value="Service A"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=10"
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="120" height="40" as="geometry"/>
</mxCell>
```

### DB 실린더
```xml
<mxCell id="db1" value="PostgreSQL"
  style="shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=8;
         fillColor=#60a917;strokeColor=#2D7600;fontColor=#ffffff;fontSize=9"
  vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="100" height="50" as="geometry"/>
</mxCell>
```

### 레이어 배경
```xml
<mxCell id="layer1" value=""
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;opacity=50"
  vertex="1" parent="1">
  <mxGeometry x="40" y="100" width="920" height="80" as="geometry"/>
</mxCell>
```

### 그룹/패키지
```xml
<mxCell id="group1" value="Module Name"
  style="shape=folder;fontStyle=1;spacingTop=10;tabWidth=50;tabHeight=14;tabPosition=left;html=1;
         fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11"
  vertex="1" parent="1">
  <mxGeometry x="40" y="50" width="200" height="150" as="geometry"/>
</mxCell>
```

## 예약 ID (Reserved IDs)

Draw.io 내보내기 시 특정 ID는 예약어로 취급되어 내보내기 실패.

| 예약 ID | 대체 예시 | 설명 |
|---------|----------|------|
| `filter` | `filter-agent`, `filter-box` | SVG/CSS 예약어 |

안전한 명명: `-agent`, `-node`, `-box` 같은 접미사 추가.

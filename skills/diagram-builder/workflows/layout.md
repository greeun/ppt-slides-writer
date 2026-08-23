# 레이아웃 가이드

## 연결 기반 배치 (핵심 규칙)

**원칙**: 연결 대상에 가까운 쪽에 요소 배치 -> 화살표 최소화

```
BAD: 긴 화살표                    GOOD: 짧은 화살표
+-------------------+ +---+      +-------------------+ +---+
| A | B | C <-------+-| X |      | C | B | A <-------+-| X |
+-------------------+ +---+      +-------------------+ +---+
```

| 상황 | 배치 규칙 |
|------|----------|
| External -> 내부 요소 | 연결받는 요소를 External 쪽에 배치 |
| 레이어 간 다중 연결 | 연결 많은 요소를 중앙에 배치 |
| 그룹 내 순차 흐름 | 흐름 순서대로 좌->우 또는 상->하 |

## 수직 정렬

연결되는 요소를 같은 X좌표에 배치 -> 화살표가 직선.

```xml
<!-- 같은 X좌표 사용 -->
<mxCell id="sql-branch" ...>
  <mxGeometry x="155" y="248" width="70" height="45"/>
</mxCell>
<mxCell id="aurora" ...>
  <mxGeometry x="155" y="375" width="70" height="55"/>
</mxCell>

<!-- exitX=0.5, entryX=0.5 -> 직선, waypoint 불필요 -->
<mxCell style="...;exitX=0.5;exitY=1;entryX=0.5;entryY=0"
  source="sql-branch" target="aurora"/>
```

## 그룹 기반 레이아웃 (복잡한 시스템용)

개별 요소마다 화살표를 그리면 선이 과다. 그룹으로 묶고 대표 화살표만 표시.

| 조건 | 개별 요소 | 그룹 기반 |
|------|----------|----------|
| 레이어 간 화살표 | 3개 이하 | 4개 이상 |
| 요소 개수 | 5개 이하 | 6개 이상 |
| 목적 | 세부 설계 | 전체 개요 |

```xml
<!-- 그룹 박스 -->
<mxCell id="compute-group" value="Compute Layer (ECS)"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;
         verticalAlign=top;fontStyle=1;fontSize=11"
  vertex="1" parent="1">
  <mxGeometry x="40" y="200" width="400" height="120" as="geometry"/>
</mxCell>

<!-- 내부 흐름을 텍스트로 -->
<mxCell id="internal-flow" value="[Router] -> [SQL/Graph/RAG] -> [Response]"
  style="text;html=1;strokeColor=none;fillColor=none;fontSize=9;fontStyle=2"
  vertex="1" parent="1">
  <mxGeometry x="60" y="250" width="360" height="20" as="geometry"/>
</mxCell>

<!-- 그룹 간 대표 화살표 (1개) -->
<mxCell style="...;exitX=0.5;exitY=1;entryX=0.5;entryY=0"
  edge="1" source="compute-group" target="data-group"/>
```

## 정렬 패턴

**수평 정렬**: 같은 레이어 요소는 동일 Y좌표, 15-20px 간격
**수직 정렬**: 레이어 간 20px 간격, Y = 이전 레이어 끝 + 간격
**그리드 배치**: 다:다 연결 시 연결 대상에 맞춰 X좌표 정렬

# 화살표 & 커넥터

## 필수: exitX/Y, entryX/Y 명시

자동 라우팅(`orthogonalEdgeStyle`만)은 경로 예측 불가. 시작점/끝점 위치 명시 필수.

```xml
<mxCell id="arr1"
  style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;
         strokeWidth=2;strokeColor=#666666;
         exitX=1;exitY=0.5;entryX=0;entryY=0.5"
  edge="1" parent="1" source="A" target="B">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

## 좌표 시스템

```
        entryY=0
           |
     +-------------+
     |             |
exitX=0 <    >  exitX=1
entryX=0         entryX=1
     |             |
     +-------------+
        exitY=1
        entryY=1
```

## 방향별 설정

| 방향 | exitX | exitY | entryX | entryY | 예시 |
|------|-------|-------|--------|--------|------|
| -> 오른쪽 | 1 | 0.5 | 0 | 0.5 | 수평 흐름 |
| <- 왼쪽 | 0 | 0.5 | 1 | 0.5 | 역방향 |
| v 아래 | 0.5 | 1 | 0.5 | 0 | 레이어 간 |
| ^ 위 | 0.5 | 0 | 0.5 | 1 | 피드백 |

## 다중 출구 (1:N 분기)

하나의 요소에서 여러 방향으로 나갈 때, exitY를 다르게:

```xml
<!-- Router -> 4개 브랜치 -->
<mxCell ... exitX=1;exitY=0.2 ... target="branch1"/>  <!-- 위쪽 -->
<mxCell ... exitX=1;exitY=0.4 ... target="branch2"/>
<mxCell ... exitX=1;exitY=0.6 ... target="branch3"/>
<mxCell ... exitX=1;exitY=0.8 ... target="branch4"/>  <!-- 아래쪽 -->
```

## Waypoint (복잡한 경로)

직선으로 안 될 때 경유점 지정:

```xml
<mxCell id="arr3" style="..." edge="1" source="A" target="C">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="300" y="150"/>
      <mxPoint x="300" y="300"/>
    </Array>
  </mxGeometry>
</mxCell>
```

## 레이어 경계 Waypoint

**문제**: 여러 화살표가 박스 위에서 겹침
**해결**: 레이어 사이 빈 공간에서 수평 이동 후 수직 하강

```xml
<!-- A -> F: 레이어 경계에서 꺾기 -->
<mxCell style="edgeStyle=orthogonalEdgeStyle;...;exitX=0.5;exitY=1;entryX=0.5;entryY=0"
  edge="1" source="A" target="F">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="100" y="215"/>  <!-- A 아래, 경계선 -->
      <mxPoint x="500" y="215"/>  <!-- F 위, 경계선 -->
    </Array>
  </mxGeometry>
</mxCell>
```

핵심: 레이어 사이 여백 최소 20-30px, 모든 레이어 간 화살표는 경계선 Y좌표에서 꺾기.

## Y좌표 분리 (화살표 겹침 방지)

같은 Y좌표에서 수평 이동하면 겹침. 각 화살표가 다른 Y좌표 사용 (6-8px 간격).

```xml
<!-- 화살표 1: y=418, 화살표 2: y=425, 화살표 3: y=432 -->
<Array as="points">
  <mxPoint x="200" y="418"/>
  <mxPoint x="500" y="418"/>
</Array>
```

## 외곽 경로 Waypoint (External 연결)

External -> 내부 레이어 연결 시 캔버스 외곽을 따라 이동:

```xml
<mxCell style="edgeStyle=orthogonalEdgeStyle;rounded=1;...;dashed=1;exitX=1;exitY=0.5;entryX=0.5;entryY=1"
  edge="1" source="external-box" target="internal-box">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="1150" y="160"/>  <!-- 외곽 오른쪽 -->
      <mxPoint x="1150" y="580"/>  <!-- 외곽 아래 -->
      <mxPoint x="540" y="580"/>   <!-- 대상 아래 -->
    </Array>
  </mxGeometry>
</mxCell>
```

`rounded=1`로 꺾이는 부분 부드럽게. 외곽 X좌표: pageWidth - 50px.

## 점선 라우팅 (배치/비동기)

**핵심 원칙**: 점선은 요소 위를 절대 지나가지 않는다 -> 항상 외곽 우회

**패턴 1: 레이어 아래 우회** (내부 요소 간)
```xml
<mxCell style="...;dashed=1;exitX=0.5;exitY=1;entryX=0.5;entryY=1"
  source="titan" target="opensearch">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="270" y="445"/>
      <mxPoint x="600" y="445"/>
    </Array>
  </mxGeometry>
</mxCell>
```

**패턴 2: 캔버스 외곽 우회** (External -> 내부)
```xml
<mxCell style="...;dashed=1;rounded=1;exitX=0;exitY=1;entryX=0.5;entryY=1"
  source="external" target="aurora">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="910" y="130"/>
      <mxPoint x="910" y="500"/>
      <mxPoint x="400" y="500"/>
    </Array>
  </mxGeometry>
</mxCell>
```

**라우팅 우선순위**: 레이어 간 간격 > 캔버스 아래 여백 > 캔버스 오른쪽 여백

## 선 스타일 옵션

| 속성 | 값 | 효과 |
|------|-----|------|
| `strokeWidth` | 1-2 | 선 두께 |
| `strokeColor` | #666666 | 선 색상 |
| `dashed` | 1 | 점선 |
| `endArrow` | classic, block, none | 화살표 모양 |
| `startArrow` | classic, none | 시작점 화살표 |

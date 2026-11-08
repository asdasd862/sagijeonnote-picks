# 사기전노트 링크허브 — DESIGN.md

`index.html`을 고치거나 새 영상 섹션을 붙일 때 지키는 규칙이에요. 상황판 DESIGN.md(Emil Kowalski 움직임 규칙,
Impeccable의 'AI 티 나는 디자인' 금지 목록, taste-skill 일관성 규칙, awesome-design-md 형식)를 허브에 맞게 옮겼어요. (2026-11-08)

## 0. 새 영상 섹션 붙이기 (매 업로드)
1. `index.html`에서 `<div id="video-list" class="video-list"></div></div>` 바로 뒤(= 첫 `<section data-theme` 앞)에 새 섹션을 넣어요. 형식은 예전과 똑같아요:
   ```html
   <section data-theme="ID" id="ID" data-video-id="유튜브ID" data-video-title="영상 제목" data-cover="ID-cover.jpg" data-cover-kind="cover" data-keywords="띄어쓰기로 구분한 검색어" hidden data-visible-from="2026-11-19T19:00:00+09:00">
   <article class="card" id="ID-1"><div class="row"><div class="photo"><img src="ID-1.jpg" alt="설명" loading="lazy"><span class="num">1</span></div><div><h2>제품명</h2><p class="benefit">한 줄 장점</p><p class="option">옵션</p><p class="shipping">배송·옵션</p></div></div><a class="cta" href="https://link.coupang.com/a/..." target="_blank" rel="sponsored noopener">쿠팡에서 상품 보기</a></article>
   …(카드 3개)
   <details><summary>구매 전에 이것만 확인하기</summary><p>…</p></details></section>
   ```
   - 원본 사진(jpg/png)은 지금처럼 저장소 맨 위 폴더에 올려요. 원본은 지우지 않아요.
   - `data-visible-from` 시각 전에는 숨겨지고, 지나면 15초 안에 저절로 맨 위에 나타나요.
   - 영상 제목 끝의 `#해시태그`는 화면에서 자동으로 빠져요(검색에는 그대로 쓰임).
2. **썸네일 만들기**: `python tools/make_thumbs.py` (Pillow 필요). 새 사진마다 `t/이름.webp`(폭 480)를 만들고
   `index.html`의 `src`/`data-cover`를 썸네일로 바꾸고 `width/height/loading/decoding`을 채워요. 여러 번 돌려도 같아요.
   깜빡해도 페이지는 원본 사진으로 그대로 동작해요(느릴 뿐).
3. `credits.html`에 출처 추가 → `git add -A` → commit → push.

`<section>`·`article.card` 안에서 쓰는 클래스(`photo` `num` `benefit` `option` `shipping` `cta` `purchase-conditions`)와
`details`는 그대로예요. 영상 묶음 머리(커버·날짜·제목)는 스크립트가 `data-*`로 만들어 붙여요 — 마크업에 따로 넣지 마세요.

## 1. 성격
가게 앞에 붙여 둔 깔끔한 쇼핑 메모. 사진과 제품명이 먼저 보이고, 버튼은 하나만 또렷하게.
꾸밈보다 찾기. 움직임은 상태가 바뀔 때만.

## 2. 색 (토큰은 `:root`, 어두운 모드는 `prefers-color-scheme`)
| 역할 | 토큰 | 쓰임 |
|---|---|---|
| 종이 | `--paper` / `--surface` / `--sunk` | 바탕 / 카드 / 눌린 면(세그먼트, 칩) |
| 글자 | `--ink` → `--ink-2` → `--ink-3` | 제목 / 본문 / 보조 |
| 행동 | `--accent` | "쿠팡에서 상품 보기" 버튼만 |
| 형광펜 | `--hi` | 브랜드 표시, 제품 번호만 |
| 주의 | `--warm` | 배송·구매 조건 |

- 그라데이션 글자, 색 있는 그림자(글로우), 보라 금지. 색 바탕 위에 회색 글자 금지.
- 새 색을 만들지 말고 토큰을 써요.

## 3. 글꼴
- Pretendard Variable(동적 서브셋, jsDelivr) → 없으면 시스템 글꼴. 숫자는 `tnum`.
- 가장 작은 글자 12px. 검색칸은 16px(iOS 확대 방지).

## 4. 레이아웃
- 폭 최대 520px 한 줄. 800px 이상에서만 '영상별로 찾기' 2칸.
- 둥글기 세 단계만: `--r1` 20(카드) / `--r2` 14(사진·입력·버튼) / `--r3` 8(칩·번호).
- 카드 안에 카드 넣지 않기. 누를 곳은 높이 44px 이상.
- 세로로 긴 영상 프레임(세로/가로 > 1.3)은 112×140에 꽉 채워 자르고, 제품 사진은 통째로 보여 줘요(스크립트가 `.tall` 붙임).

## 5. 움직임 (Emil Kowalski 기준)
| 상황 | 시간 | 곡선 |
|---|---|---|
| 누름 | 100ms, `scale(.97)` | ease-out |
| 호버·색 | 150~200ms | `--ease` |
| 세그먼트 이동 | 250ms | `--ease` |
| 첫 화면 등장 | 450ms, 50ms 간격, 8개까지 | `--ease` |
| 보기 바꿈 | 200ms 페이드 | ease-out |

- `--ease` = `cubic-bezier(.23, 1, .32, 1)`. 튀는 곡선 금지. `scale(0)` 시작 금지.
- 스크롤할 때마다 나타나는 효과, 기울기, 패럴랙스, 떠다니는 장식 금지.
- 호버 효과는 `(hover: hover)`에서만. `prefers-reduced-motion`이면 전부 정지. `transition: all` 금지.
- 애니메이션 라이브러리(GSAP 등) 쓰지 않아요. CSS만.

## 6. 바꾸면 안 되는 것
- 쿠팡 파트너스 고지 문구, 모든 쿠팡 링크의 `rel="sponsored noopener"`, `credits.html`·`privacy.html` 링크.
- 검색(띄어쓰기 무시, 제품 글자 → 없으면 영상 제목·키워드), `data-visible-from` 시간 공개, '전체 제품(최신순)/영상별로 찾기', `#섹션ID`·`#카드ID`·`#videos` 주소.

## 7. 확인 방법
375 / 1440 폭, 밝게·어둡게 스크린샷. 검색(띄어쓰기 섞어서), 두 보기, 미래 시각 섹션이 숨는지 확인.

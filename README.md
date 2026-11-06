# 이세돌 사진첩

이세돌 관련 기사의 대표 사진을 연도별로 모아 보는 페이지입니다.
본 사이트인 [이세돌 아카이브](https://claude.ai/artifact/QNQmE2fMzHjBTtG4uco8B9)는 외부 이미지를 불러올 수 없어서, 사진첩만 GitHub Pages에 따로 둡니다.

- 주소: https://tachy-git.github.io/LeeSedolPhotos/
- 사건별 바로가기: `#event-<연대기 사건 id>` (예: `#event-lee-2016-game4`)
- 연도 바로가기: `#y<연도>` (예: `#y2016`)

## 구조
| 경로 | 내용 |
|---|---|
| `data/articles.json` | 기사 목록(`articles`)과 연대기 사건 제목(`events`). **기사를 고칠 때는 이 파일만 고칩니다.** |
| `scripts/fetch_images.py` | 각 기사의 대표 사진 주소(og:image)를 모아 `site/data/images.json`을 만듭니다. |
| `site/` | 사진첩 페이지(`index.html`)와 글꼴(Neo둥근모, SIL OFL). |
| `.github/workflows/pages.yml` | 사진 주소를 모으고 GitHub Pages에 배포합니다. |

## 언제 다시 만들어지나
- `main`에 올릴 때마다
- 매주 월요일 03:17(한국 시간): 언론사가 사진을 바꾸거나 지운 경우를 반영
- Actions 탭에서 직접 실행(Run workflow)

## 사진
- 사진 파일은 저장소에 없습니다. 페이지가 원래 언론사에서 사진을 불러와 보여 주고, 저작권은 원저작자에게 있습니다.
- 사진을 찾지 못했거나 언론사가 외부에서 불러가는 것을 막은 기사는 매체·날짜 타일로 보입니다. Actions 실행 기록의 `no image` 줄에서 어떤 기사인지 볼 수 있습니다.

## 기사 원본
- `data/articles.json`의 기사는 이세돌 아카이브 아티팩트의 `data/photos.json`(116건)과 같습니다. 기사를 더하거나 빼면 아티팩트 쪽도 같이 맞춥니다.

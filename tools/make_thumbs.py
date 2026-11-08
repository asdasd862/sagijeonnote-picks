"""링크허브 썸네일 만들기 (새 섹션을 index.html에 붙인 뒤, commit 전에 한 번 실행).

    python tools/make_thumbs.py

- index.html의 <img src="..."> 와 data-cover="..." 가 가리키는 원본(jpg/png)마다
  t/<이름>.webp (폭 최대 480px) 를 만들고, index.html 참조를 그 썸네일로 바꿔요.
- <img>에는 썸네일 실제 크기의 width/height, loading="lazy", decoding="async"를 넣어요.
- 원본 파일은 지우지 않아요(credits.html 등에서 그대로 씀). 여러 번 실행해도 결과는 같아요.
- 필요: Python 3 + Pillow (pip install pillow)
"""
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
THUMB_DIR = ROOT / "t"
MAX_W = 480
QUALITY = 72


def thumb_for(src: str):
    """원본 경로 → (썸네일 상대경로, (w, h)). 원본이 없거나 외부 주소면 None."""
    if src.startswith(("http:", "https:", "data:", "//")):
        return None
    if src.startswith("t/") and src.endswith(".webp"):
        path = ROOT / src
        if path.exists():
            with Image.open(path) as im:
                return src, im.size
        return None
    original = ROOT / src
    if not original.is_file():
        print(f"  ! 원본 없음: {src}", file=sys.stderr)
        return None
    rel = f"t/{original.stem}.webp"
    out = ROOT / rel
    if not out.exists() or out.stat().st_mtime < original.stat().st_mtime:
        THUMB_DIR.mkdir(exist_ok=True)
        with Image.open(original) as im:
            im = im.convert("RGB")
            if im.width > MAX_W:
                im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
            im.save(out, "WEBP", quality=QUALITY, method=6)
        print(f"  + {rel}  ({original.stat().st_size // 1024}KB → {out.stat().st_size // 1024}KB)")
    with Image.open(out) as im:
        return rel, im.size


def set_attr(tag: str, name: str, value: str) -> str:
    pattern = re.compile(rf'\s{name}="[^"]*"')
    if pattern.search(tag):
        return pattern.sub(f' {name}="{value}"', tag, count=1)
    return tag[:-1] + f' {name}="{value}">'


def fix_img(m: re.Match) -> str:
    tag = m.group(0)
    src = re.search(r'\ssrc="([^"]+)"', tag)
    if not src:
        return tag
    found = thumb_for(src.group(1))
    if not found:
        return tag
    rel, (w, h) = found
    tag = set_attr(tag, "src", rel)
    tag = set_attr(tag, "width", str(w))
    tag = set_attr(tag, "height", str(h))
    tag = set_attr(tag, "loading", "lazy")
    tag = set_attr(tag, "decoding", "async")
    return tag


def fix_cover(m: re.Match) -> str:
    found = thumb_for(m.group(1))
    return f'data-cover="{found[0]}"' if found else m.group(0)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    with INDEX.open(encoding="utf-8", newline="") as f:
        html = f.read()
    new = re.sub(r"<img\b[^>]*>", fix_img, html)
    new = re.sub(r'data-cover="([^"]+)"', fix_cover, new)
    if new != html:
        with INDEX.open("w", encoding="utf-8", newline="") as f:
            f.write(new)
        print("index.html 참조를 썸네일로 바꿨어요.")
    else:
        print("바꿀 것 없음 (이미 최신).")


if __name__ == "__main__":
    main()

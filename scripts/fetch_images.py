"""
Collect the preview image (og:image) of each article.

Usage: python3 scripts/fetch_images.py data/articles.json site/data
Writes <out_dir>/articles.json (copy) and <out_dir>/images.json ({id: image url}).
Runs in GitHub Actions, which can reach the news sites.
"""
import json
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
TIMEOUT = 20

# =======
# Meta tags to look for, best first
# =======
# Images whose address contains one of these are page decorations, not photos
SKIP_WORDS = ["logo", "icon", "btn", "button", "banner", "blank", "spacer", "pixel", "ad_", "/ad/", "sprite", "profile", "reporter", ".gif", ".svg"]
META_KEYS = ["og:image", "og:image:url", "og:image:secure_url", "twitter:image", "twitter:image:src"]


class MetaParser(HTMLParser):
    """Keep the first value of each image meta tag, plus <link rel="image_src">."""

    def __init__(self):
        super().__init__()
        self.found = {}
        self.first_img = None  # fallback: first photo-like <img> in the page

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "meta":
            key = (a.get("property") or a.get("name") or "").lower()
            if key in META_KEYS and a.get("content"):
                self.found.setdefault(key, a["content"].strip())
        elif tag == "link" and a.get("rel", "").lower() == "image_src" and a.get("href"):
            self.found.setdefault("image_src", a["href"].strip())
        elif tag == "img" and self.first_img is None:
            src = (a.get("data-src") or a.get("src") or "").strip()
            if looks_like_photo(src):
                self.first_img = src


def looks_like_photo(src):
    low = src.lower()
    if not src or low.startswith("data:"):
        return False
    if not any(ext in low for ext in (".jpg", ".jpeg", ".png", ".webp")):
        return False
    return not any(w in low for w in SKIP_WORDS)


def find_image(url):
    try:
        return fetch_image(url)
    except (TimeoutError, urllib.error.URLError):
        return fetch_image(url)  # one retry for slow servers


def fetch_image(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "ko,zh;q=0.8,en;q=0.6"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        # The <head> is enough; meta tags are ASCII so any decoding works
        html = resp.read(1_500_000).decode("utf-8", errors="ignore")
        final_url = resp.geturl()
    parser = MetaParser()
    parser.feed(html)
    candidates = [parser.found[k] for k in META_KEYS + ["image_src"] if k in parser.found]
    if parser.first_img:
        candidates.append(parser.first_img)
    if not candidates:
        return None
    return urljoin(final_url, candidates[0])


def check(article):
    try:
        return article["id"], find_image(article["url"]), None
    except Exception as e:  # network errors, HTTP errors, bad pages
        return article["id"], None, str(e)[:120]


def main():
    src, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    data = json.loads(src.read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)

    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(check, data["articles"]))

    images = {}
    for aid, image, error in results:
        if image:
            images[aid] = image
        else:
            print(f"no image  {aid}  {error or 'no meta tag'}")

    (out_dir / "articles.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    (out_dir / "images.json").write_text(json.dumps(images, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"images {len(images)} / {len(results)}")


if __name__ == "__main__":
    main()

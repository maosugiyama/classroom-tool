#!/usr/bin/env python3
"""bunken_inspect.py — 文献PDFの書誌情報を抽出する補助スクリプト

使い方:
    python3 bunken_inspect.py ファイル.pdf [ファイル2.pdf ...]

出力: 各ファイルについて
  - PDFメタデータ（Title / Author / CreationDate）
  - ISBN / DOI（冒頭ページから正規表現で検出）
  - 冒頭ページ（最大6ページ）のテキスト抜粋
  - ファイル名の提案は行わない（判断は Claude Code / ユーザーが行う）

依存: pypdf（無ければ `pip install pypdf`。poppler がある環境では
      pdfinfo / pdftotext での代用可）
"""

import re
import sys
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("pypdf が見つかりません。`pip install pypdf` を実行してください。")

ISBN_RE = re.compile(r"ISBN[\s:‐-]*((?:97[89][\s-]?)?(?:\d[\s-]?){9}[\dXx])")
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s\"<>]+)")
YEAR_RE = re.compile(r"\b(1[89]\d{2}|20[0-4]\d)\b")


def inspect(path: Path) -> None:
    print(f"\n{'=' * 70}\nFILE: {path.name}  ({path.stat().st_size / 1_048_576:.1f} MB)")
    try:
        reader = PdfReader(str(path))
    except Exception as e:
        print(f"  読み込み失敗: {e}")
        return

    meta = reader.metadata or {}
    print(f"  Pages : {len(reader.pages)}")
    print(f"  Title : {meta.get('/Title', '')}")
    print(f"  Author: {meta.get('/Author', '')}")
    print(f"  Date  : {meta.get('/CreationDate', '')}")

    # 冒頭テキスト（最大6ページ）
    head = ""
    for page in reader.pages[: min(6, len(reader.pages))]:
        try:
            head += (page.extract_text() or "") + "\n"
        except Exception:
            pass

    isbns = sorted(set(m.replace(" ", "").replace("-", "") for m in ISBN_RE.findall(head)))
    dois = sorted(set(DOI_RE.findall(head)))
    years = YEAR_RE.findall(head)

    if isbns:
        print(f"  ISBN  : {', '.join(isbns)}")
    if dois:
        print(f"  DOI   : {', '.join(dois[:3])}")
    if years:
        # 頻出年を刊行年の候補として提示
        top = max(set(years), key=years.count)
        print(f"  Year? : {top}（冒頭ページでの最頻出年。要確認）")

    if not head.strip():
        print("  ⚠ テキスト層なし（スキャンPDFの可能性）。標題紙を画像として確認すること。")
    else:
        excerpt = "\n".join(l for l in head.splitlines() if l.strip())[:800]
        print(f"  --- 冒頭テキスト抜粋 ---\n{excerpt}\n  --- ここまで ---")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for arg in sys.argv[1:]:
        p = Path(arg)
        if p.suffix.lower() == ".pdf" and p.exists():
            inspect(p)
        else:
            print(f"スキップ: {arg}（PDFではないか、存在しません）")

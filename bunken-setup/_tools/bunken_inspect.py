#!/usr/bin/env python3
"""文献PDFの書誌情報を読み取る補助スクリプト。

使い方:
    python3 bunken_inspect.py <PDFファイルのパス>

PDFの埋め込みメタデータと冒頭ページのテキストを表示し、
著者・出版年・タイトルの特定を助ける。
pypdf が無い環境では macOS の mdls にフォールバックする。
"""

import os
import subprocess
import sys


def inspect_with_pypdf(path):
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader  # 古い環境向け
        except ImportError:
            return False

    reader = PdfReader(path)
    meta = reader.metadata or {}
    print("== PDFメタデータ ==")
    for key in ("/Title", "/Author", "/Subject", "/CreationDate", "/Producer"):
        if meta.get(key):
            print(f"  {key[1:]}: {meta[key]}")
    print(f"  ページ数: {len(reader.pages)}")

    print("\n== 冒頭テキスト（最大2ページ・各1000字） ==")
    for i, page in enumerate(reader.pages[:2]):
        try:
            text = (page.extract_text() or "").strip()
        except Exception as e:  # 抽出失敗ページはスキップ
            text = f"(テキスト抽出失敗: {e})"
        print(f"--- {i + 1}ページ目 ---")
        print(text[:1000] if text else "(テキストなし・スキャンPDFの可能性)")
    return True


def inspect_with_mdls(path):
    print("== Spotlightメタデータ (mdls) ==")
    keys = [
        "kMDItemTitle", "kMDItemAuthors", "kMDItemNumberOfPages",
        "kMDItemContentCreationDate", "kMDItemWhereFroms",
        "kMDItemTextContentLanguage",
    ]
    cmd = ["mdls"]
    for k in keys:
        cmd += ["-name", k]
    cmd.append(path)
    try:
        print(subprocess.run(cmd, capture_output=True, text=True).stdout)
    except FileNotFoundError:
        print("mdls が見つかりません（macOS以外の環境）。")
        print("pypdf をインストールしてください: pip3 install pypdf")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"ファイルが見つかりません: {path}")
        sys.exit(1)

    size_mb = os.path.getsize(path) / (1024 * 1024)
    print(f"ファイル: {path}")
    print(f"サイズ: {size_mb:.1f} MB\n")

    if not inspect_with_pypdf(path):
        inspect_with_mdls(path)


if __name__ == "__main__":
    main()

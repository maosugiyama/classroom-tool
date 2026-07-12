# 講座資料ページ ― アップロード手順

## このパッケージの中身

```
upload/                      ← この中身をそのままリポジトリに追加
└── materials/
    └── russian-course/
        ├── index.html       ← パスワード付き入口ページ(暗号化済み)
        └── pdf/             ← 資料PDF 12点
materials_html_snippet.html  ← materials.html に貼るリンクカード
src/list_source.html         ← 一覧ページの平文ソース(編集用・アップロードしない!)
src/.staticrypt.json         ← 暗号化の設定(保管用・アップロードしない)
```

## アップロード方法(GitHubのWeb画面から)

1. https://github.com/maosugiyama/maosugiyama.github.io を開く
2. 「Add file」→「Upload files」
3. `upload/` フォルダの中の `materials` フォルダごとドラッグ&ドロップ
   (リポジトリに `materials/russian-course/...` という階層ができればOK)
4. 「Commit changes」を押す
5. `materials.html` を開き、鉛筆アイコン(Edit)→ 既存の教材カードの下に
   `materials_html_snippet.html` の中身を貼り付けて Commit
6. 数分待つと https://maosugiyama.github.io/materials/russian-course/ が公開されます

## 動作確認

- 上のURLを開くとパスワード入力画面(ワインレッドのボタン)が出ます
- パスワード **nekoneko2026** を入力 → 資料一覧が表示されます
- 「このブラウザで記憶する」にチェックすると30日間は再入力不要です

## しくみと注意(だいじ)

- ページはAES-256で暗号化されており、パスワードなしに中身(資料一覧)は読めません。
  検索エンジンにも中身は載りません(noindex + 暗号化)。
- ただし **PDFファイル自体は暗号化していない**ので、PDFの直接URLを知っている人は
  開けます(受講生が一度アクセスすればURLは分かります)。また、GitHubリポジトリを
  直接見に来た人はファイルを取得できます。「授業資料の緩やかな保護」としては十分ですが、
  厳密な機密には向きません。より堅くしたい場合はPDF自体への開封パスワード設定も
  できますので、お申し付けください。
- **src/ フォルダは絶対にアップロードしないでください**(平文の一覧ページが
  入っているため、上げるとパスワードの意味がなくなります)。

## あとから編集したいとき

1. `src/list_source.html` を編集(資料の追加・文言変更など)
2. StatiCryptで再暗号化してください。コマンド:

```bash
npx staticrypt src/list_source.html -p "nekoneko2026" -d out \
  --template-title "教材ページ ― 読んで学ぶ ロシアのことばと文化" \
  --template-instructions "受講生のみなさんへ：授業でお伝えしたパスワードを入力してください。Пароль, пожалуйста!" \
  --template-button "開く" --template-placeholder "パスワード" \
  --template-color-primary "#7a2a37" --template-color-secondary "#e8e4dc" \
  --template-remember "このブラウザで記憶する" --remember 30 --short
```

3. できあがった `out/list_source.html` を `index.html` に改名して差し替え

もちろん、編集内容を私に伝えていただければ、こちらで再暗号化までやってお渡しします。

## パスワードを変えたいとき

上のコマンドの `-p "nekoneko2026"` を新しいパスワードに変えて再暗号化し、
`index.html` を差し替えるだけです(PDFはそのままでOK)。

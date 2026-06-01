#!/usr/bin/env python3
"""
classroom-tool 第7回プロンプト実験を5プロンプト構成に更新するスクリプト
~/Desktop/classroom-tool/ で実行してください
"""

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# ── ① ステップタイトルを「比較する」に変更 ──
html = html.replace(
    "{title:'演習③\u3000プロンプトで遊ぶ',badge:'AI実験',minutes:15,type:'prompt7'}",
    "{title:'演習③\u3000プロンプトで比較する',badge:'AI実験',minutes:20,type:'prompt7'}"
)
# 討議は10→5分減らさず元に戻す
# 全体時間調整: 共有・まとめを5分に
print("✓ ステップタイトル更新（遊ぶ→比較する）")

# ── ② プロンプト実験ステップを5プロンプト構成に再構築 ──

# 既存のプロンプト実験ステップを削除
import re
old_prompt_step = re.search(
    r"    case 'prompt7': return `[\s\S]*?</div>`;\n",
    html
)
if old_prompt_step:
    new_prompt_step = """    case 'prompt7': return `
      <div class="src-box"><div class="src-lbl">元テキスト（コピーして使ってください）</div><div class="src-text" id="prompt-src">${SOURCE_TEXT}</div><div class="src-chars">文字数：${SOURCE_TEXT.length}字</div></div>

      <h4 style="font-family:'Noto Serif JP',serif;font-size:1rem;margin-top:24px;margin-bottom:10px;color:var(--ink);">使う生成AIを開きましょう（無料版）</h4>
      <div class="ai-links">
        <a class="ai-link chatgpt" href="https://chatgpt.com" target="_blank" rel="noopener"><span class="ai-link-icon">G</span>ChatGPT を開く</a>
        <a class="ai-link gemini"  href="https://gemini.google.com" target="_blank" rel="noopener"><span class="ai-link-icon">✦</span>Gemini を開く</a>
      </div>
      <div class="ai-note">どちらか好きなほうを使ってください。アカウントを持っていない場合は、Googleアカウント等で無料登録できます。ログインせずに使えるサービスもあります。</div>

      <h4 style="font-family:'Noto Serif JP',serif;font-size:1.05rem;margin-bottom:8px;color:var(--ink);">プロンプトで比較する</h4>
      <p style="font-size:.85rem;color:var(--muted);margin-bottom:20px;line-height:1.75;">下のプロンプトを<strong>コピー</strong>→AIに貼り付け→<strong>続けて元テキストを貼り付け</strong>→出力をテキスト欄に貼ってください。プロンプトによって、要約の語彙・表現・強調がどう変わるかを観察します。</p>

      <div class="prompt-group-label">A ─ 読み手を変える <span class="prompt-group-sub">語彙と表現の変化を観察</span></div>
      <div class="prompt-list">
        <div class="prompt-card">
          <div class="prompt-card-hd"><span class="prompt-card-num">A-1</span><span class="prompt-card-label">小学生向け</span><button class="prompt-copy-btn" onclick="copyPrompt(this,'pA1')">コピー</button></div>
          <div class="prompt-text-box" id="pA1">以下の文章を、小学校高学年の子どもにもわかるように、やさしい言葉で50字以内に要約してください。難しい漢字や専門用語は使わないでください。</div>
          <textarea class="prompt-result-area" data-id="prompt7-A1" placeholder="AIの出力をここに貼り付けてください…"></textarea>
        </div>

        <div class="prompt-card">
          <div class="prompt-card-hd"><span class="prompt-card-num">A-2</span><span class="prompt-card-label">中学生向け</span><button class="prompt-copy-btn" onclick="copyPrompt(this,'pA2')">コピー</button></div>
          <div class="prompt-text-box" id="pA2">以下の文章を、中学生にもわかるように50字以内で要約してください。</div>
          <textarea class="prompt-result-area" data-id="prompt7-A2" placeholder="AIの出力をここに貼り付けてください…"></textarea>
        </div>

        <div class="prompt-card">
          <div class="prompt-card-hd"><span class="prompt-card-num">A-3</span><span class="prompt-card-label">大学生・専門家向け</span><button class="prompt-copy-btn" onclick="copyPrompt(this,'pA3')">コピー</button></div>
          <div class="prompt-text-box" id="pA3">以下の文章を、大学生や専門家向けに、専門的な語彙や抽象的な概念を含めて100字程度で要約してください。</div>
          <textarea class="prompt-result-area" data-id="prompt7-A3" placeholder="AIの出力をここに貼り付けてください…"></textarea>
        </div>
      </div>

      <div class="prompt-group-label" style="margin-top:24px;color:var(--sage);">B ─ 強調を変える <span class="prompt-group-sub">語の選択と価値判断を観察</span></div>
      <div class="prompt-list">
        <div class="prompt-card">
          <div class="prompt-card-hd"><span class="prompt-card-num" style="color:var(--sage)">B-1</span><span class="prompt-card-label">便利さを強調</span><button class="prompt-copy-btn" onclick="copyPrompt(this,'pB1')">コピー</button></div>
          <div class="prompt-text-box" id="pB1">以下の文章を、生成AIの便利さを強調する形で80字に要約してください。</div>
          <textarea class="prompt-result-area" data-id="prompt7-B1" placeholder="AIの出力をここに貼り付けてください…"></textarea>
        </div>

        <div class="prompt-card">
          <div class="prompt-card-hd"><span class="prompt-card-num" style="color:var(--sage)">B-2</span><span class="prompt-card-label">注意点を強調</span><button class="prompt-copy-btn" onclick="copyPrompt(this,'pB2')">コピー</button></div>
          <div class="prompt-text-box" id="pB2">以下の文章を、生成AIへの注意点を強調する形で80字に要約してください。</div>
          <textarea class="prompt-result-area" data-id="prompt7-B2" placeholder="AIの出力をここに貼り付けてください…"></textarea>
        </div>
      </div>

      <div class="disc-card" style="margin-top:24px"><h4>観察のポイント</h4><ul><li><strong>A群（読み手）</strong>：語彙の難易度・文の長さ・表現の柔らかさはどう変わったか</li><li><strong>A群</strong>：「読み手に合わせる」とき、AIは何を犠牲にしたか（情報量／正確さ／ニュアンス）</li><li><strong>B群（強調）</strong>：同じ事実なのに、読後の印象はどう変わったか</li><li><strong>B群</strong>：消えた情報・追加された語に注目してみよう</li><li>5つを並べたとき、「中立な要約」はあると言えるか</li></ul></div>`;
"""
    html = html[:old_prompt_step.start()] + new_prompt_step + html[old_prompt_step.end():]
    print("✓ プロンプト実験ステップを5プロンプト構成に更新")
else:
    print("⚠ 既存プロンプト実験ステップが見つかりません")

# ── ③ グループ見出し用CSS追加 ──
group_css = """
.prompt-group-label{font-family:'Noto Serif JP',serif;font-size:.95rem;font-weight:600;color:var(--terra);margin-bottom:12px;padding-bottom:6px;border-bottom:1px solid var(--border);display:flex;align-items:baseline;gap:10px;}
.prompt-group-sub{font-family:'Noto Sans JP',sans-serif;font-size:.7rem;font-weight:400;color:var(--light);letter-spacing:.05em;}
"""
if ".prompt-group-label" not in html:
    html = html.replace(".prompt-list{display:flex;flex-direction:column;gap:16px;}",
                        group_css + ".prompt-list{display:flex;flex-direction:column;gap:16px;margin-bottom:8px;}")
    print("✓ グループ見出しCSS追加")
else:
    print("⚠ グループ見出しCSSはすでに追加済み")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("\n=== 全ての修正完了 ===")
print("git add . && git commit -m '第7回プロンプト実験を5プロンプト構成に更新' && git push でデプロイ")

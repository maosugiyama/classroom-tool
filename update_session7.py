#!/usr/bin/env python3
"""
classroom-tool index.html に第7回プロンプト実験ステップを追加するスクリプト
~/Desktop/classroom-tool/ で実行してください
"""

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# ── ① SESSION 7 のステップ配列を更新 ──
old_steps = "steps:[{title:'導入',badge:'導入',minutes:10,type:'intro7'},{title:'ミニ講義',badge:'ミニ講義',minutes:15,type:'lecture7'},{title:'演習①\u3000自分で要約する',badge:'個人演習',minutes:15,type:'sum7a'},{title:'演習②\u3000要約を比較する',badge:'比較演習',minutes:20,type:'sum7b'},{title:'グループ討議',badge:'討議',minutes:15,type:'disc7'},{title:'共有・まとめ',badge:'まとめ',minutes:15,type:'ref7'}]"

new_steps = "steps:[{title:'導入',badge:'導入',minutes:10,type:'intro7'},{title:'ミニ講義',badge:'ミニ講義',minutes:15,type:'lecture7'},{title:'演習①\u3000自分で要約する',badge:'個人演習',minutes:15,type:'sum7a'},{title:'演習②\u3000要約を比較する',badge:'比較演習',minutes:15,type:'sum7b'},{title:'演習③\u3000プロンプトで遊ぶ',badge:'AI実験',minutes:15,type:'prompt7'},{title:'グループ討議',badge:'討議',minutes:10,type:'disc7'},{title:'共有・まとめ',badge:'まとめ',minutes:10,type:'ref7'}]"

if old_steps in html:
    html = html.replace(old_steps, new_steps)
    print("✓ ステップ配列を更新")
else:
    print("⚠ ステップ配列の更新箇所が見つかりません（すでに更新済みかも）")

# ── ② プロンプト実験ステップ用のCSSを追加 ──
prompt_css = """
/* ── PROMPT EXPERIMENT ── */
.ai-links{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px;}
.ai-link{display:inline-flex;align-items:center;gap:8px;padding:9px 16px;border-radius:100px;border:1.5px solid var(--border);background:var(--surface);color:var(--ink);text-decoration:none;font-family:'Noto Sans JP',sans-serif;font-size:.85rem;font-weight:500;transition:all .2s;}
.ai-link:hover{border-color:var(--terra);background:var(--terra-l);}
.ai-link.chatgpt{}
.ai-link.gemini{}
.ai-link-icon{width:18px;height:18px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Jost',sans-serif;font-size:.7rem;font-weight:700;flex-shrink:0;color:#fff;}
.ai-link.chatgpt .ai-link-icon{background:#10a37f;}
.ai-link.gemini .ai-link-icon{background:#4285f4;}
.ai-note{background:var(--bg);border-left:3px solid var(--gold);padding:10px 14px;font-size:.82rem;color:var(--muted);line-height:1.7;margin-bottom:24px;border-radius:4px;}
.prompt-list{display:flex;flex-direction:column;gap:16px;}
.prompt-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:16px 18px;}
.prompt-card-hd{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px;}
.prompt-card-num{font-family:'Jost',sans-serif;font-size:.7rem;letter-spacing:.15em;color:var(--terra);font-weight:600;}
.prompt-card-label{font-family:'Noto Serif JP',serif;font-size:.95rem;font-weight:600;color:var(--ink);flex:1;}
.prompt-copy-btn{font-family:'Jost',sans-serif;font-size:.7rem;letter-spacing:.06em;padding:4px 10px;border-radius:100px;border:1.5px solid var(--border);background:none;cursor:pointer;color:var(--muted);transition:all .15s;}
.prompt-copy-btn:hover{border-color:var(--terra);color:var(--terra);}
.prompt-copy-btn.copied{background:var(--sage);border-color:var(--sage);color:#fff;}
.prompt-text-box{background:var(--bg);padding:10px 14px;border-radius:4px;font-family:'Noto Sans JP',sans-serif;font-size:.83rem;color:var(--ink);line-height:1.7;margin-bottom:10px;border:1px dashed var(--border);}
.prompt-result-area{width:100%;min-height:70px;padding:10px 12px;border:1px solid var(--border);border-radius:6px;font-family:'Noto Sans JP',sans-serif;font-size:.85rem;line-height:1.7;background:var(--bg);resize:vertical;}
.prompt-result-area:focus{outline:none;border-color:var(--terra);}
"""

if ".prompt-card{" not in html:
    html = html.replace("/* ── STEP FOOTER NAV ── */", prompt_css + "\n/* ── STEP FOOTER NAV ── */")
    print("✓ プロンプト実験CSS追加")
else:
    print("⚠ プロンプト実験CSSはすでに追加済み")

# ── ③ プロンプト実験ステップのレンダリング関数を追加 ──
prompt_step_case = """    case 'prompt7': return `
      <div class="src-box"><div class="src-lbl">元テキスト（コピーして使ってください）</div><div class="src-text" id="prompt-src">${SOURCE_TEXT}</div><div class="src-chars">文字数：${SOURCE_TEXT.length}字</div></div>

      <h4 style="font-family:'Noto Serif JP',serif;font-size:1rem;margin-top:24px;margin-bottom:10px;color:var(--ink);">使う生成AIを開きましょう（無料版）</h4>
      <div class="ai-links">
        <a class="ai-link chatgpt" href="https://chatgpt.com" target="_blank" rel="noopener"><span class="ai-link-icon">G</span>ChatGPT を開く</a>
        <a class="ai-link gemini"  href="https://gemini.google.com" target="_blank" rel="noopener"><span class="ai-link-icon">✦</span>Gemini を開く</a>
      </div>
      <div class="ai-note">どちらか好きなほうを使ってください。アカウントを持っていない場合は、Googleアカウント等で無料登録できます。ログインせずに使えるサービスもあります。</div>

      <h4 style="font-family:'Noto Serif JP',serif;font-size:1rem;margin-bottom:14px;color:var(--ink);">同じ文章に、違うプロンプトを試してみよう</h4>
      <p style="font-size:.85rem;color:var(--muted);margin-bottom:18px;line-height:1.75;">下のプロンプトを<strong>コピー</strong>→AIに貼り付け→<strong>続けて元テキストを貼り付け</strong>→出力をテキスト欄に貼ってください。プロンプトによって、同じ文章からどれだけ違う要約が生まれるかを観察します。</p>

      <div class="prompt-list">
        <div class="prompt-card">
          <div class="prompt-card-hd"><span class="prompt-card-num">PROMPT 01</span><span class="prompt-card-label">そのまま要約</span><button class="prompt-copy-btn" onclick="copyPrompt(this,'p1')">コピー</button></div>
          <div class="prompt-text-box" id="p1">以下の文章を80字で要約してください。</div>
          <textarea class="prompt-result-area" data-id="prompt7-r1" placeholder="AIの出力をここに貼り付けてください…"></textarea>
        </div>

        <div class="prompt-card">
          <div class="prompt-card-hd"><span class="prompt-card-num">PROMPT 02</span><span class="prompt-card-label">読者を変える</span><button class="prompt-copy-btn" onclick="copyPrompt(this,'p2')">コピー</button></div>
          <div class="prompt-text-box" id="p2">以下の文章を、中学生にもわかるように50字で要約してください。</div>
          <textarea class="prompt-result-area" data-id="prompt7-r2" placeholder="AIの出力をここに貼り付けてください…"></textarea>
        </div>

        <div class="prompt-card">
          <div class="prompt-card-hd"><span class="prompt-card-num">PROMPT 03</span><span class="prompt-card-label">強調を変える（便利さ寄り）</span><button class="prompt-copy-btn" onclick="copyPrompt(this,'p3')">コピー</button></div>
          <div class="prompt-text-box" id="p3">以下の文章を、生成AIの便利さを強調する形で80字に要約してください。</div>
          <textarea class="prompt-result-area" data-id="prompt7-r3" placeholder="AIの出力をここに貼り付けてください…"></textarea>
        </div>

        <div class="prompt-card">
          <div class="prompt-card-hd"><span class="prompt-card-num">PROMPT 04</span><span class="prompt-card-label">強調を変える（注意喚起寄り）</span><button class="prompt-copy-btn" onclick="copyPrompt(this,'p4')">コピー</button></div>
          <div class="prompt-text-box" id="p4">以下の文章を、生成AIの利用に対する注意点を強調する形で80字に要約してください。</div>
          <textarea class="prompt-result-area" data-id="prompt7-r4" placeholder="AIの出力をここに貼り付けてください…"></textarea>
        </div>
      </div>

      <div class="disc-card" style="margin-top:24px"><h4>観察のポイント</h4><ul><li>4つの要約で「残った情報」と「消えた情報」はどう違ったか</li><li>プロンプトの違いは、何を残し何を消すかにどう影響したか</li><li>同じ文章なのに、印象は変わりましたか</li><li>これが意味することは何か——AIの「中立」をどう考えるか</li></ul></div>`;
"""

# disc7 の case の直前に挿入
disc7_marker = "    case 'disc7': return `"
if "case 'prompt7'" not in html:
    html = html.replace(disc7_marker, prompt_step_case + "\n" + disc7_marker)
    print("✓ プロンプト実験ステップ追加")
else:
    print("⚠ プロンプト実験ステップはすでに追加済み")

# ── ④ コピー機能のJS関数を追加 ──
copy_fn = """
function copyPrompt(btn, id){
  const text = document.getElementById(id).textContent;
  navigator.clipboard.writeText(text).then(()=>{
    btn.textContent='コピーしました';
    btn.classList.add('copied');
    setTimeout(()=>{btn.textContent='コピー';btn.classList.remove('copied');},1800);
  });
}
"""

if "function copyPrompt" not in html:
    # render() 関数の前に挿入
    html = html.replace("function render(){", copy_fn + "\nfunction render(){")
    print("✓ コピー機能JS追加")
else:
    print("⚠ コピー機能JSはすでに追加済み")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("\n=== 全ての修正完了 ===")
print("git add . && git commit -m '第7回プロンプト実験ステップ追加' && git push でデプロイ")

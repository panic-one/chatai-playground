# chatai-playground

AIとチャットできるアプリケーション（ChatGPTみたいなやつ）。

ただし、以下に示す追加の要件がある。

## 要件
- 様々なLLMを使えるチャットアプリにする
  - GPT、Gemini、Cloude、Llama、国産LLM
- ユーザーがLLMモデルを選択できる
- プロンプトに応じて、自動で最適なLLMモデルを選択する
  - コストと品質の観点
  - 例：簡単な入力なら弱いモデルで、難しい入力なら強いモデルで
- チャット履歴をスレッドごとに保存できる
- スレッドを一覧できる
- （Optional）OSSのLLMも追加できるようにする


### 現在の進捗
https://github.com/user-attachments/assets/032ed0ec-d263-47bc-b270-1adb362a7844
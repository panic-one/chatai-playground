# chatai-playground

AIとチャットできるアプリケーション（ChatGPTみたいなやつ）。

ただし、以下に示す追加の要件がある。

## 要件
- 様々なLLMを使えるチャットアプリにする
  - GPT、Gemini、Claude、Llama、国産LLM
- ユーザーがLLMモデルを選択できる
- プロンプトに応じて、自動で最適なLLMモデルを選択する
  - コストと品質の観点
  - 例：簡単な入力なら弱いモデルで、難しい入力なら強いモデルで
- チャット履歴をスレッドごとに保存できる
- スレッドを一覧できる
- （Optional）OSSのLLMも追加できるようにする


### 現在の進捗
https://github.com/user-attachments/assets/a93744b5-8182-4dd5-8003-b73f7e5f14e8

- GPT、Gemini、Cloude、DeepseekのLLMが使える
- ユーザーがLLMモデルを選択できる
- チャット履歴の保存ができる
- スレッド一覧ができる

### 現在の進捗2
https://github.com/user-attachments/assets/93a4317f-40f6-40e1-9ec8-387f39f35866

- ユーザーはLLMのProviderを選択し、モデルは分析結果に基づいて選択する方法に変更
- Provider選択をautoにしていた場合、分野ごとに最適なmodelになるようにproviderを決定する

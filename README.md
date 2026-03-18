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


- GPT、Gemini、Cloude、DeepseekのLLMが使える
- ユーザーがLLMモデルを選択できる
- チャット履歴の保存ができる
- スレッド一覧ができる

### 現在の進捗2
https://github.com/user-attachments/assets/708a6ecd-2363-46e4-b4dc-4cf586605da3

- ユーザーはLLMのProviderを選択し、モデルは分析結果に基づいて選択する方法に変更
- Provider選択をautoにしていた場合、分野ごとに得意なmodelになるようにprovider選択をする

# Deltaria Posters

Cafe & Bar Deltariaのワールドで表示するポスターです。

[ポスター一覧](https://taki98029.github.io/deltaria-posters/)

## 画像を追加するだけで掲載

1. [images/posters/main](https://github.com/taki98029/deltaria-posters/tree/main/images/posters/main) にPNG/JPG/JPEG/WebPをUploadしてCommitするか、ローカルで追加してmainへPushします。
2. GitHubのActionsで **Publish posters** が緑になるまで待ちます。通常数分です。
3. [公開一覧](https://taki98029.github.io/deltaria-posters/)で画像を確認し、ワールドへ入り直します。既存インスタンスに滞在中の表示は自動更新しません。

指定フォルダ直下の対応画像がすべて対象です。画像URLやJSONの手動登録は不要です。サブフォルダと `images/posters/old/` は対象外です。削除・oldへ移動してPushすると掲載から外れます。画像の原本は変えず、配信用コピーを長辺2048px以下へ自動縮小します。アニメーション画像は先頭フレームのみ表示します。

並び順はDeltaria案内 `poster.png` → 募集 `recruitment.png` → その他のファイル名順です。その他の順序を指定したい場合は `01_`、`02_` などを名前の先頭に付けます。現在の3枚目は `TVSEA.png`。

ワールドの受付ボードとメニュー6冊は6秒表示、Fade1.2秒、初期AUTO ON。PREV／AUTO／NEXTで本人の表示を切り替えます。導入済みSceneを最初に一度VRChatへ再アップロードする必要があります。その後は64枚以内の追加・削除・差し替えにワールド再アップロードは不要です。

## 制限・失敗時

- 1～64枚。0枚・65枚以上・破損画像は公開を止め、直前に成功した公開内容を保持します。Actionsのエラーを確認し修正してPushしてください。
- GitHub Pagesの反映・キャッシュにより時間差があります。公開一覧を確認してからワールドへ入り直してください。
- 受付とメニューは本人の表示で連動します。参加者間の再生時刻は同期しません。
- 募集ポスターの編集元は `poster-recruitment.html`。HTMLだけを編集しても画像は更新されないので、PNGを書き出して `images/posters/main/recruitment.png` へ反映してください。相談先は「キャスト or 公式XアカウントのDMまで」。
- EBKウィザードを全体再適用すると独自の受付レイアウトが戻る可能性があります。日常のポスター更新にウィザード操作は不要です。

## 配信の仕組み

`tools/build_posters.py` がフォルダを列挙し、EBK標準の64個の固定URL `images/slide-posters/<boardIdのSHA-256>/slot0.png` ～ `slot63.png` と `data/slide_poster_manifest.json` を生成します。配信リストが有効な画像と表示順を決めます。生成物はGitHub Pagesへ一括デプロイされ、mainへ生成物を書き戻しません。旧slot0～2のURLは再アップロード前のワールド用に配信時のみ維持しますが、現行の巡回には含めません。

ローカル検査：`python -m pip install -r requirements.txt` → `python -m unittest discover -s tools` → `python tools/build_posters.py`。出力 `_site/` は未作成の状態で実行します。通常の画像追加にこの操作は不要です。

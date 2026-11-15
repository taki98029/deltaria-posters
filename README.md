# Deltaria Posters

VRChatワールドのEBKポスター表示を試すための画像置き場です。
3枚ともAI生成の架空イベント画像であり、実際の開催告知ではありません。

[ポスター一覧を開く](https://taki98029.github.io/deltaria-posters/)

## 画像URL

| 番号 | タイトル | EBKの「外部画像URL」に入れるURL |
|---|---|---|
| 01 | MOONLIT READING | https://taki98029.github.io/deltaria-posters/images/posters/main/slot0.png |
| 02 | GARDEN TEA TIME | https://taki98029.github.io/deltaria-posters/images/posters/main/slot1.png |
| 03 | MIDNIGHT JAZZ | https://taki98029.github.io/deltaria-posters/images/posters/main/slot2.png |

各画像は1024×1536 pxのPNGです。画像内の番号は01〜03、ファイル名はEBKのスロット規約に合わせて0始まりです。

## EBKでの最小設定

1. Wizardの「商品・案内」→「ポスター・表示板」→「相互ポスター」で「画像URLも使用」をONにします。
2. 「相互ポスターを追加」で3件作り、タイトルと上の外部画像URLを1件ずつ入力します。ローカル画像は未指定で構いません。
3. 説明には「架空イベントの表示テスト」と記入し、案内先グループURLは空欄にします。
4. 表示に使うギャラリーやボードを設定し、「確認・適用」からSceneへ反映します。
5. 初回のワールド反映・アップロード後、VRChatで画像の読込を確認します。

このリポジトリは画像配信用です。EBKのOPSや名簿・スライドManifest一式は含みません。上のURLを各ポスターへ直接指定する方式で使えます。EBK全体のGitHub連携を後から設定する場合、生成されるデータや画像がこのテスト画像を上書きしないよう確認してください。

## 画像の差し替え

`images/posters/main/slot0.png`〜`slot2.png`を同じファイル名で差し替え、mainブランチへ保存します。GitHub Pagesの公開が完了してから確認してください。ワールド側のURLが同じなら、画像だけの更新のためにワールドを再アップロードする必要はありません。読込済みの画像が残る場合は、EBKの外部画像再読込・新しいインスタンスへの入り直しで確認します。

このリポジトリと画像は公開されています。実際の他イベント画像を置くときは、公開掲載用に提供された画像へ差し替えてください。

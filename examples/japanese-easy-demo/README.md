<!-- markdownlint-disable MD013 MD043 -->

# OpenSSA sample

## ライブラリインストール(初回のみ)

```bash
poetry install
```

## 実行前手順

- `.env.template`をコピーして`.env`ファイルを作成し、ファイル内の環境変数を記載する
- `.data` ディレクトリを作成して、そこに回答の情報となるPDFファイルを配置する

## メモ

- 初回実行時に `.data` 内に `.indexes` ディレクトリが作成されインデックスが配置される
- 初回はその分実行に時間がかかる

## 実行

```bash
poetry run python main.py
```

# pentatonics
- 本ツールは書籍「[インサイド・インプロヴィゼイション・シリーズ Vol.2 ペンタトニックスケール](https://amzn.asia/d/cQaBhfx)」のエクササイズを行うアプリです。

## 機能
- コンソール上にminor7thコードと対応するペンタトニックスケールをランダムに表示します。
- MIDIデバイスでノーツを入力できます。
- ペンタトニックスケールの5つの音が入力されたら(入力順は問わない)、次のコードを表示します

## インストール
- 最新バージョンのchordis.zipを[ここ](https://github.com/shuntacurosu/chordis/releases)からダウンロードしてください。
- ダウンロードしたzipファイルを解凍してください。
- 解凍したフォルダ内のchordis.batを実行するとアプリケーションが起動します。

## 使い方
### 基本操作
- MIDIキーボードをPCに接続します。
- chordis.batを実行します。タスクトレイにアイコンが表示されます。
- 設定画面/Chord画面でMIDI入力機器, MIDI出力機器を選択してください。
- MIDIキーボードで和音を演奏します。ディスプレイ左上に和音名が表示されます。
- 終了するときはタスクトレイのアイコンを右クリックし、「quit」を選択します。

## 開発
### 開発環境
- Python 3.10.10
- requirements.txtでライブラリをインストールしてください。
    ```
    $ pip install -r requirements.txt
    ```

### 再配布用zipファイル作成
- make.pyを実行してください。
    ```
    $ python make.py
    ```
- make.pyでは以下の処理が行われます。
    1. 作業ディレクトリ直下(pentatonics)にpentatonicsフォルダを作成します。
    1. pentatonics/pentatonics/envフォルダにPython Embeddable環境を作成します。
    1. mainブランチをpentatonics/pentatonics/envフォルダにpullします。
    1. pentatonics/pentatonics/execute.bat(実行用bat)を配置します。
    1. pentatonics/requirements.txtを読み込み、pentatonics/pentatonicsに必要なライブラリをインストールします。
    1. pentatonics/pentatonics/__pycache__を削除します。
    1. pentatonics/pentatonics/.gitを削除します(Y/N選択有り)
- make.pyを再度実行する場合、作成されたchordisフォルダとchordis.zipは削除してください。

## ライセンス
このプロジェクトはGNU General Public License v3.0のもとで公開されています。詳細は[LICENSE](https://github.com/shuntacurosu/chordis/blob/main/LICENSE)を参照してください

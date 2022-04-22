# kot_working_hours
勤務時間の取得

## 事前準備
* GoogleChromをインストール
* 下記を参考にPython3系をインストール
    <http://netsu-n.mep.titech.ac.jp/~Kawaguchi/python/install-win/>
* コマンドラインで以下をインストール
    ``` pip install selenium ```
    ``` pip install chromedriver-binary ```
    ``` pip install webdriver_manager ```
    ``` pip install requests ```

## 実行手順
1. working_hours.pyにキングオブタイムのID、パスワードを入力する
2. コマンドラインで以下を実行する
    ``` python working_hours.py ```
3. 自動的にGoogleChromeが起動し、スプレッドシートへの書き込みが行われる
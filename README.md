# kot_working_hours
1か月分の勤務時間を取得する

## 事前準備
* GoogleChromをインストール
* 下記を参考にPython3系をインストール
    * windowsの場合（どちらかを参考にしてください）
        * <https://www.python.jp/install/windows/install.html>
        * <http://netsu-n.mep.titech.ac.jp/~Kawaguchi/python/install-win/>
    * macの場合
        * <http://netsu-n.mep.titech.ac.jp/~Kawaguchi/python/install-mac/>
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
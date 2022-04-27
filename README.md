# kot_working_hours
1か月分の勤務時間を取得する

## 事前準備
* GoogleChromをインストールする
* 勤務時間を反映させたいスプレッドシートを作成する
    * スプレッドシートの「拡張機能」から「Apps Script」を開く
        * ![](/images/sheet_1.png)
    * 既存の myFunction() を削除し、以下のコードを入力する
        * ```
        function doPost(e) {
            // スプレッドシートへの書き込み
            var id = "スプレッドシートID"
            var ss = SpreadsheetApp.openById(id)
            var spread = SpreadsheetApp.getActiveSpreadsheet();
            var lastRow = spread.getSheets()[0].getLastRow();
            spread.getSheets()[0].getRange((lastRow + 1), 1).setValue(e.parameter.day);
            spread.getSheets()[0].getRange((lastRow + 1), 2).setValue(e.parameter.day_schedule);
            spread.getSheets()[0].getRange((lastRow + 1), 3).setValue(e.parameter.start_work);
            spread.getSheets()[0].getRange((lastRow + 1), 4).setValue(e.parameter.end_work);
            spread.getSheets()[0].getRange((lastRow + 1), 5).setValue(e.parameter.start_break);
            spread.getSheets()[0].getRange((lastRow + 1), 6).setValue(e.parameter.end_break);
        }
        ```
    * コード内の「スプレッドシートID」を作成したスプレッドシートのIDに変更する
        * https://docs.google.com/spreadsheets/d/[ここにIDが存在]/edit
    * 変更が完了したら保存する
        *  ![](/images/sheet_2.png)
    * デプロイから新しいデプロイを選択する
        * ![](/images/sheet_3.jpg)
    * 歯車マークからウェブアプリを選択し、「アクセスできるユーザー」を「全員」に変更してデプロイを押下する
        * ![](/images/sheet_4.jpg)
    * 表示されたURLをコピーして「実行手順4」に入力する
        * ![](/images/sheet_5.jpg)
* 下記を参考にPython3系をインストールする
    * windowsの場合（どちらかを参考にする）
        * <https://www.python.jp/install/windows/install.html>
        * <http://netsu-n.mep.titech.ac.jp/~Kawaguchi/python/install-win/>
    * macの場合
        * <http://netsu-n.mep.titech.ac.jp/~Kawaguchi/python/install-mac/>
* コマンドプロンプトで以下を実行する（1行ずつ実行する）
    * ``` pip install selenium ```
    * ``` pip install chromedriver-binary ```
    * ``` pip install webdriver_manager ```
    * ``` pip install requests ```

## 実行手順
1. user_idにKING OF TIME の ID を入力する
2. my_passにKING OF TIME の パスワード を入力する
3. range_startとrange_endの各項目を入力する（月初から月末の場合は変更なしでOK）
4. 事前準備で用意したApps ScriptのURLを入力する
5. ファイルを保存してターミナルを起動し、以下のコマンドを実行する
    * ``` python working_hours.py ```
5. 自動的にGoogleChromeが起動し、スプレッドシートへの書き込みが行われる
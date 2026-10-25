# todo.py の説明

このアプリは、タスクをリストに溜めて、メニューの番号で「追加」「状態変更」「終了」を繰り返すプログラムです。画面に出す文字列を作る関数と、データを書き換える関数が分かれています。

## データの置き場所

```python
# タスクの入れ物。1件は次のような辞書。
# {"name": "牛乳を買う", "status": "未了"}
tasks = []

# 選べる状態。表示もこの順番にする。
STATUSES = ("未了", "完了", "キャンセル")
```

`tasks` はタスク全体のリストです。最初は空の `[]` で、追加するたびに辞書が1件増えます。1件の中身は次の2つだけです。

- `name` … タスクの文章
- `status` … `"未了"` `"完了"` `"キャンセル"` のどれか

たとえば2件入っているときは、こうなります。

```python
tasks = [
    {"name": "牛乳を買う", "status": "完了"},
    {"name": "メールを送る", "status": "未了"},
]
```

`STATUSES` は選べる状態を並べたタプルです。メニューの「1. 未了、2. 完了、3. キャンセル」はこの並びをそのまま使っています。状態の名前をここだけに書いておけば、表示と入力チェックが同じリストを参照します。

ファイル先頭の `"""..."""` は、このファイルが何をするかの説明文です。プログラムの動作には影響しません。`import sys` は、あとで「画面に出せる文字の種類」を調べるために、Python 標準の `sys` を読み込んでいます。

## `with_strike`：取り消し線を付ける

```python
def with_strike(text):
    """完了・キャンセル用に、文字へ取り消し線を付ける。"""
    struck = "".join(char + "\u0336" for char in text)
    encoding = sys.stdout.encoding or "utf-8"
    try:
        struck.encode(encoding)
    except UnicodeEncodeError:
        return f"~~{text}~~"
    return struck
```

引数 `text` は、線を引きたい文字列です。`"牛乳"` のような普通の文字列が渡されます。

`for char in text` は、文字列を1文字ずつ取り出す書き方です。`"牛乳"` なら `"牛"` と `"乳"` の2回回ります。各文字のうしろに `\u0336` を足します。これは「前の文字に横線を重ねる」という特殊な文字です。

`"".join(...)` は、ばらばらの文字を空文字 `""` でつないで1つの文字列に戻します。結果は `牛̶乳̶` のように見えます。

そのあと、今のターミナルがその線付き文字を表示できるかを調べています。`sys.stdout.encoding` は画面出力の文字コードです。`struck.encode(encoding)` で「その文字コードに変換できるか」を試し、できなければ `UnicodeEncodeError` になります。そのときは線の記号をやめて、`~~牛乳~~` のように前後を `~~` で囲んで返します。変換できれば、線付きの文字列を返します。

`return` は、この関数の結果を呼び出し元へ渡して、関数を終了します。

## `format_task`：1件を1行の文章にする

```python
def format_task(number, task):
    """1件を「番号. [状態] 内容」の1行にする。"""
    name = task["name"]
    status = task["status"]
    # 未了以外（完了・キャンセル）は線を引いて、ひと目で区別する。
    if status != "未了":
        name = with_strike(name)
    return f"  {number}. [{status}] {name}"
```

`number` は画面に出す番号、`task` は1件分の辞書です。`task["name"]` で文章、`task["status"]` で状態を取り出します。

状態が `"未了"` 以外、つまり完了かキャンセルのときだけ `with_strike` を呼び、`name` を線付きの文字列に差し替えます。未了のときはそのままです。

最後の `f"..."` は f文字列です。波かっこの中は変数の中身に置き換わります。`number` が `1`、`status` が `"完了"`、`name` が線付きの「牛乳を買う」なら、戻り値は次のような1行です。

```text
  1. [完了] 牛̶乳̶を̶買̶う̶
```

この関数は表示用の文字列を作るだけで、`tasks` の中身は変えません。

## `show_tasks`：一覧を全部表示する

```python
def show_tasks():
    """今あるタスクを全部表示する。"""
    print()
    print("--- タスク一覧 ---")
    if not tasks:
        print("  （まだタスクはありません）")
        print()
        return
    for number, task in enumerate(tasks, start=1):
        print(format_task(number, task))
    print()
```

最初の `print()` は空行です。見出しの前に1行空けています。

`if not tasks:` は「リストが空なら」です。空のリストは条件の中で偽になるので、`not` を付けると「空のとき」になります。そのときは案内を出して `return` します。`return` に値が無いので、ここで関数は終わり、下の `for` には進みません。

タスクがあるときは `for` で先頭から1件ずつ処理します。`enumerate(tasks, start=1)` は、リストの中身と番号を同時に出します。`start=1` なので番号は 1 から始まります。Python のリスト自体は 0 番から数えますが、画面の番号は人が見やすい 1 始まりにしています。

各件は `format_task` に渡して、返ってきた1行を `print` します。

## `add_task`：タスクを1件足す

```python
def add_task():
    """新しいタスクを「未了」で追加する。"""
    name = input("タスクの内容: ").strip()
    if name == "":
        print("内容が空なので、追加しませんでした。")
        return
    tasks.append({"name": name, "status": "未了"})
    print(f"追加しました: {name}")
```

`input(...)` はメッセージを出して、ユーザーが Enter を押すまで待ちます。入力された文字列が戻り値です。`.strip()` は前後の空白を取り除きます。スペースだけの入力は空文字 `""` になります。

空なら追加せず、メッセージを出して `return` で戻ります。

中身があれば `tasks.append(...)` でリストの末尾に辞書を足します。新しいタスクの状態は必ず `"未了"` です。`append` は既存のリストに要素を足す操作なので、`tasks = ...` とリスト自体を代入し直していません。この書き方なら、関数の中から外側の `tasks` をそのまま更新できます。

## `change_status`：番号を選んで状態を変える

この関数は、次の順で進みます。

1. タスクが無ければ中断する
2. 一覧を見せて、変える番号を聞く
3. 番号が正しいか調べる
4. 新しい状態を選ばせる
5. 選ばれた状態をそのタスクに書き込む

### タスク番号の受け取り

```python
def change_status():
    """番号でタスクを選び、状態を変える。"""
    if not tasks:
        print("タスクがありません。先に追加してください。")
        return

    show_tasks()
    number_text = input("状態を変えるタスクの番号: ").strip()
    if not number_text.isdigit():
        print("番号は数字で入力してください。")
        return

    index = int(number_text) - 1
    if index < 0 or index >= len(tasks):
        print("その番号のタスクはありません。")
        return
```

`input` の結果は常に文字列です。`"1"` であっても数値の `1` ではありません。`.isdigit()` は「1文字以上の数字だけか」を調べます。`"1"` は真、`"abc"` や `""` は偽です。数字でなければメッセージを出して戻ります。

`int(number_text)` で文字列を整数にします。画面の番号は 1 始まり、リストの位置は 0 始まりなので、1 を引いて `index` にします。ユーザーが `1` と入れたら `index` は `0` で、`tasks[0]` が最初のタスクです。

範囲の確認は2つです。

- `index < 0` … 位置として不正な番号です。
- `index >= len(tasks)` … リストの長さ以上です。3件しかないのに `9` を選ぶと、ここに当てはまります。`len(tasks)` は件数です。

### 状態の選択と書き込み

```python
    print("新しい状態を選んでください。")
    for index_in_menu, status in enumerate(STATUSES, start=1):
        print(f"  {index_in_menu}. {status}")
    choice = input("番号: ").strip()
    if not choice.isdigit():
        print("1, 2, 3 のいずれかを入力してください。")
        return

    choice_index = int(choice) - 1
    if choice_index < 0 or choice_index >= len(STATUSES):
        print("1, 2, 3 のいずれかを入力してください。")
        return

    tasks[index]["status"] = STATUSES[choice_index]
    print("状態を変更しました。")
    print(format_task(index + 1, tasks[index]))
```

状態のメニューも `STATUSES` を `enumerate` して出しています。並びは次のとおりです。

1. 未了
2. 完了
3. キャンセル

番号の検査はタスク番号のときと同じです。

通過したら、選んだタスクの `status` だけを書き換えます。`tasks[index]["status"] = ...` は、その辞書の `status` というキーを上書きします。`name` はそのままです。

`STATUSES` の中身と番号の対応は次のとおりです。

| ユーザーの入力 | `choice_index` | 入る状態 |
| --- | --- | --- |
| `1` | `0` | `"未了"` |
| `2` | `1` | `"完了"` |
| `3` | `2` | `"キャンセル"` |

最後に `format_task(index + 1, ...)` で、変えた直後の1行を表示します。`index` は 0 始まりなので、画面用には 1 を足して戻しています。

## `main`：メニューを繰り返す

```python
def main():
    print("ToDoアプリへようこそ。")
    while True:
        show_tasks()
        print("メニュー")
        print("  1. タスクを追加")
        print("  2. 状態を変更")
        print("  3. 終了")
        choice = input("番号を入力: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            change_status()
        elif choice == "3":
            print("終了します。")
            break
        else:
            print("1, 2, 3 のいずれかを入力してください。")
```

`while True:` は、条件が常に真なので、自分から抜けるまで同じブロックを繰り返します。1周の中身はいつも同じです。

1. 今の一覧を出す
2. メニューを出す
3. 番号を1つ受け取る
4. 番号に応じた関数を呼ぶ

`if` / `elif` / `else` は上から順に見て、最初に当てはまった枝だけを実行します。`"1"` なら `add_task`、`"2"` なら `change_status` です。呼び出された関数が `return` で終わると、また `while` の先頭に戻り、一覧が最新の内容で出ます。

`"3"` の `break` は、この `while` を抜けます。抜けたあとに `main` の続きは無いので、`main` も終わります。それ以外の入力は `else` に入り、案内を出して次の周に進みます。

## プログラムの起動

```python
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Ctrl+C でも途中で止まれるようにする。
        print()
        print("終了します。")
```

`python todo.py` でこのファイルを直接実行したとき、Python は `__name__` に `"__main__"` を入れます。そのときだけ `main()` が呼ばれ、アプリが始まります。

`try` の中で `main()` を動かしています。ユーザーが Ctrl+C を押すと `KeyboardInterrupt` という例外が起きます。`except` はそれを受け取って、空行と「終了します。」を出してプログラムを止めます。例外を捕まえないと、途中で止めたときに長いエラー表示が出ます。

## 1周の具体例

「牛乳を買う」を追加して、完了にするときの流れです。

1. `main` が `show_tasks` を呼ぶ。リストは空なので「まだタスクはありません」と出る。
2. ユーザーが `1` を入れる。`add_task` が `"牛乳を買う"` を受け取り、`tasks` は `[{"name": "牛乳を買う", "status": "未了"}]` になる。
3. `while` の先頭に戻る。`show_tasks` が `format_task(1, その辞書)` を呼び、`1. [未了] 牛乳を買う` と出る。未了なので線は付かない。
4. ユーザーが `2` を入れる。`change_status` が番号 `1` を受け取る。`index` は `0`。
5. 状態で `2` を選ぶ。`tasks[0]["status"]` が `"完了"` になる。
6. `format_task` は状態が未了ではないので `with_strike("牛乳を買う")` を呼び、線付きの1行を出す。
7. また `main` の一覧表示に戻り、同じ線付きの行が一覧にも出る。

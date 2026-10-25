"""かんたんなToDoアプリ（ターミナル版）

起動:
    python todo.py

できること:
    - タスクを追加する
    - 各タスクの状態を「未了」「完了」「キャンセル」から選ぶ
    - 「完了」と「キャンセル」は取り消し線付きで表示する
"""

import sys

# タスクの入れ物。1件は次のような辞書。
# {"name": "牛乳を買う", "status": "未了"}
tasks = []

# 選べる状態。表示もこの順番にする。
STATUSES = ("未了", "完了", "キャンセル")


def with_strike(text):
    """完了・キャンセル用に、文字へ取り消し線を付ける。

    各文字のうしろに「重ねて線を引く」記号（U+0336）を足している。
    ターミナルがその記号を出せないときは、前後を ~~ で囲む。
    """
    struck = "".join(char + "\u0336" for char in text)
    encoding = sys.stdout.encoding or "utf-8"
    try:
        struck.encode(encoding)
    except UnicodeEncodeError:
        return f"~~{text}~~"
    return struck


def format_task(number, task):
    """1件を「番号. [状態] 内容」の1行にする。"""
    name = task["name"]
    status = task["status"]
    # 未了以外（完了・キャンセル）は線を引いて、ひと目で区別する。
    if status != "未了":
        name = with_strike(name)
    return f"  {number}. [{status}] {name}"


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


def add_task():
    """新しいタスクを「未了」で追加する。"""
    name = input("タスクの内容: ").strip()
    if name == "":
        print("内容が空なので、追加しませんでした。")
        return
    tasks.append({"name": name, "status": "未了"})
    print(f"追加しました: {name}")


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


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Ctrl+C でも途中で止まれるようにする。
        print()
        print("終了します。")

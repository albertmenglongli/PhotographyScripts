import random

aperture_table = [
    ["f/1.4", "f/1.6", "f/1.8", "f/2.0"],
    ["f/2.0", "f/2.2", "f/2.5", "f/2.8"],
    ["f/2.8", "f/3.2", "f/3.5", "f/4.0"],
    ["f/4.0", "f/4.5", "f/5.0", "f/5.6"],
    ["f/5.6", "f/6.3", "f/7.1", "f/8.0"],
    ["f/8.0", "f/9.0", "f/10",  "f/11"],
    ["f/11",  "f/13",  "f/14",  "f/16"],
    ["f/16",  "f/18",  "f/20",  "f/22"],
    ["f/22",  "f/26",  "f/28",  "f/32"],
]

def normalize(value):
    value = value.lower().replace(" ", "").replace("f/", "")
    try:
        num = float(value)
        if num.is_integer():
            return f"f/{int(num)}"
        else:
            return f"f/{num}"
    except ValueError:
        return "invalid"

def ask_question(item):
    full1, third1, third2, full2 = item
    print(f"\n【题目】{full1} → {full2}，中间两档是？")
    answer = input("你的答案（用空格分隔）: ").strip()
    parts = answer.split()
    if len(parts) != 2:
        print("⚠️ 请输入两个数值，用空格分隔。")
        return False

    ans1, ans2 = normalize(parts[0]), normalize(parts[1])
    correct1, correct2 = normalize(third1), normalize(third2)
    correct = True

    if ans1 != correct1:
        print(f"✘ 第一个错误，正确是 {third1}")
        correct = False
    else:
        print("✔ 第一个正确")

    if ans2 != correct2:
        print(f"✘ 第二个错误，正确是 {third2}")
        correct = False
    else:
        print("✔ 第二个正确")

    if correct:
        print("✔ 正确！")
    return correct

def run_quiz():
    remaining = aperture_table.copy()
    random.shuffle(remaining)
    retry = []

    while remaining:
        current = remaining.pop(0)
        if not ask_question(current):
            retry.append(current)

        if not remaining and retry:
            print("\n📘 开始错题复习...")
            remaining = retry
            retry = []

    print("\n🎉 太棒了，全部答对，训练完成！")

if __name__ == "__main__":
    run_quiz()

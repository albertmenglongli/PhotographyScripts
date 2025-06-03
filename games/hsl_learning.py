import random
from collections import deque
import colorsys

# 色相环颜色字典（名称 → 色相角）
colors = {
    "红": 0,
    "橙": 30,
    "黄": 60,
    "黄绿": 90,
    "绿": 120,
    "青绿": 150,
    "青": 180,
    "靛": 210,
    "蓝": 240,
    "紫": 270,
    "品红": 300,
    "紫红": 330,
}

TOLERANCE = 3  # 允许角度误差 ±3 度

def color_block(hue):
    """根据色相角生成彩色方块"""
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue / 360, 1, 1)]
    return f"\033[38;2;{r};{g};{b}m█\033[0m"

def play_color_hue_game():
    color_items = list(colors.items())
    random.shuffle(color_items)
    color_queue = deque(color_items)

    seen = set()        # 已经训练过（第一次答对或答错过的颜色）
    to_reinforce = set()  # 第一次答错过，需要最后再问一次的颜色

    print("🎨 色相环颜色角度记忆游戏开始！输入颜色角度（0–360°），允许 ±3° 误差。\n")

    while color_queue:
        color_name, correct_angle = color_queue.popleft()

        block = color_block(correct_angle)
        prompt = f"👉『{color_name}』 {block} 的颜色角度是多少？输入数字："

        try:
            user_input = input(prompt)
            user_angle = int(user_input.strip()) % 360
        except ValueError:
            print("⚠️ 无效输入，请输入整数角度（0–360）。\n")
            color_queue.appendleft((color_name, correct_angle))  # 重问当前
            continue

        diff = abs(user_angle - correct_angle)
        diff = min(diff, 360 - diff)

        if diff <= TOLERANCE:
            if color_name in to_reinforce:
                print("✅ 正确！已进入最后巩固环节。\n")
                continue  # 这次就不再放回去了
            elif color_name in seen:
                print("✅ 正确！\n")
                continue  # 已经是强化阶段，不再处理
            else:
                print("✅ 一次就答对，棒！\n")
                seen.add(color_name)
                continue  # 一次通过，不再处理

        # 第一次答错
        print(f"❌ 错误！再试一次。提示：目标角度约为 {correct_angle}°。\n")
        while True:
            # 重复问直到答对
            try:
                user_input = input(f"🔁『{color_name}』再试一次：")
                user_angle = int(user_input.strip()) % 360
            except ValueError:
                print("⚠️ 无效输入，请输入整数角度（0–360）。\n")
                continue

            diff = abs(user_angle - correct_angle)
            diff = min(diff, 360 - diff)

            if diff <= TOLERANCE:
                print("✅ 正确！该颜色稍后会再出现一次。\n")
                seen.add(color_name)
                to_reinforce.add(color_name)
                color_queue.append((color_name, correct_angle))  # 加到队尾，强化训练
                break
            else:
                print(f"❌ 仍然不对，再来。目标角度约为 {correct_angle}°。\n")

    print("\n🎉 所有颜色训练完毕，色相记忆巩固完成！")

if __name__ == "__main__":
    play_color_hue_game()

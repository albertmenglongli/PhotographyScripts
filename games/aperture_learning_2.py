# 全部 1/3 档光圈值，f/1.4 ~ f/32
aperture_list = [
    "f/1.4", "f/1.6", "f/1.8", "f/2.0",
    "f/2.2", "f/2.5", "f/2.8", "f/3.2",
    "f/3.5", "f/4.0", "f/4.5", "f/5.0",
    "f/5.6", "f/6.3", "f/7.1", "f/8.0",
    "f/9.0", "f/10",  "f/11",  "f/13",
    "f/14",  "f/16",  "f/18",  "f/20",
    "f/22",  "f/26",  "f/28",  "f/32",
]

def normalize(value):
    value = value.lower().replace(" ", "").replace("f/", "")
    try:
        num = float(value)
        if num.is_integer():
            return f"f/{int(num)}"
        else:
            return f"f/{num}"
    except:
        return "invalid"

def run_memory_test():
    print("📘 开始从 f/1.4 默写到 f/32 (步长为1/3档光圈)，答错就从头开始！")

    while True:
        print("\n👉 默写开始：")
        for i, correct in enumerate(aperture_list):
            ans = input().strip()
            if normalize(ans) != normalize(correct):
                print(f"❌ 错了，正确答案是：{correct}")
                print("🔁 再来一次，从头开始！")
                break
        else:
            print("\n🎉 恭喜你，全部默写正确！")
            break

if __name__ == "__main__":
    run_memory_test()

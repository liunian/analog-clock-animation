import sys  # 用于解析命令行参数
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
from datetime import datetime
import shutil  # 用于删除整个目录

# 创建帧图目录
frame_dir = "clock_frames"
os.makedirs(frame_dir, exist_ok=True)

# 画时钟函数（带小时数字，动态秒针）
def draw_clock(hour, minute, second, filename):
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_aspect('equal')
    ax.axis('off')

    # 表盘圆圈
    circle = plt.Circle((0, 0), 1, fill=False, linewidth=2)
    ax.add_artist(circle)

    # 表盘中心小圆
    center_circle = plt.Circle((0, 0), 0.05, color='black', zorder=5)  # 半径为0.05，颜色为黑色
    ax.add_artist(center_circle)

    # 添加小时刻度线和数字
    for i in range(12):
        angle = np.deg2rad(90 - 30 * i)  # 修正角度方向
        x1, y1 = 0.9 * np.cos(angle), 0.9 * np.sin(angle)
        x2, y2 = np.cos(angle), np.sin(angle)
        ax.plot([x1, x2], [y1, y2], 'k', lw=2)

        # 数字
        tx, ty = 0.75 * np.cos(angle), 0.75 * np.sin(angle)
        label = i if i != 0 else 12
        ax.text(tx, ty, str(label), ha='center', va='center', fontsize=12, fontweight='bold')

    # 添加分钟刻度线
    for i in range(60):
        if i % 5 != 0:  # 跳过小时刻度线的位置
            angle = np.deg2rad(90 - 6 * i)
            x1, y1 = 0.95 * np.cos(angle), 0.95 * np.sin(angle)
            x2, y2 = np.cos(angle), np.sin(angle)
            ax.plot([x1, x2], [y1, y2], 'k', lw=1)

    # 指针角度
    hour_angle = np.deg2rad(90 - (30 * (hour % 12) + 0.5 * minute + second / 120))
    minute_angle = np.deg2rad(90 - (6 * minute + 0.1 * second))
    second_angle = np.deg2rad(90 - 6 * second)

    # 画指针（从中心逐渐变粗再变细）
    ax.plot([0, 0.5 * np.cos(hour_angle)], [0, 0.5 * np.sin(hour_angle)], lw=6, color='black', solid_capstyle='round')
    ax.plot([0, 0.75 * np.cos(minute_angle)], [0, 0.75 * np.sin(minute_angle)], lw=4, color='blue', solid_capstyle='round')
    ax.plot([0, 0.9 * np.cos(second_angle)], [0, 0.9 * np.sin(second_angle)], lw=2, color='red', solid_capstyle='round')

    # 保存图片，设置透明背景
    plt.savefig(filename, dpi=300, transparent=False)
    plt.close()

def run(start_hour=9, total_frames=55):
    # 生成帧图
    frame_paths = []

    print("🚀 开始生成帧图...")

    for i, t in enumerate(range(0, 3600, 3600 // total_frames)):
        m = (t // 60) % 60
        s = t % 60
        filename = os.path.join(frame_dir, f"frame_{t:04d}.png")
        draw_clock(start_hour, m, s, filename)
        frame_paths.append(filename)

        # 更新进度展示在同一行
        print(f"\r[进度] 已完成 {i + 1} / {total_frames} 帧", end='')

    print("\n✅ 帧图生成完毕，开始生成 GIF...")

    # 生成 GIF（每帧0.05秒，循环播放），文件名包含时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    gif_path = f"clock_{start_hour}_{total_frames}_{timestamp}.gif"
    with imageio.get_writer(gif_path, mode='I', duration=0.05, loop=0) as writer:
        for i, path in enumerate(frame_paths):
            image = imageio.imread(path)
            writer.append_data(image)

    print("🎉 GIF 生成成功！文件名:", gif_path)

    # 删除临时生成的帧图和目录
    try:
        shutil.rmtree(frame_dir)  # 删除整个 frame_dir 目录
        print("🧹 临时帧图已清理！")
    except Exception as e:
        print(f"⚠️ 清理临时帧图时出错: {e}")

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) > 1:
        try:
            start_hour = int(sys.argv[1])
            total_frames = int(sys.argv[2]) if len(sys.argv) > 2 else 55

            if start_hour < 0 or total_frames <= 0:
                raise ValueError("参数必须是正整数！")

            run(start_hour=start_hour, total_frames=total_frames)
        except ValueError as e:
            print(f"❌ 参数错误: {e}")
            print("用法: python main.py <start_hour> <total_frames>")
    else:
        run()

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.widgets import Slider

# 输入参数
# 屏幕的大小
L = 50
# 屏幕之间的折射率
n = 10
# 屏幕间距
D = 50
# 双缝间距
d = 10
# 干涉角
sita = 60

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.35)

# 定义波长计算函数
def wave_length(d, sita):
    return d * np.sin(sita)

# 定义屏幕上的坐标范围
x_min, x_max = -0.3 * d, 0.3 * d
y_min, y_max = -0.3 * d, 0.3 * d

# 定义屏幕上的网格点数
m = 500

# 生成屏幕上的网格坐标
x = np.linspace(x_min, x_max, m)
y = np.linspace(y_min, y_max, m)
X, Y = np.meshgrid(x, y)

T = wave_length(d, sita)
P = int(T)
j = (L * d) / (D * P)
deta_y = P * D / d
P = P / j

# 计算双缝到屏幕上每个点的距离
r1 = np.sqrt(D ** 2 + Y ** 2 + (X + d / 2) ** 2)
r2 = np.sqrt(D ** 2 + Y ** 2 + (X - d / 2) ** 2)

# 定义计算光程差函数
def delta_r():
    return n * (r1 - r2)

# 定义计算相位差的函数
def delta_phi():
    return 2 * np.pi * delta_r() / P

# 定义光强函数
def I():
    return 4 * np.power(np.cos(delta_phi() / 2), 2)

im = ax.imshow(I(), cmap='gray', extent=[x_min, x_max, y_min, y_max])
ax.set_title("杨氏双缝干涉明暗条纹图像")
ax.set_xlabel("x（mm）")
ax.set_ylabel("y（mm）")

axcolor = 'lightgoldenrodyellow'
ax_L = plt.axes([0.2, 0.25, 0.6, 0.02], facecolor=axcolor)
ax_n = plt.axes([0.2, 0.20, 0.6, 0.02], facecolor=axcolor)
ax_D = plt.axes([0.2, 0.15, 0.6, 0.02], facecolor=axcolor)
ax_d = plt.axes([0.2, 0.10, 0.6, 0.02], facecolor=axcolor)
ax_sita = plt.axes([0.2,0.05,0.6,0.02],facecolor=axcolor)

s_L = Slider(ax_L, '屏幕大小 (mm)', 1, 200, valinit=L)
s_n = Slider(ax_n, '屏幕之间的折射率', 1, 50,valinit=n)
s_D = Slider(ax_D, '屏幕间距 (mm)', 50, 100, valinit=D)
s_d = Slider(ax_d, '双缝间距 (mm)', 11.3, 11.7, valinit=d)
s_sita = Slider(ax_sita, '干涉角 (度)', 45, 50, valinit=sita)

def update(val):
    global L, n, D, d, sita
    L = s_L.val
    n = s_n.val
    D = s_D.val
    d = s_d.val
    sita = np.deg2rad(s_sita.val)

    T = wave_length(d, sita)
    P = int(T)
    j = (L * d) / (D * P)
    deta_y = (P * s_D.val) / (s_d.val*s_n.val)
    P = P / j
    T=(T*s_n.val)/(s_D.val*np.sin(sita))
    
    # 计算双缝到屏幕上每个点的距离
    r1 = np.sqrt(D ** 2 + Y ** 2 + (X + d / 2) ** 2)
    r2 = np.sqrt(D ** 2 + Y ** 2 + (X - d / 2) ** 2)

    # 定义计算光程差函数
    def delta_r():
        return n * (r1 - r2)

    # 定义计算相位差的函数
    def delta_phi():
        return 2 * np.pi * delta_r() / P

    # 定义光强函数
    def I():
        return 4 * np.power(np.cos(delta_phi() / 2), 2)

    im.set_data(I())
    
    ax.set_title(f"杨氏双缝干涉明暗条纹图像\n波长: {T:.3f} mm, 条纹间距: {deta_y:.3f} mm")
    
    fig.canvas.draw_idle()

plt.rcParams['font.sans-serif']=['FangSong']
plt.rcParams['axes.unicode_minus'] = False
s_L.on_changed(update)
s_n.on_changed(update)
s_D.on_changed(update)
s_d.on_changed(update)
s_sita.on_changed(update)

plt.colorbar(im)

plt.show()
#2023615完成

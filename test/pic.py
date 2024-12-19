import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 设置中文字体
font = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc", size=14)  # 选择一个支持中文的字体文件
# 数据
cities = ['北京', '上海', '广州', '深圳']
sales = [120, 150, 90, 110]

# 创建柱状图
plt.bar(cities, sales)

# 添加标题和标签
plt.title('各城市销售额', fontproperties=font)
plt.xlabel('城市', fontproperties=font)
plt.ylabel('销售额', fontproperties=font)

# 显示图形
plt.show()
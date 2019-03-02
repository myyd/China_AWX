#黄山市气象台 胡玥琦制作
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cmx
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from tkinter import filedialog
#加载自定义的颜色脚本
import color
#加载FY4A_AWX脚本
import FY4A_AWX
#颜色名称请进入color脚本中查看


#交互式数据选择
file = filedialog.askopenfilename(filetypes = [('AWX Files', '*.AWX')], title = '请选择要处理的风云4号AWX格式数据')

#调用FY4A_AWX CLASS
awx = FY4A_AWX.FY4A_AWX(file)
#读出数据
data = awx.data_out()
#读出经纬度等信息
lons, lats, lonmid, latmid = awx.geo_out()
#计算数据尺寸
size1, size2 = (data.shape[1], data.shape[0])
#读取通道
channel_number = awx.channel_number
#投影方式
#proj = ccrs.Orthographic(central_longitude = lonmid, central_latitude = latmid)
#proj = ccrs.PlateCarree(central_longitude = 0.)
proj = ccrs.LambertConformal(central_longitude = lonmid, central_latitude = latmid, standard_parallels = [35])
#设置自定义color与量程
if channel_number in [1, 2, 3]:
    colorbar = input('请选择颜色：1.nmc，2.bd，3.color，4.wv，5.ssdwv，6.bw。（不选择回车默认黑白色阶）')
    if colorbar == '1':
        ys = color.nmc
    elif colorbar == '2':
        ys = color.irbd
    elif colorbar == '3':
        ys = color.ircolor
    elif colorbar == '4':
        ys = color.wv
    elif colorbar == '5':
        ys = color.ssdwv
    else:
        ys = color.irbw
    my_cmap = mpl.colors.LinearSegmentedColormap('my_colormap', ys, 256)
    norm = mpl.colors.Normalize(-100, 50)
    linewidth1 = 0.5
    linewidth2 = 0.7
else:
    my_cmap = 'gray'
    norm = mpl.colors.Normalize(0, 1)
    data = np.sqrt(data)
    linewidth1 = 2
    linewidth2 = 3

plt.axis('off')
fig = plt.figure(frameon=False) 

#自定义尺寸画图
fig.set_size_inches(size1/110.6, size2/100)

#设置图片无边框
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
plt.margins(0,0)
ax = plt.axes(projection = proj)
ax.background_patch.set_visible(False)
ax.outline_patch.set_visible(False)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
plt.margins(0,0)

#自定义显示范围（经纬度）
#ax.set_extent((89, 125, 16.5, 47.5))
ax.pcolormesh(lons, lats, data, cmap = my_cmap, norm = norm, transform = ccrs.PlateCarree())

#读取shp文件
coastlines = "shp\\ne_50m_coastline.shp"  #预先准备好的50m海岸线地图
adm2_shapes = list(shpreader.Reader(coastlines).geometries())    #读取地图文件信息
ax.add_geometries(adm2_shapes, ccrs.PlateCarree(), edgecolor='dimgray', linewidth = linewidth1,  facecolor='none')

china_border = "shp\\cnhimap.shp"  #预先准备好的精准中国地图
adm1_shapes = list(shpreader.Reader(china_border).geometries())    #读取地图文件信息
ax.add_geometries(adm1_shapes, ccrs.PlateCarree(), edgecolor='white', linewidth = linewidth2,  facecolor='none')
#交互式画图保存，若无法保存为jpg请先pip安装pillow库
path = filedialog.asksaveasfilename(filetypes=[('','*')], title='另存为')
plt.savefig(path + '.jpg')
plt.close()
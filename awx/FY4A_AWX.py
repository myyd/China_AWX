#黄山市气象台 胡玥琦制作
#Read FY4A_L1.AWX
import numpy as np
#解码AWX
_awx_dtype = [#head1
            ('name', 'S', 12),
            ('head1 int', 'i2', 1),
            ('head1 length', 'i2', 1), 
            ('head2 length', 'i2', 1),
            ('fill long', 'i2', 1),
            ('stepping1', 'i2', 3),
            ('product category', 'i2', 1),
            ('stepping2', 'S', 12),
            #head2
            ('satellite name', 'S', 8),
            ('year', 'i2', 1),
            ('month', 'i2', 1),
            ('day', 'i2', 1),
            ('hour', 'i2', 1),
            ('minutes', 'i2', 1),
            ('channel number', 'i2', 1),
            ('projection mode', 'i2', 1),
            ('lines', 'i2', 1),
            ('columns', 'i2', 1),
            ('begin lines', 'i2', 1),
            ('begin columns', 'i2', 1),
            ('sampling rates', 'i2', 1),
            ('north latitude', 'i2', 1),
            ('south latitude', 'i2', 1),
            ('west longitude', 'i2', 1),
            ('east longitude', 'i2', 1),
            ('center latitude', 'i2', 1),
            ('center longitude', 'i2', 1),
            ('stepping3', 'i2', 6),
            ('color palette length', 'i2', 1),
            ('calibration length', 'i2', 1),
            ('location', 'i2', 1),
            ('stepping4', 'i2', 1),
            ('calibration', 'u2', 1024)]

class FY4A_AWX:
    def __init__(self, filename):
        self.f = open(filename, mode = 'rb')
        self.count = np.arange(0, 256, 1)
        self.read = np.frombuffer(self.f.read(np.dtype(_awx_dtype).itemsize), np.dtype(_awx_dtype))
        self.x = self.read['lines'][0]
        self.y = self.read['columns'][0]
        self.channel_number = self.read['channel number'][0]

    def _geo(self):
        #经纬度信息
        latmin = self.read['north latitude'][0] / 100
        latmax = self.read['south latitude'][0] / 100
        lonmin = self.read['west longitude'][0] / 100
        lonmax = self.read['east longitude'][0] / 100
        lonmid = self.read['center longitude'][0] / 100
        latmid = self.read['center latitude'][0] / 100
        #制作经纬度list
        lons = np.linspace(lonmin, lonmax, self.x)
        lats = np.linspace(latmin, latmax, self.y)
        return lons, lats, lonmid, latmid

    def _readdata(self):
        #读取数据
        awx_data = [('fill', 'i1', self.read['fill long'][0]), ('data', 'u1', int(self.x) * int(self.y))]
        read1 = np.frombuffer(self.f.read(np.dtype(awx_data).itemsize), np.dtype(awx_data))
        dt1 = read1['data'][0]
        if self.channel_number in [1, 2, 3]:
            #读取读取红外，水汽定标表
            var1 = self.read['calibration'][0] / 100
            #定标
            dictionary = dict(zip(self.count, var1[::4]))
            data = np.vectorize(dictionary.__getitem__)(dt1).reshape(self.y, self.x) - 273.15
        else:
            #读取可见光定标表
            var1 = self.read['calibration'][0] / 10000
            var1 = var1[:64]
            var1 = var1.repeat(4)
            #定标
            dictionary = dict(zip(self.count, var1))
            data = np.vectorize(dictionary.__getitem__)(dt1).reshape(self.y, self.x)
        return data

    def data_out(self):
        #输出数据
        data = self._readdata()
        return data

    def geo_out(self):
        #输出经纬度
        lons, lats, lonmid, latmid = self._geo()
        return lons, lats, lonmid, latmid


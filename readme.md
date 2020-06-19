第一步：安装相关工具包

```shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple flask==0.12.2 flask-jsonpify==1.5.0 flask-jsonrpc==0.3.1
pip install  -i https://pypi.tuna.tsinghua.edu.cn/simple baidu-aip
```

第二步：修改配置文件config

```python
# ocr_tool配置

URL = 'http://192.168.8.126:5010'  # 默认ocr调用接口，确认自己电脑ping得通192.168.8.126
FLAGS = ['光大', '广发', '广州', '华夏', '交通', '民生', '平安', '浦发', '上海', '兴业', '中国', '招商' , '汇丰', '中信']  # 如果识别的信用卡种类不在里面，需要自己自行添加
```

第三步：根据自己需求调用predict.py文件下面的函数

```python
# 示例1
ocr_path('../bank_logo')  # 检测文件夹下面所有图片
# 示例2
ocr_file("/home/huangjx/Projects/Thursday_yolo3/bank_logo/SH800_PQ18081705.jpg")  # 检测一张图片
```


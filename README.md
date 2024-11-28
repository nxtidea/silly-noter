# Silly Noter
为比赛开发的简单数据标注工具，以力破巧。
- 自动保存结果和进度，下次打开时可以继续标注
- 如果标错了，直接去修改`output`目录下`marked_`开头的json文件即可
- 建议使用大点的或高分辨率屏幕进行标注

## 使用方法

### 下载本项目并安装依赖（实际仅依赖streamlit）：

```
git clone https://github.com/nxtidea/silly-noter.git
cd silly-noter
pip install -r requirements.txt
```

### 准备数据

1. 将赛题10000数据的zip压缩包放在`raw`目录下，使用`unzip`命令解压，解压后应得到目录结构如下：

```
raw
├── test1
|---- test1.json
|---- images
```

2. 运行`split_data.py`脚本分割数据集，分割后数据集在`splited`目录下
```
python split_data.py
```

### 运行标注工具

在终端运行下面命令，启动标注工具：

```
streamlit run main.py 0-2000.json
```

其中`0-2000.json`是要标注的数据集名称，可以用`splited`目录下的文件名来指定。
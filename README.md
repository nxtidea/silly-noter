# Silly Noter
为比赛开发的简单数据标注工具，以力破巧。

## 使用方法

### 下载本项目并安装依赖（实际仅依赖streamlit）：

```
git clone https://github.com/gavinzhou/silly-noter.git
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

1. 选择要标注的部分数据集，在`main.py`开头的地方修改`your_splited_filename`变量，例如：

```python
your_splited_filename = "0-2000.json"
```

2. 在终端运行下面命令，启动标注工具：

```
streamlit run main.py
```

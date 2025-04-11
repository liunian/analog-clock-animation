# 模拟时钟 GIF 动图

生成模拟时钟从某个小时开始的一小时指针、分针、秒针动图。

## 准备

安装依赖

如果使用 `uv`，可以使用

```bash
uv sync
```

否则可以使用 `pip`

```bash
pip install -r requirements.txt
```

## 运行

可以直接使用默认的 `9` 点 `55` 帧

```bash
python main.py
```

也可以使用额外的运行参数来分别指定开始小时和总帧数，如从 12 点开始，共 90 帧

```bash
python main.py 12 90
```
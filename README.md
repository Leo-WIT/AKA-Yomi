<div align="center">

# AKA-Yomi

<br>

![AKA-Yomi Screenshot](AKA-Yomi.png)

<br>

<div>
    <img alt="platform" src="https://img.shields.io/badge/platform-Windows-blueviolet">
    <img alt="license" src="https://img.shields.io/github/license/Leo-WIT/AKA-Yomi">
    <img alt="language" src="https://img.shields.io/badge/python-%3E%3D%203.10-green">
</div>
<br>

[简体中文](README.md) | [English](README_en-US.md)

</div>

## 简介

AKA-Yomi 是一款基于 [KeymouseGo](https://github.com/taojy123/KeymouseGo) 重构的鼠标键盘自动化工具，专注于 Windows 平台的用户体验优化。

功能：记录用户的鼠标键盘操作，通过触发按钮自动执行之前记录的操作，可设定执行的次数，支持运行前/后延迟和随机延迟，可以理解为 `精简绿色版` 的 `按键精灵`。

用途：在进行某些操作简单、单调重复的工作时，使用本软件就可以很省力了。自己只要做一遍，然后接下来就让电脑来做。

## 主要特性

- 🌍 **多语言支持**：简体中文 / English / 繁體中文
- 🎨 **主题系统**：Material 浅色、Material 深色、Bootstrap 风格、玻璃拟态、卡通、极客等多种主题
- ⏱️ **延迟控制**：支持运行前/后延迟，可启用随机延迟范围
- 🛑 **停止按钮**：录制或运行时可随时停止
- 📁 **文件管理**：一键打开脚本文件夹，支持重命名、编辑、清除脚本
- ⌨️ **热键支持**：可自定义启动/停止/录制热键
- 🔧 **插件系统**：支持自定义插件扩展功能

## 下载使用

### 直接下载（推荐）

前往 [Releases](https://github.com/Leo-WIT/AKA-Yomi/releases) 页面下载最新版本的 `AKA-Yomi.exe`，双击即可运行。

> 所有运行时文件（配置、脚本、日志）均存储在系统临时目录 `%TEMP%\KeymouseGo\` 下，不会在 exe 所在目录生成任何文件。

### 从源码运行

```bash
# 1. 克隆仓库
git clone https://github.com/Leo-WIT/AKA-Yomi.git
cd AKA-Yomi

# 2. 安装依赖
pip install -r requirements-windows.txt

# 3. 运行
python KeymouseGo.py
```

### 打包为可执行文件

```bash
# 安装 pyinstaller
pip install pyinstaller

# 打包（Windows）
pyinstaller -Fw --add-data "assets;assets" --icon "Mondrian.ico" --name "AKA-Yomi" KeymouseGo.py
```

打包完成后，可执行文件位于 `dist/AKA-Yomi.exe`。

## 使用指南

### 界面说明

| 区域 | 功能 |
|------|------|
| 执行控制 | 开始录制 / 暂停录制 / 启动 / 停止 |
| 脚本列表 | 选择要执行的脚本 |
| 文件管理 | 打开文件夹 / 编辑 / 重命名 / 清除脚本 |
| 执行设置 | 循环次数、运行前/后延迟、随机延迟 |
| 录制设置 | 鼠标/键盘录制开关 |
| 主题设置 | 切换界面主题 |
| 语言设置 | 切换界面语言 |
| 热键设置 | 自定义启动/停止/录制热键 |

### 基本操作

1. **录制脚本**
   - 点击 `开始录制` 按钮
   - 进行鼠标点击、键盘输入等操作
   - 点击 `完成录制` 按钮结束
   - 脚本自动保存到脚本文件夹

2. **执行脚本**
   - 在脚本列表中选择要执行的脚本
   - 设置循环次数（0 为无限循环）
   - 可选：设置运行前/后延迟
   - 点击 `启动` 按钮开始执行

3. **停止操作**
   - 录制中点击 `停止`：弹窗确认是否放弃本次录制
   - 运行中点击 `停止`：立即终止脚本执行

### 热键

- **启动热键**：默认 `F6`，等同于点击 `启动` 按钮
- **停止热键**：默认 `F9`，等同于点击 `停止` 按钮
- **录制热键**：默认 `F10`，等同于点击 `开始录制` 按钮

### 提示

1. 可设置脚本重复执行的次数，如果为 `0` 即为无限循环。
2. 录制时只记录鼠标点击动作和键盘动作，不记录鼠标移动轨迹。
3. 每次录制结束后都会在脚本文件夹中生成一个新的脚本文件。
4. 运行前可以在列表中选择一个需要执行的脚本。
5. 热键设置中的 `Middle` 指代鼠标中键，`XButton` 指代鼠标侧键。
6. 由于程序速度受限，当输入的鼠标速度大于一定值时脚本将无法以预期的输入速度执行。
7. 部分系统环境中，可能出现无法录制完整的鼠标事件的情况，请以管理员身份运行此工具即可正常使用。

## 脚本语法

脚本为 `json5` 格式，每个事件代表一个操作：

```json5
{
  scripts: [
    // 开始运行 3000ms 后，在屏幕相对坐标 (0.05208, 0.1852) 即 (100,200) 处按下鼠标右键
    {type: "event", event_type: "EM", delay: 3000, action_type: "mouse right down", action: ["0.05208%", "0.1852%"]},
    // 等待 50ms 后在相同位置抬起鼠标右键
    {type: "event", event_type: "EM", delay: 50, action_type: "mouse right up", action: [-1, -1]},
    // 等待 1000ms 后按下 F 键
    {type: "event", event_type: "EK", delay: 1000, action_type: "key down", action: [70, 'F', 0]},
    // 等待 50ms 后抬起 F 键
    {type: "event", event_type: "EK", delay: 50, action_type: "key up", action: [70, 'F', 0]},
    // 等待 100ms 后输入文字
    {type: "event", event_type: "EX", delay: 100, action_type: "input", action: "你好 world"}
  ]
}
```

## 技术栈

- Python 3.10+
- PySide6（Qt 界面）
- pynput（鼠标键盘录制）
- pyautogui（鼠标键盘执行）
- qt-material（主题系统）
- loguru（日志）

## 开源协议

本项目基于 [GNU GPLv3](LICENSE) 协议开源。

## 致谢

本项目基于 [KeymouseGo](https://github.com/taojy123/KeymouseGo) 进行二次开发，感谢原作者的贡献。

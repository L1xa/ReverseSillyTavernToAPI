# ReverseSillyTavernToAPI

ReverseSillyTavernToAPI是一个基于 Selenium 的 SillyTavern API 代理服务，通过Selenium自动化操作SillyTavern网页，实现了SillyTavern的API接口。

## ⚠️ 免责声明

本项目仅用于学习和研究目的：
1. 请遵守 SillyTavern 的使用条款和规则
2. 不得用于任何商业用途
3. 使用本项目造成的任何问题由使用者自行承担

## 功能特点

- 使用 Selenium 自动化操作 SillyTavern 网页界面
- 提供 HTTP API 接口，支持发送消息和查询状态
- 自动等待页面加载和响应
- 支持命令行交互模式

## 系统要求

- Python 3.7+
- Google Chrome 浏览器
- ChromeDriver（与 Chrome 版本匹配）

## 安装

1. 克隆仓库：
```bash
git clone 
```

## 使用限制

1. 请控制请求频率，避免对服务器造成压力
2. 建议在个人或测试环境中使用
3. 遵守相关法律法规和服务条款

## 使用示例

```python
# 创建一个 SillyTavernAPI 实例
api = SillyTavernAPI()

# 发送消息
response = api.send_message("Hi!")
print(response)

# 查询状态
status = api.get_status()
print(status)
```
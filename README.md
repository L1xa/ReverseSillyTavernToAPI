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
git clone https://github.com/the-lazy-me/ReverseSillyTavernToAPI.git
```

## 使用限制

1. 请控制请求频率，避免对服务器造成压力
2. 建议在个人或测试环境中使用
3. 遵守相关法律法规和服务条款

## API 接口说明

### 1. 状态检查

检查服务是否就绪。

```bash
curl http://localhost:4444/status
```

响应示例：
```json
{
    "status": "ready"  // 或 "initializing"
}
```

### 2. 发送消息

向 SillyTavern 发送消息并获取回复。

```bash
curl -X POST http://localhost:4444 \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi!"}'
```

响应示例：
```json
{
    "response": "Hello! How can I help you today?"
}
```

错误响应示例：
```json
{
    "error": "聊天系统正在初始化，请稍后再试"  // 503 Service Unavailable
}
```
```json
{
    "error": "Message is required"  // 400 Bad Request
}
```

## 使用示例

### Python 示例
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

### curl 示例
```bash
# 检查状态
curl http://localhost:4444/status

# 发送消息
curl -X POST http://localhost:4444 \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi!"}'
```

### JavaScript 示例
```javascript
// 发送消息
fetch('http://localhost:4444', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        message: 'Hi!'
    })
})
.then(response => response.json())
.then(data => console.log(data));

// 检查状态
fetch('http://localhost:4444/status')
.then(response => response.json())
.then(data => console.log(data));
```



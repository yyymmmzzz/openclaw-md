---
name: self-improving-agent
description: 自我改进Agent，持续学习优化。安装量21,856+，开发者必备。
---

# Self-Improving Agent - 自我改进

持续学习和优化的Agent系统。

## 功能

- 📊 分析历史对话，提取改进点
- 🎯 识别常见错误，避免重复
- 📝 优化提示词和响应质量
- 📈 追踪性能指标

## 使用方法

```bash
# 分析最近会话
python3 improve.py analyze --sessions 10

# 生成改进建议
python3 improve.py suggest

# 查看学习报告
python3 improve.py report

# 应用优化
python3 improve.py apply --category prompts
```

## 工作原理

1. **收集反馈**: 从对话历史中提取用户反馈
2. **模式识别**: 识别常见问题和成功模式
3. **生成建议**: 基于分析生成改进建议
4. **持续优化**: 迭代改进响应质量

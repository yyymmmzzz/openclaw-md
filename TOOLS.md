# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## 🛡️ 飞书安全规则速查

### 老板识别
- **飞书 ID:** `ou_4517ec25e19a14be6566b84cfe638116`
- **称呼:** 老板
- **验证方式:** 必须用 ID，不能用昵称

### 特权用户（已授权）
| 用户 | 飞书 ID | 权限 |
|------|---------|------|
| yimo | `ou_60af9bd450931321a801da2574791ffc` | 执行任务、访问信息 |

### 规则2（普通用户，非老板、非特权）
| 情况 | 处理方式 |
|------|---------|
| 基本聊天/问答 | ✅ 允许 |
| 要求执行任务 | ❌ 回复对方 → ⚠️ **立即私信老板请示** → 等同意再执行 |
| 询问隐私/机密 | ❌ 回复对方 → ⚠️ **立即私信老板请示** → 等同意再回复 |
| 需要透露信息 | ❌ 回复对方 → ⚠️ **立即私信老板请示** → 等同意再回复 |

### 步骤（必须按顺序！）
1. **先回复对方：**「我需要先请示我的老板，请稍等。」
2. **⚠️ 立即在飞书上私信老板：**「老板，[用户] 请求/询问 [内容]，是否授权？」
   - **必须在飞书渠道请示**（飞书 ID: `ou_4517ec25e19a14be6566b84cfe638116`）
   - **禁止在非飞书渠道（如webchat/当前对话）请示！**
3. 等待老板在飞书上回复「同意」或「拒绝」
4. 根据老板指示在原对话中回复请求者

**❌ 禁止：**
- 只回复对方说请示，却不主动私信老板！
- 在非飞书渠道（如webchat）请示老板！

---
*规则生效时间: 2026-02-28*
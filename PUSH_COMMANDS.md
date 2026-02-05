# 推送代码到 GitHub 的方法

## 方法 1: 使用 Personal Access Token（推荐）

### 步骤 1: 生成 Personal Access Token

1. 访问 GitHub: https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 填写信息：
   - Note: SDL Security Crawler Push
   - Expiration: 选择过期时间（如 90 days）
   - Scopes: 勾选 `repo`（完整仓库访问权限）
4. 点击 "Generate token"
5. **重要**: 复制生成的 token（只显示一次）

### 步骤 2: 推送代码

```bash
# 设置用户名（使用你的 GitHub 用户名）
git config --global user.name "he1m4n6a"

# 设置邮箱
git config --global user.email "your-email@example.com"

# 推送代码（会提示输入密码时，粘贴 Token）
git push -u origin 260205-feat-sdl-security-news-crawler
```

**注意**: 
- Username 输入: he1m4n6a
- Password 输入: 刚才复制的 Token（不是 GitHub 密码）

## 方法 2: 使用 Git Credential Helper

### 配置凭证存储

```bash
# 使用凭证助手
git config --global credential.helper store

# 推送时会要求输入一次凭证
git push -u origin 260205-feat-sdl-security-news-crawler
```

## 方法 3: 使用 SSH 密钥

### 生成 SSH 密钥

```bash
# 生成 SSH 密钥（如果还没有）
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
```

### 添加公钥到 GitHub

1. 访问: https://github.com/settings/keys
2. 点击 "New SSH key"
3. 输入标题: SDL Security Crawler Key
4. 复制公钥内容:
   ```bash
   cat ~/.ssh/id_rsa.pub
   ```
5. 粘贴到 GitHub
6. 点击 "Add SSH key"

### 修改远程仓库为 SSH

```bash
# 修改为 SSH 地址
git remote set-url origin git@github.com:he1m4n6a/sdlcrawl.git

# 推送代码
git push -u origin 260205-feat-sdl-security-news-crawler
```

## 方法 4: 使用 GitHub CLI（gh）

### 安装 gh CLI

```bash
# macOS
brew install gh

# Linux
sudo apt install gh

# Windows
winget install GitHub.cli
```

### 使用 gh 推送

```bash
# 登录
gh auth login

# 推送代码
gh repo create sdlcrawl --public --source=.
# 或推送到已存在的仓库
gh repo set-default sdlcrawl
git push -u origin 260205-feat-sdl-security-news-crawler
```

## 方法 5: 在 GitHub 网页上创建

### 步骤 1: 创建仓库

1. 访问: https://github.com/new
2. 填写信息：
   - Repository name: sdlcrawl
   - Description: SDL 安全文章爬取系统 - 自动爬取安全资讯并推送到飞书
   - Public/Private: 根据需要选择
   - 不要勾选 "Initialize this repository"
3. 点击 "Create repository"

### 步骤 2: 推送现有代码

```bash
# 添加新的远程仓库（如果需要）
git remote add origin https://github.com/he1m4n6a/sdlcrawl.git

# 推送代码
git push -u origin 260205-feat-sdl-security-news-crawler
```

## 推送验证

推送成功后，访问: https://github.com/he1m4n6a/sdlcrawl

### 查看分支
https://github.com/he1m4n6a/sdlcrawl/tree/260205-feat-sdl-security-news-crawler

### 查看提交
https://github.com/he1m4n6a/sdlcrawl/commits/260205-feat-sdl-security-news-crawler

## 快速推送命令

### 一键推送（使用 Token）

```bash
# 在你的本地终端执行
cd /path/to/sdlcrawl
git push -u origin 260205-feat-sdl-security-news-crawler
```

### 查看所有分支

```bash
git branch -a
git log --oneline -5
```

### 查看待推送的提交

```bash
git log origin/260205-feat-sdl-security-news-crawler..HEAD --oneline
```

## 常见问题

### Q: 提示 "Authentication failed"
A: 
- 检查用户名是否正确
- 确认 Token 是否有效
- 确保 Token 有 `repo` 权限

### Q: 提示 "remote already exists"
A: 
- 仓库已存在，直接推送即可
- 无需重新创建仓库

### Q: 提示 "nothing to commit"
A: 
- 所有改动已提交
- 运行 `git status` 确认

### Q: 推送速度很慢
A: 
- 可能网络问题
- 尝试使用 SSH 替代 HTTPS
- 检查代理设置

## 推送后的操作

推送成功后：

1. **创建 Pull Request**（可选）
   - 访问: https://github.com/he1m4n6a/sdlcrawl/compare/260205-feat-sdl-security-news-crawler
   - 点击 "Create pull request"

2. **合并到主分支**（可选）
   - 访问: https://github.com/he1m4n6a/sdlcrawl/pull/new
   - 创建 Pull Request 合并分支

3. **设置 GitHub Actions**（可选）
   - 添加自动化 CI/CD
   - 自动运行测试
   - 自动部署

## 仓库文件结构

推送成功后，仓库将包含：

```
sdlcrawl/
├── .git/
├── config/
│   └── sources.yaml
├── src/
│   ├── crawler/
│   ├── translator/
│   ├── notifier/
│   ├── utils/
│   ├── data/
│   ├── logs/
│   ├── main.py
│   ├── simple_demo.py
│   ├── demo_with_translation.py
│   ├── show_lark_format.py
│   └── sources.yaml
├── scheduler.py
├── requirements.txt
├── .env.example
├── README.md
├── FINAL_SUMMARY.md
├── ENHANCED_SOURCES.md
├── RUNNING_RESULTS.md
├── PROJECT_SUMMARY.md
├── LARK_WEBHOOK_GUIDE.md
├── LARK_FORMAT_OPTIMIZATION.md
├── PUSH_GUIDE.md
└── DOWNLOAD_GUIDE.md
```

## 总结

推荐使用 **方法 1**（Personal Access Token）或 **方法 3**（SSH 密钥）。

推送成功后，你就可以在 GitHub 上查看和协作代码了！

---

如果推送成功，告诉我，我可以帮你进行后续操作（如创建 PR、设置 GitHub Actions 等）。

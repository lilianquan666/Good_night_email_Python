# 发送晚安邮件项目

## 项目概述

这是一个基于Python的自动化邮件发送系统，主要功能是每天晚上23:00自动发送晚安邮件给指定用户。邮件包含个性化天气信息和随机晚安语录。该项目使用MySQL数据库存储用户信息、天气链接和语录数据，通过爬虫获取全国城市天气信息，并利用QQ邮箱SMTP服务发送HTML格式的邮件。

## 项目结构

```
发送晚安邮件/
├── city_weather_list.json          # 全国城市天气链接列表（由爬虫生成）
├── weather_crawler.py              # 天气数据爬虫脚本
└── Base_Python_for_email/
    ├── README.md                   # 项目说明文档
    ├── Evening-email/
    │   └── new_goodnight.py        # 晚安邮件发送主脚本
    └── Mysql/
        ├── user.sql                # 用户信息表结构和示例数据
        ├── weather.sql             # 天气链接表结构和数据
        └── word.sql                # 晚安语录表结构和数据
```

## 功能特性

- **自动化定时发送**: 每天23:00自动执行邮件发送任务
- **个性化天气信息**: 根据用户所在城市获取明日天气预报
- **随机晚安语录**: 从语录库中随机选择温暖的话语
- **HTML邮件格式**: 美观的邮件模板，包含图片和样式
- **数据库管理**: 使用MySQL存储用户、天气和语录数据
- **城市数据爬取**: 自动获取全国城市天气链接
- **测试模式**: 支持命令行参数进行即时测试

## 环境要求

- Python 3.x
- MySQL 5.7+
- 所需Python包：
  - requests
  - pymysql
  - pandas
  - beautifulsoup4
  - schedule
  - pypinyin

## 安装步骤

1. **克隆或下载项目文件**

2. **安装依赖包**
   ```bash
   pip install requests pymysql pandas beautifulsoup4 schedule pypinyin
   ```

3. **设置MySQL数据库**
   - 创建数据库：`goodnight_db`
   - 执行SQL文件创建表结构：
     ```sql
     -- 依次执行以下SQL文件
     -- user.sql
     -- weather.sql
     -- word.sql
     ```

4. **配置邮件发送**
   - 修改 `new_goodnight.py` 中的邮件配置：
     ```python
     mail_user = "your_qq_email@qq.com"
     mail_pass = "your_qq_authorization_code"
     ```

5. **配置数据库连接**
   - 修改 `new_goodnight.py` 中的数据库配置：
     ```python
     user_name = 'your_mysql_username'
     password = 'your_mysql_password'
     address = 'localhost'
     port = 3306
     DB_NAME = 'goodnight_db'
     ```

## 使用方法

### 运行晚安邮件发送

**定时模式（生产环境）**：
```bash
python new_goodnight.py
```
程序将在每天23:00自动发送邮件。

**测试模式**：
```bash
python new_goodnight.py --test
```
立即执行一次邮件发送，用于测试。

### 生成城市天气数据

运行爬虫脚本获取最新城市数据：
```bash
python weather_crawler.py
```
这将生成 `city_weather_list.json` 文件，包含全国城市拼音和天气链接。

## 数据库表说明

### user表
存储收件人信息：
- `id`: 主键ID
- `city`: 城市名称（必须与weather表中的city一致）
- `email`: 收件人邮箱地址

### weather表
存储城市天气链接：
- `city`: 城市名称
- `address`: 中国天气网城市天气页面URL

### word表
存储晚安语录：
- `Chinese`: 晚安话语文本

## 邮件内容示例

邮件包含：
- 精美图片
- 随机晚安语录
- 明日天气情况（天气、最高/最低温度）
- 温馨的晚安祝福

## 注意事项

1. **邮箱配置**: 使用QQ邮箱需要开启SMTP服务并获取授权码
2. **数据库编码**: 建议使用utf8mb4字符集支持中文
3. **网络请求**: 爬虫和天气获取依赖网络连接
4. **定时任务**: 确保服务器稳定运行，程序会持续运行等待定时任务
5. **数据一致性**: user表的city字段必须与weather表的city字段匹配

## 扩展计划

- 添加早晨邮件功能
- 支持更多邮箱服务提供商
- 添加邮件模板自定义功能
- 实现用户订阅/退订功能
- 添加天气预警功能

## 许可证

本项目仅供学习和个人使用，请遵守相关法律法规。

## 贡献
欢迎提交Issue和Pull Request来改进项目。--643541775@qq.com



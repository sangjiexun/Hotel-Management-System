# Hotel Management System

A Flask-based hotel/conference room booking system with reservation management and availability checking.

## 中文说明

### 项目简介
Hotel Management System是一个基于Flask框架开发的酒店/会议室预订系统，具有预订管理和可用性检查功能。

### 技术架构

#### 后端技术栈
- Python 3.x
- Flask 1.1.1
- Flask-SQLAlchemy
- Flask-Login (用户认证)
- Flask-Migrate (数据库迁移)
- SQLite (数据库)

#### 前端技术栈
- HTML5
- CSS3
- Jinja2模板引擎

### 功能模块

1. **用户管理**
   - 用户注册和登录
   - 个人信息管理
   - 密码重置

2. **团队管理**
   - 团队创建和管理
   - 团队成员管理

3. **会议室管理**
   - 会议室信息管理
   - 会议室设备管理（电话、投影仪、白板）
   - 会议室费用管理

4. **会议预订**
   - 会议创建和管理
   - 会议室预订
   - 会议时间管理

5. **参会人员管理**
   - 内部人员参会管理
   - 外部合作伙伴参会管理

6. **费用管理**
   - 会议费用计算
   - 费用日志记录
   - 团队费用统计

### 数据库设计

主要表结构：
- `user` - 用户信息
- `team` - 团队信息
- `room` - 会议室信息
- `meeting` - 会议信息
- `businesspartner` - 业务合作伙伴信息
- `participants_user` - 用户参会记录
- `participants_partner` - 合作伙伴参会记录
- `cost_log` - 费用日志

### 快速开始

#### 环境要求
- Python 3.x

#### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/sangjiexun/Hotel-Management-System.git
cd Hotel-Management-System
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 初始化数据库
```bash
flask db init
flask db migrate
flask db upgrade
```

4. 启动应用
```bash
python lab2.py
```

#### 测试账户
默认测试账户：
- 用户名：admin
- 密码：admin123

### 项目结构

```
Hotel-Management-System/
├── app/
│   ├── templates/       # 模板文件
│   │   ├── _formhelpers.html
│   │   ├── addteam.html
│   │   ├── adduser.html
│   │   ├── allrecords.html
│   │   ├── base.html
│   │   ├── book.html
│   │   ├── cancelbooking.html
│   │   ├── costcheck.html
│   │   ├── costs.html
│   │   ├── deleteteam.html
│   │   ├── deleteuser.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── meetingbooker.html
│   │   ├── meetingparticipants.html
│   │   ├── meetingparticipantscheck.html
│   │   ├── register.html
│   │   ├── roomavailable.html
│   │   ├── roomavailablelist.html
│   │   ├── roomoccupation.html
│   │   └── roomoccupationlist.html
│   ├── __init__.py      # 应用初始化
│   ├── forms.py         # 表单定义
│   ├── models.py        # 数据库模型
│   └── routes.py        # 路由定义
├── migrations/          # 数据库迁移文件
├── config.py            # 配置文件
├── lab2.db              # SQLite数据库
├── lab2.py              # 主应用文件
├── populate.py          # 数据填充脚本
├── test.py              # 测试脚本
└── README.md            # 项目说明
```

### 主要API

- `GET /` - 首页
- `GET /login` - 登录页面
- `POST /login` - 登录提交
- `GET /register` - 注册页面
- `POST /register` - 注册提交
- `GET /book` - 会议预订页面
- `POST /book` - 预订提交
- `GET /roomavailable` - 会议室可用性检查
- `GET /roomoccupation` - 会议室占用情况
- `GET /costs` - 费用管理页面
- `GET /allrecords` - 所有记录页面

## English Documentation

### Project Introduction
Hotel Management System is a Flask-based hotel/conference room booking system with reservation management and availability checking functionality.

### Technical Architecture

#### Backend Technology Stack
- Python 3.x
- Flask 1.1.1
- Flask-SQLAlchemy
- Flask-Login (user authentication)
- Flask-Migrate (database migration)
- SQLite (database)

#### Frontend Technology Stack
- HTML5
- CSS3
- Jinja2 template engine

### Feature Modules

1. **User Management**
   - User registration and login
   - Personal information management
   - Password reset

2. **Team Management**
   - Team creation and management
   - Team member management

3. **Room Management**
   - Conference room information management
   - Room equipment management (telephone, projector, whiteboard)
   - Room cost management

4. **Meeting Booking**
   - Meeting creation and management
   - Room reservation
   - Meeting time management

5. **Participant Management**
   - Internal participant management
   - External business partner management

6. **Cost Management**
   - Meeting cost calculation
   - Cost log recording
   - Team cost statistics

### Database Design

Main tables:
- `user` - User information
- `team` - Team information
- `room` - Conference room information
- `meeting` - Meeting information
- `businesspartner` - Business partner information
- `participants_user` - User participation records
- `participants_partner` - Partner participation records
- `cost_log` - Cost logs

### Quick Start

#### Requirements
- Python 3.x

#### Installation Steps

1. Clone the repository
```bash
git clone https://github.com/sangjiexun/Hotel-Management-System.git
cd Hotel-Management-System
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Initialize database
```bash
flask db init
flask db migrate
flask db upgrade
```

4. Start the application
```bash
python lab2.py
```

#### Test Account
Default test account:
- Username: admin
- Password: admin123

### Project Structure

```
Hotel-Management-System/
├── app/
│   ├── templates/       # Template files
│   │   ├── _formhelpers.html
│   │   ├── addteam.html
│   │   ├── adduser.html
│   │   ├── allrecords.html
│   │   ├── base.html
│   │   ├── book.html
│   │   ├── cancelbooking.html
│   │   ├── costcheck.html
│   │   ├── costs.html
│   │   ├── deleteteam.html
│   │   ├── deleteuser.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── meetingbooker.html
│   │   ├── meetingparticipants.html
│   │   ├── meetingparticipantscheck.html
│   │   ├── register.html
│   │   ├── roomavailable.html
│   │   ├── roomavailablelist.html
│   │   ├── roomoccupation.html
│   │   └── roomoccupationlist.html
│   ├── __init__.py      # Application initialization
│   ├── forms.py         # Form definitions
│   ├── models.py        # Database models
│   └── routes.py        # Route definitions
├── migrations/          # Database migration files
├── config.py            # Configuration file
├── lab2.db              # SQLite database
├── lab2.py              # Main application file
├── populate.py          # Data population script
├── test.py              # Test script
└── README.md            # Project documentation
```

### Main APIs

- `GET /` - Home page
- `GET /login` - Login page
- `POST /login` - Login submission
- `GET /register` - Registration page
- `POST /register` - Registration submission
- `GET /book` - Meeting booking page
- `POST /book` - Booking submission
- `GET /roomavailable` - Room availability check
- `GET /roomoccupation` - Room occupation status
- `GET /costs` - Cost management page
- `GET /allrecords` - All records page

## License

This project is licensed under the MIT License - see the LICENSE file for details.
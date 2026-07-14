# 🏥 Medical Data Analysis Platform

> 基于 Python、PostgreSQL 与 Power BI 构建的端到端医疗数据分析平台。

![医疗数据分析总览](docs/images/dashboard-overview.png)

## 📌 项目简介

本项目模拟医疗机构的数据分析与数据治理流程，覆盖合成医疗数据生成、PostgreSQL 数据存储、数据标准化、数据质量检查、医学宽表构建、指标分析、自动化报告及 Power BI 交互式看板。

项目主要用于展示从原始医疗业务数据到可视化决策支持的完整分析链路。

## 🏗 系统架构

```mermaid
flowchart TD
    A[合成医疗数据生成器<br/>Faker + Python] --> B[(PostgreSQL 数据库)]
    B --> C[数据读取<br/>SQLAlchemy]
    C --> D[数据标准化<br/>性别与 ICD 映射]
    D --> E[数据质量检查<br/>患者、诊断、用药规则]
    E --> F[医学宽表构建<br/>Pandas Merge]
    F --> G[业务指标分析<br/>KPI 与 EDA]

    G --> H[Excel 自动报告<br/>OpenPyXL]
    G --> I[Python 图表<br/>Matplotlib]

    B --> J[Power BI 数据模型]
    J --> K[DAX 业务指标]
    K --> L[医疗运营总览]
    K --> M[患者画像分析]
    K --> N[疾病与用药分析]
    K --> O[运营分析]
    K --> P[数据质量监控]
```

## 📊 Dashboard Showcase

### 🏠 Dashboard

![Dashboard](docs/images/dashboard-overview.png)

---

### 👤 Patient Analysis

![Patient](docs/images/patient-analysis.png)

---

### 🩺 Clinical Analytics

![Clinical](docs/images/clinical-analytics.png)

---

### 🏥 Operational Analytics

![Operational](docs/images/operational-analytics.png)

---

### 🛡 Data Quality Dashboard

![Quality](docs/images/data-quality-dashboard.png)

## ✨ Features

### 📂 Data Generation

- Generate **1000+ synthetic patients**
- Generate **3000+ visit records**
- Generate diagnosis and medication records
- Inject configurable abnormal data for quality testing

---

### 🗄 Data Management

- PostgreSQL healthcare database
- Relational data model
- Modular data loader
- Environment-based configuration (.env)

---

### 🧹 Data Quality

- Gender standardization
- ICD diagnosis standardization
- Age validation
- Diagnosis validation
- Medication validation
- Hospital quality ranking

---

### 📈 Business Analytics

- Patient profile analysis
- Clinical analytics
- Operational analytics
- Hospital KPI
- Medical wide table
- Automated Excel reports

---

### 📊 Business Intelligence

- Interactive Power BI Dashboard
- DAX KPI measures
- Multi-page dashboards
- Drill-down analysis
- Data quality monitoring

## 🛠 Tech Stack

| Layer | Technology | Responsibility |
|---|---|---|
| Programming | Python 3.12 | 数据生成、清洗与分析 |
| Database | PostgreSQL | 医疗业务数据存储 |
| Data Access | SQLAlchemy | 数据库连接与访问 |
| Data Processing | Pandas | ETL 与统计分析 |
| Visualization | Matplotlib | 静态分析图表 |
| Business Intelligence | Power BI | 交互式分析看板 |
| BI Modeling | DAX | KPI 与业务指标计算 |
| Data Generation | Faker | 合成医疗数据生成 |
| Report Export | OpenPyXL | Excel 报告生成 |
| Configuration | python-dotenv | 环境变量管理 |

## 📁 Project Structure

```text
medical-data-analysis-platform/
├── analysis/          # 指标与业务分析
├── generator/         # 合成医疗数据生成
├── loader/            # PostgreSQL 数据读取
├── quality/           # 数据质量规则
├── standard/          # 字段与 ICD 标准化
├── visualization/     # Python 图表生成
├── report/            # Excel 报告生成
├── powerbi/           # Power BI 看板文件
├── docs/
│   ├── diagrams/      # 架构图、ER 图源文件
│   └── images/        # README 展示图片
├── sql/               # 数据库初始化脚本
├── config.py
├── logger.py
├── main.py
└── requirements.txt
```

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/huhu-0026/medical-data-analysis-platform.git
cd medical-data-analysis-platform
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env`

```text
DB_DRIVER=postgresql+psycopg2
DB_HOST=localhost
DB_PORT=5432
DB_NAME=medical_data_practice
DB_USER=postgres
DB_PASSWORD=your_password
DATASET_MODE=synthetic
```

### 4. Run

```bash
python main.py
```

### 5. Open Power BI

Open

```
powerbi/medical_data_analysis_dashboard.pbix
```


## 📜 License

This project is released under the MIT License.

## 🗄 Database Model

![ER Diagram](docs/images/er-diagram.png)
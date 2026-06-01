## Walmart Retail Analytics Platform

### Overview

Designed and implemented an end-to-end retail analytics platform leveraging Snowflake, dbt, SQL, and Python to transform raw retail sales data into actionable business insights.

The platform leverages modern data engineering practices, including dimensional modeling, analytics engineering, and automated reporting to analyze store performance, sales trends, markdown effectiveness, and operational metrics.

## Architecture

```text
Raw Walmart Sales Data
        ↓
Snowflake Data Warehouse
        ↓
dbt Transformations
        ↓
Star Schema Data Model
        ↓
Python Analytics & Reporting
        ↓
Business Intelligence Insights
```

## Technology Stack

- Snowflake
- dbt
- SQL
- Python
- Pandas
- Matplotlib
- Git
- GitHub

## Data Model

### Fact Tables
- Fact Sales

### Dimension Tables
- Dim Store
- Dim Date
- Dim Department

## Business Questions Answered

- Which stores generate the highest revenue?
- Which departments perform best?
- How do markdowns impact sales?
- How does seasonality affect revenue?
- Which store types drive the strongest performance?

## Key Deliverables

- Designed and implemented a cloud data warehouse in Snowflake
- Developed analytics engineering transformations using dbt
- Built a dimensional star schema data model
- Automated reporting workflows using Python
- Delivered business intelligence reporting and visualization solutions

## Sample Reports

### Holiday Sales Impact Analysis
Compared holiday and non-holiday sales performance across 45 stores to identify seasonal demand patterns and revenue opportunities.
<img width="1402" height="701" alt="Screenshot 2026-04-30 at 10 36 44 PM" src="https://github.com/user-attachments/assets/a837d196-b038-47ed-9034-01a5709f375a" />

### Markdown Effectiveness Analysis
Evaluated promotional markdown strategies across multiple years to understand the relationship between discount programs and revenue generation.
<img width="1541" height="717" alt="Screenshot 2026-04-30 at 10 40 02 PM" src="https://github.com/user-attachments/assets/40c6a663-0ce6-42fb-ab7c-66e26faa75b1" />

### Store Size Performance Analysis
Analyzed the relationship between store size and weekly sales performance to identify scaling trends and operational efficiencies.
<img width="1541" height="791" alt="Screenshot 2026-04-30 at 10 38 23 PM" src="https://github.com/user-attachments/assets/f4259939-d5b2-47b5-a2b7-ffde583febf0" />

## Key Insights

- Holiday periods consistently generated higher sales across most stores.
- Larger stores generally produced higher weekly revenue, indicating a positive relationship between store size and sales performance.
- Promotional markdown strategies demonstrated measurable impact on sales volume and customer demand.
- Store performance varied significantly across locations, highlighting opportunities for targeted operational improvements.
- Seasonal patterns influenced sales performance, supporting the importance of demand forecasting and inventory planning.


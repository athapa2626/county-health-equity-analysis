# Federal County-Level Health & Socioeconomic Analytics Pipeline

## Project Overview

This project demonstrates the end-to-end data analytics lifecycle by integrating multiple public federal datasets into a unified county-level analytical database. The objective is to build a reproducible data pipeline that acquires, validates, cleans, integrates, analyzes, and visualizes data from multiple government agencies.

The project combines socioeconomic indicators, population health measures, healthcare access metrics, and Medicare utilization data to identify county-level patterns across the United States.

Rather than focusing on individual people, the analysis is performed at the county level using publicly available federal datasets. The final product is an analysis-ready dataset, SQL database, and Power BI dashboard that can be used to answer policy-relevant questions related to healthcare access, socioeconomic conditions, disability, and Medicare utilization.

---

# Why I Built This Project

I designed this project to simulate the type of work performed by federal data analysts and consultants supporting government agencies.

The project closely follows the responsibilities described in the TSPI Data Analyst position by demonstrating the ability to:

- Acquire data from multiple federal sources
- Clean and validate datasets
- Perform data quality assurance (QA/QC)
- Integrate heterogeneous datasets using common identifiers
- Build reproducible data pipelines
- Store structured data in SQL
- Perform exploratory and statistical analysis
- Develop dashboards and communicate findings

The project emphasizes reproducibility, documentation, and data stewardship rather than simply producing visualizations.

---

# Alignment with the TSPI Data Analyst Role

This project directly demonstrates experience with responsibilities listed in the job description.

| Job Responsibility | How this Project Demonstrates It |
|-------------------|----------------------------------|
| Data intake | Download data from APIs and federal data portals |
| Data cleaning | Handle missing values, duplicates, inconsistent formats, and standardize variables |
| Data validation | QA/QC checks before and after transformations |
| Data transformation | Engineer county-level metrics and derived variables |
| Data storage | Load cleaned datasets into SQL |
| Data analysis | Analyze relationships between socioeconomic and healthcare indicators |
| SQL development | Write SQL queries for joins, validation, and analysis |
| Python programming | Build automated data acquisition and cleaning scripts |
| Dashboard development | Create Power BI dashboard for stakeholders |
| Technical documentation | Maintain reproducible project documentation |

---

# Project Objectives

Build an end-to-end analytics pipeline that demonstrates the complete data lifecycle from acquisition through reporting.

Answer questions such as:

- Do counties with higher poverty rates also experience worse health outcomes?
- Is Medicare utilization associated with healthcare provider shortages?
- How does disability prevalence relate to socioeconomic conditions?
- Are rural counties disproportionately affected by healthcare access limitations?

---

# Data Sources

## 1. U.S. Census Bureau (ACS 5-Year)

Purpose:
Socioeconomic characteristics.

Variables include:

- Population
- Median household income
- Poverty
- Educational attainment
- Disability

---

## 2. CDC PLACES

Purpose:
Population health outcomes.

Measures include:

- Diabetes
- Obesity
- Smoking
- Physical inactivity
- Preventive healthcare indicators

---

## 3. CMS Geographic Variation

Purpose:
County-level Medicare utilization and spending.

Variables include:

- Medicare beneficiaries
- Spending
- Healthcare utilization

---

## 4. HRSA HPSA

Purpose:
Healthcare access.

Variables include:

- Primary care shortage
- Mental health shortage
- Dental shortage
- HPSA score
- Rural status

---

# Technology Stack

## Programming

- Python

Libraries:

- pandas
- requests
- python-dotenv
- numpy

---

## Database

SQL

(PostgreSQL or SQLite)

---

## Visualization

Power BI

---

## Development

VS Code

Git

GitHub

---

# Project Architecture

Raw Federal Data

↓

Python Data Acquisition

↓

Raw CSV Storage

↓

Python Data Cleaning

↓

Clean CSV Files

↓

SQL Database

↓

SQL Validation

↓

SQL Analysis

↓

Power BI Dashboard

---

# Folder Structure

```

federal-health-analytics/

data/
raw/
cleaned/
final/

scripts/

sql/

notebooks/

dashboard/

README.md

plan.md

requirements.txt

```

---

# Milestones

## Milestone 1 — Project Setup

Objective

Create the project structure and development environment.

Tasks

- Create repository
- Configure VS Code
- Create virtual environment
- Install dependencies
- Create folder structure
- Configure Git

Deliverable

Working project structure.

---

## Milestone 2 — Data Acquisition

Objective

Acquire all raw federal datasets.

Tasks

- Download CDC dataset
- Download CMS dataset
- Download HRSA dataset
- Retrieve ACS data through Census API
- Store all datasets in `/data/raw`

Deliverable

Four raw datasets.

---

## Milestone 3 — Data Profiling

Objective

Understand each dataset before cleaning.

Tasks

- Explore variables
- Identify missing values
- Check duplicate records
- Inspect data types
- Identify join keys
- Create data dictionary

Deliverable

Data profiling notebook and data dictionary.

---

## Milestone 4 — Data Cleaning

Objective

Clean each dataset independently.

Tasks

- Rename columns
- Handle missing values
- Remove duplicates
- Standardize FIPS codes
- Engineer derived variables
- Export cleaned datasets

Deliverable

Four cleaned datasets.

---

## Milestone 5 — SQL Database

Objective

Build an integrated county-level database.

Tasks

- Create SQL tables
- Import cleaned datasets
- Define relationships
- Create SQL views

Deliverable

Integrated SQL database.

---

## Milestone 6 — Data Quality (QA/QC)

Objective

Validate the integrated dataset.

Tasks

- Verify joins
- Check record counts
- Detect null values
- Identify duplicate FIPS
- Compare summary statistics

Deliverable

QA report.

---

## Milestone 7 — Exploratory Data Analysis

Objective

Identify meaningful county-level patterns.

Tasks

- Summary statistics
- Correlation analysis
- Geographic comparisons
- Feature engineering

Deliverable

EDA notebook.

---

## Milestone 8 — Dashboard Development

Objective

Communicate findings.

Tasks

- Build Power BI dashboard
- Add KPIs
- Create maps
- Add trend charts
- Build county comparison views

Deliverable

Interactive dashboard.

---

## Milestone 9 — Documentation

Objective

Document the project for reproducibility.

Tasks

- Complete README
- Document pipeline
- Explain design decisions
- Add screenshots
- Write project summary

Deliverable

Complete GitHub portfolio project.

---

# Expected Learning Outcomes

Upon completion, this project demonstrates the ability to:

- Acquire data from multiple federal systems
- Build reproducible ETL pipelines
- Clean and validate complex datasets
- Integrate heterogeneous data sources
- Perform SQL-based analysis
- Produce stakeholder-ready dashboards
- Document technical work professionally

These skills closely align with the responsibilities of an entry-level Data Analyst supporting federal healthcare and public-sector analytics projects.
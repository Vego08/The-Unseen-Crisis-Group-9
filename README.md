# The-Unseen-Crisis-Group-9

An interactive data storytelling dashboard exploring global inequality in mental health access, infrastructure, and treatment availability. The project combines healthcare, economic, and mental health indicators to uncover how countries with lower economic capacity often face significantly higher treatment gaps and weaker mental health support systems.

Rather than functioning as a traditional dashboard, this project was designed as a human-centered narrative experience that guides stakeholders from awareness to intervention through interactive visual storytelling.

---

# Project Objective

The objective of this project is to highlight the unequal global burden of mental health challenges and demonstrate how economic inequality, healthcare investment, and infrastructure availability influence access to mental healthcare systems worldwide.

The dashboard was designed for policymakers, healthcare stakeholders, researchers, and global organizations to support awareness, insight generation, and policy-focused decision-making.

---

# Narrative Structure

## A Silent Global Crisis

Introduces the global scale and severity of mental health challenges using geographic visualization.

## Not All Countries Suffer Equally

Explores the relationship between economic capacity and mental healthcare access through inequality analysis.

## Access to Care Is the Real Divide

Highlights disparities in mental health infrastructure, workforce availability, and treatment systems.

## Intervention Can Change Outcomes

Demonstrates how increased investment and policy intervention can improve mental healthcare readiness through interactive simulations.

---

# Dashboard Features

* Interactive Choropleth Map
* GDP vs Treatment Gap Scatter Analysis
* Healthcare Infrastructure Visualizations
* What-If Policy Simulation
* Dynamic Region & Income Filters
* Interactive Hover Tooltips
* Dark-Themed Design System
* Responsive Interactive Layout

---

# Advanced Features Implemented

## 1. Context-Aware Filtering

Interactive filters dynamically update dashboard visuals and analytical insights based on selected regions and income groups.

## 2. Rich Interactive Tooltips

Hover interactions reveal additional contextual information including GDP, population, crisis index, and treatment gap indicators.

## 3. What-If Simulation

Users can simulate increases in mental health investment to observe projected changes in system readiness and treatment gaps.

---

# Technologies Used

* Python
* Streamlit
* Plotly
* Pandas
* Tableau Public (Exploratory Prototyping)
* GitHub

---

# Project Structure

```text
project-folder/
│
├── app.py
├── requirements.txt
├── merged_dataset.xlsx
├── assets/
│   ├── background.png
│   ├── logo.png
│
├── README.md
```

---

# How to Run the Project

## 1. Clone the Repository

```bash
git clone https://github.com/Vego08/The-Unseen-Crisis-Group-9.git
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Launch Streamlit Dashboard

```bash
streamlit run app.py
```

---

# Data Dictionary

| Variable Name             | Data Type      | Description                                                                                                                                                           | Source / Provenance                  |
| ------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `country`                 | Text           | Name of the country included in the analysis. Used as the primary geographic identifier across all visuals and interactions.                                          | WHO / World Bank                     |
| `iso3`                    | Text           | ISO-3 country code used for choropleth map rendering and geographic mapping.                                                                                          | ISO Country Standards                |
| `region`                  | Text           | Geographic region classification of each country (e.g., Europe, Africa, Asia). Used for grouping and comparative analysis.                                            | World Bank Regional Classification   |
| `income_group`            | Text           | Economic classification of countries based on income level (Low, Lower-Middle, Upper-Middle, High Income).                                                            | World Bank                           |
| `gdp_per_capita`          | Numeric (USD)  | Gross Domestic Product per capita representing the economic capacity of a country. Used to explore economic inequality and healthcare accessibility.                  | World Bank 2024                      |
| `population_millions`     | Numeric        | Estimated total population of the country in millions. Used for proportional scaling in scatter plots and contextual interpretation.                                  | United Nations / World Bank          |
| `total_affected_millions` | Numeric        | Estimated number of individuals affected by mental health challenges in each country (in millions). Used to demonstrate scale and impact.                             | WHO Global Mental Health Estimates   |
| `mh_crisis_index`         | Numeric        | Composite index representing the overall severity of mental health challenges within a country. Higher values indicate greater crisis intensity.                      | Derived from multiple WHO indicators |
| `treatment_gap_pct`       | Percentage (%) | Percentage of individuals requiring mental health support who are unable to access adequate treatment or services. Used as a core indicator of healthcare inequality. | WHO Mental Health Atlas              |
| `psychiatrists_per100k`   | Numeric        | Number of psychiatrists available per 100,000 people. Used to evaluate workforce availability and healthcare infrastructure readiness.                                | WHO Mental Health Atlas              |
| `mh_budget_pct_health`    | Percentage (%) | Percentage of a country's healthcare budget allocated specifically toward mental health services and infrastructure.                                                  | WHO / National Health Reports        |
| `mh_system_score`         | Numeric        | Composite score evaluating the readiness and effectiveness of national mental health systems, including infrastructure, workforce, and funding capacity.              | Derived analytical metric            |
| `data_year`               | Numeric (Year) | Year associated with the collected mental health and economic indicators. Ensures temporal consistency across analysis.                                               | Consolidated dataset metadata        |

---

# Data Sources and Credits

* World Health Organization (WHO)
* World Bank
* United Nations Population Data
* Global Mental Health Reports (2024–2025)
* Streamlit
* Plotly
* Tableau Public

---
# Collaboration and Workflow

This project followed an integrated and highly collaborative studio workflow, where all team members contributed across multiple stages of dashboard development, storytelling, visual refinement, and presentation preparation.

The team primarily collaborated through WhatsApp communication and regular in-person working sessions at the University of Technology Sydney. Across the duration of the project, the group conducted approximately 7–8 in-person collaboration sessions, each averaging around 4 hours, alongside multiple virtual Google Meet discussions for progress reviews and integration.

Rather than dividing the project into isolated tasks, the team adopted a collaborative co-development approach where major design, storytelling, and analytical decisions were collectively discussed, researched, reviewed, and finalized before implementation. This ensured consistency across the dashboard narrative, visual design system, and stakeholder-focused storytelling structure.

All dashboard concepts, visual choices, interaction logic, and narrative directions were iteratively refined through group feedback and discussion.

## Team Contributions

### Dashboard Development

All team members contributed to dashboard planning, ideation, and development.

### Data Cleaning and Preparation

* Vedang Gosavi
* Prachi Dhimate

### Narration and Storytelling

* Pon Saranya Krishnan

### UI and Visual Design

* Pon Saranya Krishnan
* Rohan Yadav
* Chakshu Karwal

### Presentation Development

* Vedang Gosavi
* Chakshu Karwal
* Rohan Yadav

### Documentation

* Nana Ama Goldwater
* Pon Saranya Krishnan

### Visual Asset Design

* Rohan Yadav
* Chakshu Karwal
* Nana Ama Goldwater

### GitHub Integration and Repository Management

* Prachi Dhimate
* Vedang Gosavi
* Rohan Yadav

The project workflow emphasized collaborative iteration, shared accountability, and continuous peer feedback throughout the development process.

---

# Contributors

* Dashboard Development
* Data Cleaning and Analysis
* Narrative Design and Storytelling
* Visual Design and Presentation
* Documentation and Deployment

---

# Key Insight

The project demonstrates that the global mental health crisis is not solely a healthcare issue, but a structural inequality issue shaped by economic capacity, healthcare investment, and access to treatment systems.

> “Every statistic in this crisis was once a person asking for help.”

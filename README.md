# Multi-Source Business Dashboard

Real-time business intelligence dashboard aggregating data from multiple sources.

## 🔗 [View Live Dashboard Demo](https://mhmd-py-tech.github.io/multi-source-dashboard/dashboard.html)

## Problem It Solves
Founders waste 5-10 hours/week manually checking multiple platforms:
- Sales spreadsheets
- Customer databases  
- External market data

This dashboard unifies everything in one real-time view.

## What It Does
Pulls data from 3 sources and creates a unified visual dashboard:

**Source 1: CSV File** (Sales Data)
- Total revenue calculation
- Closed deals tracking
- Performance metrics

**Source 2: Google Sheets** (Customer Data)
- Total customer count
- Plan distribution
- Growth tracking

**Source 3: Live API** (Market Data)
- Real-time USD/EUR exchange rates
- Currency trend visualization

## Features
- ✨ Animated metric cards
- 📊 Interactive charts (Chart.js)
- 🎨 Modern glassmorphic design
- ⚡ Real-time data updates
- 🔄 Multi-source synchronization
- 🛡️ Error handling for all data sources

## Business Value
**Saves 5-10 hours per week** of manual data aggregation and reporting.

**Perfect for:**
- Executive dashboards
- Investor reporting
- Team performance tracking
- Multi-platform data consolidation

**Custom implementation:** $3,000-8,000

## How To Use

### Setup
1. Get Google Sheets API credentials from https://console.cloud.google.com/
2. Save as `credentials.json` in project folder
3. Create your data sources:
   - `sales_data.csv` with columns: date, customer, amount, status
   - Google Sheet called "Customer List"

### Run
```bash
python main.py
```

Opens `dashboard.html` in your browser with live data.

## Technical Stack
- Python (data processing)
- Google Sheets API (cloud data)
- Exchange Rate API (live market data)
- Chart.js (visualizations)
- Modern CSS (animations, glassmorphism)

## What I Learned
- Multi-source data integration
- Building production-grade dashboards
- Real-time API integration
- Prompt engineering for UI/UX design with AI
- Prompt engineering for Chart.js for interactive visualizations
- OAuth authentication

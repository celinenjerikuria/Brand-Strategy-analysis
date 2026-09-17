# Brand Strategy Analysis
A Python data analysis project examining pricing, stockout rates, and estimated lost revenue across fashion brands sold on ASOS.

## Overview

This project analyzes a dataset of 18,000 ASOS product listings to answer a simple business question: **which brands are losing the most revenue to stockouts, and how does that relate to their pricing strategy?**

The script cleans and standardizes brand names from raw product descriptions, calculates a stockout rate for each product based on unavailable sizes, and estimates lost revenue as price × number of out-of-stock sizes. It then aggregates these metrics by brand and visualizes the relationship between average price, stockout rate, and total lost revenue.

##  Key Findings

- **ASOS's own label** had the highest estimated lost revenue (£472,000) across 4,844 products, despite a mid-range average price (£46.57).
- **Topshop** followed with £76,000 in estimated lost revenue across 1,017 products.
- Several smaller brands (e.g. Mango, Naked, Pull&Bear) combined above-average pricing (>£40) with high stockout rates (>40%) — a pattern that may indicate demand outpacing supply on higher-margin items.

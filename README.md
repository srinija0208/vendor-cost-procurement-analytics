
# Vendor Performance & Procurement Analytics

## Project Overview
This project analyzes procurement, sales, and freight data for a retail/wholesale distribution business to evaluate vendor performance beyond simple sales volume. Using SQL, Python, statistical hypothesis testing, and a 2-page Power BI dashboard, it identifies which vendor relationships are operationally efficient — and which are quietly eroding margin through freight costs, slow turnover, or over-concentration risk.

## Business Problem
Beyond identifying which vendors sell well, the business needs to know which vendor relationships are operationally efficient and which are quietly costing money through hidden freight inefficiencies, slow-moving inventory, or over-dependence on a small supplier base. This analysis answers five specific questions:

1. Which vendors have disproportionately high freight cost relative to volume shipped?
2. How do vendors rank when scored jointly on margin, turnover, and volume — not sales alone?
3. Which brands combine low sales with high profit margin, making them strong candidates for promotional action?
4. Does purchasing in bulk reduce unit cost, and what's the optimal order size?
5. Is the profit margin gap between top and low-performing vendors statistically significant, or just noise from sales volume?

## Dataset
Raw data spans six tables — `purchases` (2.3M+ rows), `sales` (12.8M+ rows), `purchase_prices`, `vendor_invoice`, `begin_inventory`, and `end_inventory` — ingested into a SQLite database (`inventory.db`). `begin_inventory`/`end_inventory` were loaded during ingestion but not used in the core vendor-level analysis, since the data lacks time-stamped snapshots needed for true days-on-hand inventory turnover.

A CTE-based SQL query consolidates purchase, sales, and freight data at the vendor-brand level into a single analytical table, `vendor_sales_summary`.

**Final columns:** `VendorNumber, VendorName, Brand, Description, PurchasePrice, ActualPrice, Volume, TotalPurchaseQuantity, TotalPurchaseDollars, TotalSalesQuantity, TotalSalesDollars, TotalSalesPrice, TotalExciseTax, FreightCost, FreightCostPerUnit, GrossProfit, ProfitMargin, StockTurnover, SalesToPurchaseRatio`, plus engineered features: `MarginScore`, `TurnoverScore`, `VolumeScore`, `VendorTier`, `UnitPurchasePrice`, `OrderSize`, `UnsoldInventoryValue`, `IsTargetBrand`.

**Note on `StockTurnover`:** calculated as `TotalSalesQuantity / TotalPurchaseQuantity` — a sales-to-purchase ratio proxy, not a true days-on-hand inventory turnover metric. Treated as a directional risk signal, not an exact holding-cost figure.

## Tech Stack
Python (Pandas, NumPy, Matplotlib, Seaborn, SciPy) · SQL (SQLite) · Power BI

## Approach
```
Raw CSVs
   ↓
SQLite Database (ingestion + logging)
   ↓
SQL Aggregation (CTE-based vendor-brand summary)
   ↓
Python Data Cleaning & Feature Engineering
   ↓
Exploratory Data Analysis
   ↓
Statistical Hypothesis Testing
   ↓
Business Insights
   ↓
Power BI Dashboard
```

1. **Ingestion:** Raw CSVs loaded into SQLite via a chunked ingestion script, with logging for row counts and load time.
2. **Aggregation:** SQL CTEs join purchase, sales, and freight data at the vendor-brand level.
3. **Cleaning:** Removed rows with negative/zero gross profit, margin, or sales quantity (data quality issues, confirmed via distribution and outlier analysis) — reducing the dataset to records with valid, sellable transactions.
4. **Feature engineering:** Freight cost per unit, vendor tiering (composite score across margin/turnover/volume quartiles), order-size buckets, unsold inventory value, and a target-brand flag for promotional candidates.
5. **Statistical testing:** Compared profit margins between top-quartile and bottom-quartile vendors (by sales) using a two-sample t-test, cross-validated with a Mann-Whitney U test, plus 95% confidence intervals for both groups.

## Key Findings
- **Overall performance:** $441.41M in total sales, $134.07M gross profit, 30.37% overall profit margin, across 118 vendors.
- **Vendor concentration risk:** The top 10 vendors contribute 65.7% of total purchase spend — the remaining 100+ vendors combined supply only about a third, indicating meaningful supply-chain dependency risk.
- **Freight inefficiency:** Vendors like Martignetti Companies and Diageo North America show freight cost per unit well above the norm (avg. $2.69K per unit across flagged vendors), independent of shipment volume — flagged as renegotiation candidates.
- **Bulk purchasing impact:** Larger order sizes reduce unit purchase price by roughly 72% compared to the smallest order tier.
- **Promotional candidates:** A distinct cluster of brands (flagged via `IsTargetBrand`) combines high profit margin with low sales volume — strong candidates for promotional investment rather than pricing changes.
- **Statistically validated margin gap:** Low-volume vendors run significantly higher profit margins (95% CI: 40.5%–42.6%) than high-volume vendors (95% CI: 30.7%–31.6%), confirmed via t-test and Mann-Whitney U (p < 0.0001) — indicating two genuinely different vendor operating models (premium/niche vs. volume-driven), not a sampling artifact.
- **Unsold inventory:** $2.71M in capital remains tied up in unsold stock (avg. stock turnover proxy: 2.03), concentrated among a handful of vendors.

## Business Insights
- A small number of vendors drive the majority of both revenue and procurement spend — the business is structurally dependent on a small supplier base.
- Sales volume alone is a poor proxy for vendor quality: several high-volume vendors score lower once margin and turnover are factored in jointly, while some lower-volume vendors are genuinely more profitable per dollar sold.
- Profitability strategy differs by vendor type: high-volume vendors should be managed for efficiency and cost, while low-volume/high-margin vendors and brands are better served by promotional investment.

## Business Recommendations
- Diversify procurement across a broader vendor base to reduce supply-chain concentration risk.
- Renegotiate freight terms with vendors showing disproportionately high cost per unit.
- Shift toward bulk ordering where the ~72% unit-cost reduction justifies the storage/cash-flow tradeoff.
- Invest in promotional activity for high-margin, low-volume brands rather than adjusting price.
- Continue monitoring vendor tiers (margin × turnover × volume) rather than ranking vendors by sales alone.

## Power BI Dashboard

**Page 1 — Vendor & Brand Performance Overview:** total sales, gross profit, purchase spend, and overall margin KPIs; top 10 vendors by sales; bottom 10 brands by profit margin; vendor purchase concentration (Pareto); brands flagged for promotional/pricing action.

**Page 2 — Efficiency & Risk Deep-Dive:** avg. freight cost per unit, total unsold inventory value, avg. stock turnover, and vendors flagged high-risk KPIs; freight cost inefficiency ranking; vendor tier segmentation (margin vs. turnover, sized by sales volume); bulk purchase unit-price impact; statistical significance callout on the vendor margin gap.

`![Page 1](images\page1.png)`
`![Page 2](images\page2.png)`

## Repository Structure
```
Vendor-Performance-Analytics/
│
├── notebooks/
│   ├── ingestion_db.ipynb
│   ├── eda.ipynb
│   └── vendor_performance_analysis.ipynb
├── scripts/
│   ├── data_ingestion.py
│   └── vendor_summary.py
├── data/                                 # raw CSVs
├── dashboard/
│   └── Vendor_Performance_Dashboard.pbix
├── images/                               # dashboard screenshots
└── README.md
```

## How to Run
1. Place raw CSVs in the `data/` folder.
2. Run `python scripts/data_ingestion.py` to load them into `inventory.db`.
3. Run `python scripts/vendor_summary.py` to build the `vendor_sales_summary` table.
4. Open `notebooks/vendor_performance_analysis.ipynb` and run top to bottom for the full analysis and final CSV export.
5. Open `dashboard/Vendor_Performance_Dashboard.pbix` in Power BI Desktop and point the data source to the exported `vendor_sales_summary.csv`.

## Skills Demonstrated
SQL query design (CTEs, multi-table joins) · data cleaning & feature engineering · exploratory data analysis · statistical hypothesis testing (t-test, Mann-Whitney U, confidence intervals) · business intelligence dashboard design · business recommendation writing

## Author
Srinija — Data Analyst | [LinkedIn](#) | [Portfolio](#)
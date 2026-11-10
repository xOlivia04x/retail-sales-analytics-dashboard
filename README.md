# Retail Sales Analytics Dashboard

An original Python, SQLite, Pandas, Plotly, and Streamlit portfolio project that analyzes fictional retail transactions.

## Features

- Filter sales by date and product category
- View revenue, transactions, and units sold
- Explore revenue trends and category/product comparisons
- Inspect individual sales records and export filtered CSV data
- Store repeatable fictional sample transactions in SQLite
- Run automated database tests

## Run locally

Requires Python 3.9+.

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows, use `py` instead of `python` if needed. The dashboard typically opens at http://localhost:8501.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Architecture

`database.py` initializes SQLite and seeds deterministic demonstration data. `app.py` queries SQLite, analyzes transactions with Pandas, and presents interactive charts through Streamlit and Plotly. `tests/test_database.py` validates seeding and database constraints.

## Data and limitations

All transactions are **synthetic and fictional**. They are not derived from a real employer or customer. Prices and quantities are illustrative, and revenue is computed as quantity × unit price, without taxes, returns, or discounts. This is an educational portfolio dashboard, not a production reporting system.

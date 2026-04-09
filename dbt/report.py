import snowflake.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from dotenv import load_dotenv
import os

load_dotenv()

# ------- Connection to Snowflake -------
def get_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse='COMPUTE_WH',
        database='WALMART_DB',
        schema='DBT_KALLEYNE'
    )

# --------------- Chart 1 ---------------
def sales_by_store_and_holiday(conn):
    query = """
    SELECT 
        store_id,
        is_holiday,
        sum(store_weekly_sales) as total_weekly_sales
    FROM fct_walmart_sales s
    JOIN dim_walmart_date w ON s.DATE_ID = w.DATE_ID 
    GROUP BY store_id, is_holiday
    ORDER BY store_id
    """

    df = pd.read_sql(query, conn)
    
    print(df.head())

    pivot_df = df.pivot(index='STORE_ID', columns='IS_HOLIDAY', values='TOTAL_WEEKLY_SALES').fillna(0)

    false_sales = pivot_df.get(False, pd.Series(0, index=pivot_df.index))
    true_sales = pivot_df.get(True, pd.Series(0, index=pivot_df.index))

    x = np.arange(len(pivot_df.index))
    width = 0.4

    plt.figure(figsize=(14, 7))
    plt.bar(x - width/2, false_sales, width, label='FALSE')
    plt.bar(x + width/2, true_sales, width, label='TRUE')

    plt.title('Weekly Sales by Store and Holiday')
    plt.xlabel('Store ID')
    plt.ylabel('Total Sales')

    plt.xticks(x, pivot_df.index, rotation=45)

    plt.gca().yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda y, _: f'${y:,.0f}')
    )

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Is Holiday')
    plt.tight_layout()
    plt.show()

# --------------- Chart 2 ---------------
def weekly_sales_by_store_size(conn):
    query = """
    WITH unique_stores AS (
        SELECT
            store_id,
            MAX(store_size) AS store_size
        FROM dim_walmart_store
        GROUP BY store_id
    ),
    sales_by_size AS (
        SELECT
            u.store_size,
            SUM(s.store_weekly_sales) AS total_weekly_sales
        FROM fct_walmart_sales s
        JOIN unique_stores u
            ON s.store_id = u.store_id
        GROUP BY u.store_size
    )
    SELECT
        store_size,
        total_weekly_sales
    FROM sales_by_size
    ORDER BY store_size
    """

    df = pd.read_sql(query, conn)
    
    print(df.head())
    
    plt.figure(figsize=(14, 7))
    plt.plot(df['STORE_SIZE'], df['TOTAL_WEEKLY_SALES'])
    plt.fill_between(df['STORE_SIZE'], df['TOTAL_WEEKLY_SALES'], alpha=0.3)

    plt.title('Weekly Sales by Store Size')
    plt.xlabel('Store Size')
    plt.ylabel('Total Weekly Sales')

    plt.gca().yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda y, _: f'${y/1e6:.0f}M')
    )

    plt.gca().xaxis.set_major_formatter(
        ticker.FuncFormatter(lambda x, _: f'{int(x/1000)}K')
    )

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# --------------- Chart 3 ---------------


# ---------- MAIN ----------
if __name__ == "__main__":
    conn = get_connection()
    
    sales_by_store_and_holiday(conn)
    weekly_sales_by_store_size(conn)
    
    conn.close()
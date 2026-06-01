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
def weekly_sales_by_temp_and_year(conn):
    query = """
    SELECT
        YEAR(dt.store_date) AS year,
        ROUND(s.store_temperature, 0) AS store_temperature,
        SUM(s.store_weekly_sales) AS total_sales
    FROM fct_walmart_sales s
    JOIN dim_walmart_date dt
        ON dt.date_id = s.date_id
    GROUP BY
        YEAR(dt.store_date), ROUND(s.store_temperature, 0)
    ORDER BY
        store_temperature, year
    """

    df = pd.read_sql(query, conn)
    
    print(df.head())

    pivot_df = df.pivot(
            index='STORE_TEMPERATURE',
            columns='YEAR',
            values='TOTAL_SALES'
        ).fillna(0)

    x = np.arange(len(pivot_df.index))
    width = 0.25
    years = list(pivot_df.columns)

    plt.figure(figsize=(16, 7))

    for i, year in enumerate(years):
        plt.bar(
            x + (i - len(years)/2) * width + width/2,
            pivot_df[year],
            width,
            label=str(year)
        )

    plt.title('Weekly Sales by Temperature and Year')
    plt.xlabel('Store Temperature')
    plt.ylabel('Total Weekly Sales')

    plt.xticks(x, [f'{temp:.1f}' for temp in pivot_df.index], rotation=45)

    plt.gca().yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda y, _: f'${y/1e6:.1f}M')
    )

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Year')
    plt.tight_layout()
    plt.show()
# --------------- Chart 3 ---------------
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
# --------------- Chart 4 ---------------
def weekly_sales_by_store_type_and_month(conn):
    query = """
        SELECT
            MONTH(dt.store_date) AS month_num,
            TO_VARCHAR(dt.store_date, 'MMMM') AS month_name,
            st.store_type,
            SUM(s.store_weekly_sales) AS total_sales
        FROM FCT_WALMART_SALES s
        JOIN DIM_WALMART_STORE st 
            ON st.STORE_ID = s.STORE_ID
        JOIN DIM_WALMART_DATE dt 
            ON dt.DATE_ID = s.DATE_ID
        GROUP BY 
            MONTH(dt.store_date),
            TO_VARCHAR(dt.store_date, 'MMMM'),
            st.store_type
        ORDER BY 
            month_num,
            st.store_type
    """

    df = pd.read_sql(query, conn)

    df.columns = df.columns.str.lower()

    print(df.head())
    print(df.columns)

    pivot_df = df.pivot(
        index=["month_num", "month_name"],
        columns="store_type",
        values="total_sales"
    ).reset_index()

    pivot_df = pivot_df.sort_values("month_num")

    # Plot
    plt.figure(figsize=(12, 7))

    for store_type in ["A", "B", "C"]:
        if store_type in pivot_df.columns:
            plt.plot(
                pivot_df["month_name"],
                pivot_df[store_type],
                marker="o",
                label=store_type
            )

    plt.title("Weekly Sales by Month and Store Type", fontsize=16)
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.legend(title="Store Type")
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()
# --------------- Chart 5 ---------------
def markdown_sales_by_year_and_store(conn):
    query = """
        SELECT 
            YEAR(dt.store_date) as year,
            SUM(s.MARKDOWN1) as markdown1,
            SUM(s.MARKDOWN2) as markdown2,
            SUM(s.MARKDOWN3) as markdown3,
            SUM(s.MARKDOWN4) as markdown4,
            SUM(s.MARKDOWN5) as markdown5    
        FROM FCT_WALMART_SALES s
        JOIN DIM_WALMART_DATE dt ON s.date_id = dt.date_id
        GROUP BY YEAR(dt.store_date)
        """
    
    df = pd.read_sql(query, conn)
    
    print(df.head())
    
    x = np.arange(len(df['YEAR']))
    width = 0.15

    plt.figure(figsize=(12, 6))

    plt.bar(x - 2*width, df['MARKDOWN1'], width, label='MarkDown1')
    plt.bar(x - width,   df['MARKDOWN2'], width, label='MarkDown2')
    plt.bar(x,           df['MARKDOWN3'], width, label='MarkDown3')
    plt.bar(x + width,   df['MARKDOWN4'], width, label='MarkDown4')
    plt.bar(x + 2*width, df['MARKDOWN5'], width, label='MarkDown5')

    plt.title('MarkDown1 to MarkDown5 by Year')
    plt.xlabel('Year')
    plt.ylabel('Total Markdown Amount')

    plt.xticks(x, df['YEAR'])

    plt.gca().yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda y, _: f'{y/1e9:.2f}bn')
    )

    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# ---------- MAIN ----------
if __name__ == "__main__":
    conn = get_connection()
    
    #sales_by_store_and_holiday(conn)
    #weekly_sales_by_temp_and_year(conn)
    #weekly_sales_by_store_size(conn)
    weekly_sales_by_store_type_and_month(conn)
    #markdown_sales_by_year_and_store(conn)
    conn.close()
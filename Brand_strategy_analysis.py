"""
Product Strategy Analysis

using the ASOS product dataset, clean the brand metadata, analyzes
stockout patterns, and estimates the revenue impact by brand.

"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CSV_PATH = Path(__file__).resolve().parent / "products_asos.csv"


def get_brand(text):
    """Extract a raw brand name from a product description string."""
    text = str(text or "").strip()
    if "by " in text.lower():
        try:
            return text.lower().split("by ")[1].split(" ")[0].title()
        except Exception:
            return "unknown"
    return "unknown"


def calculate_stockout_metrics(size_str):
    """Return (out_of_stock_count, stockout_rate) for a size string."""
    if not isinstance(size_str, str):
        return 0, 0.0

    sizes = [s.strip() for s in size_str.split(",") if s.strip()]
    total_sizes = len(sizes)
    out_of_stock_count = size_str.lower().count("out of stock")
    stockout_rate = out_of_stock_count / total_sizes if total_sizes > 0 else 0.0
    return out_of_stock_count, stockout_rate


def load_and_clean_data(csv_path):
    """Load the raw CSV and apply basic cleaning."""
    csv_path = Path(csv_path)
    if not csv_path.is_file():
        raise FileNotFoundError(
            f"Input dataset not found: {csv_path}. "
            "Place 'products_asos.csv' beside this script."
        )

    df = pd.read_csv(csv_path, on_bad_lines="skip")

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"]).copy()
    df["description"] = df["description"].fillna("").astype(str)

    print(f"Data loaded: {len(df)} rows")
    return df


def assign_brands(df):
    """Derive a cleaned 'brand' column from product descriptions."""
    df["brand_raw"] = df["description"].apply(get_brand)

    brand_map = {
        "New": "New Look",
        "River": "River Island",
        "Miss": "Miss Selfridge",
        "Topshopwelcome": "Topshop",
        "TopshopWelcome": "Topshop",
        "ASOS": "ASOS",
    }
    df["brand"] = df["brand_raw"].map(brand_map).fillna(df["brand_raw"])

    brand_counts = df["brand"].value_counts()
    valid_brands = brand_counts[brand_counts > 5].index
    df_clean = df[df["brand"].isin(valid_brands)].copy()

    print(df_clean["brand"].value_counts().head())
    return df_clean


def compute_stockout_and_revenue(df_clean):
    """Add stockout count/rate and estimated lost revenue columns."""
    metrics = df_clean["size"].apply(calculate_stockout_metrics)
    df_clean["stockout_count"] = [m[0] for m in metrics]
    df_clean["stockout_rate"] = [m[1] for m in metrics]
    df_clean["lost_revenue"] = df_clean["price"] * df_clean["stockout_count"]
    return df_clean


def summarize_by_brand(df_clean):
    """Aggregate price, stockout rate, and lost revenue per brand."""
    brand_summary = df_clean.groupby("brand", as_index=False).agg(
        avg_price=("price", "mean"),
        avg_stockout_rate=("stockout_rate", "mean"),
        lost_revenue=("lost_revenue", "sum"),
        product_count=("name", "count"),
    )

    brand_summary = brand_summary[brand_summary["product_count"] > 10].sort_values(
        "lost_revenue", ascending=False
    )
    print(brand_summary.head(5))
    return brand_summary


def plot_brand_strategy(df_clean):
    """Scatter plot of average price vs. stockout rate, sized by lost revenue."""
    brand_strategy = (
        df_clean.groupby("brand")
        .agg(
            price=("price", "mean"),
            stockout_rate=("stockout_rate", "mean"),
            lost_revenue=("lost_revenue", "sum"),
            name=("name", "count"),
        )
        .reset_index()
    )

    brand_strategy = brand_strategy[brand_strategy["name"] > 10]

    plt.figure(figsize=(12, 8))
    sns.scatterplot(
        data=brand_strategy,
        x="price",
        y="stockout_rate",
        size="lost_revenue",
        hue="lost_revenue",
        sizes=(50, 500),
        alpha=0.7,
        palette="viridis",
    )

    winners = brand_strategy[
        (brand_strategy["price"] > 40) & (brand_strategy["stockout_rate"] > 0.4)
    ]

    for i in range(len(winners)):
        plt.text(
            winners.iloc[i]["price"] + 1,
            winners.iloc[i]["stockout_rate"],
            winners.iloc[i]["brand"],
        )

    plt.title("Brand Strategy Analysis")
    plt.xlabel("Average Price")
    plt.ylabel("Stockout Rate")
    plt.axvline(x=40, color="red", linestyle="--")
    plt.axhline(y=0.4, color="red", linestyle="--")
    plt.savefig("brand_strategy_analysis.png", dpi=150, bbox_inches="tight")
    plt.close()


def main():
    df = load_and_clean_data(CSV_PATH)
    df_clean = assign_brands(df)
    df_clean = compute_stockout_and_revenue(df_clean)
    summarize_by_brand(df_clean)
    plot_brand_strategy(df_clean)


if __name__ == "__main__":
    main()
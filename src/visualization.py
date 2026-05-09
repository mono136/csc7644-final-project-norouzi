import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress


def plot_group(df, group_col, title):
    """
    Plot median degradation trend for each group.

    Uses normalized cycle to compare batteries with different lifetimes.
    """

    plt.figure()

    for g in df[group_col].unique():
        df_g = df[df[group_col] == g].copy()

        # Normalize cycle for fair comparison across batteries
        df_g["cycle_norm"] = df_g.groupby("file")["cycle"].transform(
            lambda x: x / x.max()
        )

        curve = df_g.groupby("cycle_norm")["capacity"].median()
        plt.plot(curve.index, curve.values, linewidth=2, label=g, alpha=0.9)

    plt.xlabel("Normalized Cycle")
    plt.ylabel("Capacity")

    plt.title(title)
    plt.legend()
    plt.grid()

    # Save plot automatically
    os.makedirs("outputs", exist_ok=True)
    plt.savefig(f"outputs/{group_col}_trend.png")

    plt.show()


def plot_box(df, group_col):
    """
    Plot boxplot of capacity distribution for each group.
    """

    plt.figure()

    sns.boxplot(x=df[group_col], y=df['capacity'])

    plt.xlabel(group_col)
    plt.ylabel("Capacity")

    plt.title(f"Capacity Distribution - {group_col}")

    # Save plot
    os.makedirs("outputs", exist_ok=True)
    plt.savefig(f"outputs/{group_col}_box.png")

    plt.show()


def plot_single_battery(df_b, battery_name, save=True):
    """
    Plot degradation curve for a single battery.
    """

    plt.figure()

    plt.plot(
        df_b['cycle'],
        df_b['capacity'],
        linewidth=2,
        label=battery_name
    )

    plt.xlabel("Cycle")
    plt.ylabel("Capacity")

    # Add initial capacity reference line
    initial = df_b['capacity'].iloc[0]
    plt.axhline(
        y=initial,
        linestyle='--',
        label='Initial Capacity'
    )

    # Add trend line using regression
    if len(df_b) > 2:
        slope, intercept, _, _, _ = linregress(
            df_b['cycle'],
            df_b['capacity']
        )
        trend = intercept + slope * df_b['cycle']
        plt.plot(
            df_b['cycle'],
            trend,
            linestyle='--',
            label='Trend'
        )

    plt.title(f"Battery Degradation - {battery_name}")
    plt.legend()
    plt.grid()

    # Save plot if enabled
    if save:
        os.makedirs("outputs", exist_ok=True)
        plt.savefig(f"outputs/{battery_name}.png")

    plt.show()
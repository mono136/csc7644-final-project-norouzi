import numpy as np
from scipy.stats import linregress


def compute_group_summary(df, group_col):
    """
    Compute degradation statistics for each group.

    Parameters:
        df (DataFrame): Preprocessed battery dataset
        group_col (str): Column used for grouping

    Returns:
        summary (str): Text summary of statistics
        best_group (str): Group with fastest degradation
    """

    summary = ""
    best_group = None
    best_slope = 0  # more negative → faster degradation

    for g in df[group_col].unique():
        df_g = df[df[group_col] == g]

        slopes = []

        for file in df_g['file'].unique():
            df_b = df_g[df_g['file'] == file]

            # Minimum 20 cycles required for reliable regression
            if len(df_b) < 20:
                continue

            # Linear regression: capacity vs cycle
            # slope < 0 → degradation
            slope = linregress(df_b['cycle'], df_b['capacity']).slope
            slopes.append(slope)

        if not slopes:
            continue

        avg = np.mean(slopes)
        std = np.std(slopes)

        if avg < best_slope:
            best_slope = avg
            best_group = g

        summary += (
            f"\nGroup: {g}\n"
            f"Avg: {avg:.6f}\n"
            f"Std: {std:.6f}\n"
            f"Count: {len(slopes)}\n"
        )

    return summary, best_group
import numpy as np


def get_temp_group(temp):
    """
    Categorize temperature.
    - ~24°C → treated as Low/Room
    - ~43–45°C → High
    """

    if temp <= 25:
        return "Low/Room Temp"
    else:
        return "High Temp"


def is_dynamic(current):
    """
    Detect dynamic vs constant load.

    Uses standard deviation instead of max difference
    to avoid noise misclassification.
    """

    # More robust than max(diff)
    return np.std(current) > 0.5


def get_load_level(current):
    """
    Categorize load level based on average current magnitude.
    """

    avg = np.mean(np.abs(current))

    if avg < 1.5:
        return "Low"
    elif avg < 3:
        return "Medium"
    else:
        return "High"


def preprocess(df):
    """
    Clean dataset and generate derived features.
    """

    df = df[df['capacity'] > 0.5].copy()

    df['temp_group'] = df['temp'].apply(get_temp_group)

    df['load_type'] = df['current'].apply(
        lambda x: "Dynamic" if is_dynamic(x) else "Constant"
    )

    df['load_level'] = df['current'].apply(get_load_level)

    return df

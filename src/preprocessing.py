import numpy as np


def get_temp_group(temp):
    """Categorize temperature."""
    if temp < 10:
        return "Low Temp"
    elif temp > 40:
        return "High Temp"
    return "Room Temp"


def is_dynamic(current):
    """
    Detect dynamic load based on current variation.
    """
    return np.max(np.abs(np.diff(current))) > 1


def get_load_level(current):
    """Categorize load level."""
    avg = np.mean(np.abs(current))
    if avg < 1.5:
        return "Low"
    elif avg < 3:
        return "Medium"
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
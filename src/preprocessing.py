import numpy as np


def get_temp_group(temp):
    """
    Categorize temperature into three groups:

    - Low Temp:  temp < 10°C
    - Room Temp: 10°C ≤ temp ≤ 30°C
    - High Temp: temp > 30°C

    Note:
    The current dataset mostly contains ~24°C and ~43–45°C.
    Therefore, Low Temp may not appear unless such data exists.
    """

    if temp < 10:
        return "Low Temp"
    elif temp <= 30:
        return "Room Temp"
    else:
        return "High Temp"


def is_dynamic(current):
    """
    Detect whether the load profile is dynamic or constant.

    Uses standard deviation of current signal:
    - std > 0.5 → Dynamic
    - std ≤ 0.5 → Constant

    More robust than max(diff), which is sensitive to noise.
    """

    return np.std(current) > 0.5


def get_load_level(current):
    """
    Categorize load level based on average current magnitude.

    - Low:    avg < 1.5
    - Medium: 1.5 ≤ avg < 3
    - High:   avg ≥ 3
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

    Steps:
    1. Remove invalid capacity values
    2. Assign temperature group
    3. Classify load type (Dynamic / Constant)
    4. Assign load level (Low / Medium / High)

    Returns:
        Processed DataFrame with new feature columns
    """

    # Remove invalid/noisy entries
    df = df[df['capacity'] > 0.5].copy()

    # Assign temperature group
    df['temp_group'] = df['temp'].apply(get_temp_group)

    # Assign load type
    df['load_type'] = df['current'].apply(
        lambda x: "Dynamic" if is_dynamic(x) else "Constant"
    )

    # Assign load level
    df['load_level'] = df['current'].apply(get_load_level)

    return df

import os
import scipy.io
import pandas as pd


def load_mat(file_path):
    """
    Load MATLAB battery dataset and extract discharge cycles.
    """

    mat_data = scipy.io.loadmat(file_path)
    battery = mat_data[list(mat_data.keys())[-1]]
    cycles = battery[0, 0]['cycle'][0]

    rows = []

    for i, cycle in enumerate(cycles):
        # Only discharge cycles are relevant
        if cycle['type'][0] == 'discharge':
            data = cycle['data'][0, 0]

            if len(data['Capacity'][0]) == 0:
                continue

            rows.append({
                'file': os.path.basename(file_path),
                'cycle': i,
                'capacity': data['Capacity'][0][0],
                'current': data['Current_measured'][0],
                'temp': cycle['ambient_temperature'][0][0]
            })

    return pd.DataFrame(rows)


def load_all_data(folder):
    """
    Load all .mat files from a folder.
    """

    all_data = []

    for file in os.listdir(folder):
        if file.endswith(".mat"):
            df = load_mat(os.path.join(folder, file))
            all_data.append(df)

    return pd.concat(all_data, ignore_index=True)
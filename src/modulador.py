import pandas as pd
import numpy as np

def get_avg_sheet(dfs_names: list[str]) -> pd.DataFrame:
    """
    Receives a list of dataframes, like-sized,
    and returns a dataframe with the most frequent values on each cell
    """
    dfs = [pd.read_csv(file) for file in dfs_names]
    shape = dfs[0].shape
    if any(df.shape != shape for df in dfs):
        print("Dataframes must have the same shape")
        return None
    cols = dfs[0].columns
    n_rows = len(dfs[0])
    freq_row = pd.DataFrame(columns=cols)
    for c in cols:
        for r in range(n_rows):
            avg_cell = []
            for df in dfs:
                val = df.loc[r, c]
                # identifies invalid values, like NaN
                # and inserts a '-' instead
                if type(val) == float and np.isnan(val):
                    avg_cell.append("-")
                    continue
                avg_cell.append(val)
            avg_cell = pd.Series(avg_cell).mode()
            freq_row.loc[r, c] = avg_cell[0]    
    return freq_row

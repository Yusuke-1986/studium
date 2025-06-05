import pandas as pd
import numpy as np
import os

class Signal:
    """
    # Signal Object class
    simple signal object
    - label: signal name
    - unit: signal unit
    - data: measurement data as numpy array
    """
    def __init__(self, label: str, unit: str, data: np.ndarray):
        self.label = label
        self.unit = unit

        try:
            self.data = data.astype(np.float32)
        except:
            self.data = data

class DataContainer:
    """
    # Signal container
    each signal container
    - all_signal: all signal object, label:Signal object
    - freq: sampling rate, default=0.1 sec(10 Hz)
    - x_axis: x axis data, sample count × freq
    - ofs: offset counter
    - labels: all signal label
    """
    def __init__(self, df:pd.DataFrame, freq: float = 0.1):
        self.all_signal = {}

        self.freq = freq
        self.ofs = 0
        self.x_axis = np.array([i * self.freq for i in range(len(df.index))], dtype="float32")

        self.labels = df.iloc[0, :].tolist()
        units = df.iloc[1, :].tolist()
        
        for i in range(len(self.labels)):
            self.all_signal[self.labels[i]] = Signal(self.labels[i], units[i], df.iloc[3:, i].to_numpy())

    def __getitem__(self, label: str) -> Signal:
        return self.all_signal[label]

    def offset(self, ofs: float):
        self.ofs = ofs

    def get_time_axis(self) -> np.ndarray:
        return self.x_axis + self.ofs

def format_checker(dframe: pd.DataFrame):
    if len(dframe.iloc[0, :]) == len(dframe.iloc[1, :]) == len(dframe.iloc[2, :]):
        return True
    else:
        return False

def structed_data_builder(path: str) -> DataContainer:
    """
    # Build structed data format
    file path -> DataContainer object
    """
    try:
       dframe = pd.read_csv(path, header=None, low_memory=False, encoding='utf-8_sig')
       file_name = os.path.basename(path)
       
       if format_checker(dframe):
           return {file_name: DataContainer(dframe)}
       else:
           raise Exception("format Error.")

    except Exception as e:
        print(f"Error while parsing {path}: {e}")
        raise

if __name__ == "__main__":
    data = structed_data_builder("./sample/test.csv")

    print(data)
    print(data["test.csv"]["label_1"].data)
    print(data["test.csv"].get_time_axis())
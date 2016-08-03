import pandas as pd
from datetime import datetime
import os

DTG_FMT = "%Y-%m-%d %H:%M:%S"


def ensure_sensors_named_and_sorted(sms_dat_path, verbose=True, force_rename=False):
    """
    Adds the "Name" column which combines the field id and the sensor id (FID and SID).
    Also sorts the entries by the Sensor name and the date/time of the reading. If
    modifications are made the original file is overwritten.

    Name has format "SMS{two digit field id}{two digit sensor id}"

    :param sms_dat_path: filepath to csv with soil data with headers
                         [FID,SID,DTG,TEMP,SENSOR8,SENSOR16,SENSOR24]
    :param force_rename: force name column to be redone, maybe convention will change
    :param verbose: print things
    """

    df = pd.read_csv(sms_dat_path)
    df["DTG"] = df["DTG"].map(lambda x: datetime.strptime(x, DTG_FMT))  # format column as datetimes

    if "NAME" not in df.columns.values or force_rename:
        df["FID"] = df["FID"].astype(int)
        df["SID"] = df["SID"].astype(int)
        df["NAME"] = "SMS" + df["FID"].map(lambda x: str(x).zfill(2)).astype(str) + \
                     df["SID"].map(lambda x: str(x).zfill(2)).astype(str)
        df.sort_values(by=["NAME", "DTG"], inplace=True)

        # ensure Name column comes out as first column for readable csvs
        column_names = list(df.columns.values)
        try:
            column_names.remove("NAME")
        except ValueError:
            pass
        column_names.insert(0, "NAME")
        df.to_csv(sms_dat_path, columns=column_names, index=False)  # overwrite input file

        if verbose:
            print("Added Names to file at {0}".format(os.path.abspath(sms_dat_path)))
    else:
        if verbose:
            print("Names already present in file at {0}".format(os.path.abspath(sms_dat_path)))


def main(folder=None):
    """
    ensure sensors have names and everything is sorted for all files in soil folder
    """

    if folder is None:
        folder = "../dat/soil"

    sms_data_files = [os.path.join(folder, fname) for fname in os.listdir(folder) if fname.endswith(".csv")]
    for sms_data_file in sms_data_files:
        ensure_sensors_named_and_sorted(sms_data_file, force_rename=True)


if __name__ == "__main__":
    main()


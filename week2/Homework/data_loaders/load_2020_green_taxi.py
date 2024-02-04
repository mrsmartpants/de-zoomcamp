import pandas as pd

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# Replace ? with 10-12
BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-?.csv.gz"

dtypes = {
    'VendorID': pd.Int64Dtype(),
    'passenger_count': pd.Int64Dtype(),
    'trip_distance': float,
    'RatecodeID': pd.Int64Dtype(),
    'store_and_fwd_flag': str,
    'PULocationID': pd.Int64Dtype(),
    'DOLocationID': pd.Int64Dtype(),
    'payment_type': pd.Int64Dtype(),
    'fare_amount': float,
    'extra': float,
    'mta_tax': float,
    'tip_amount': float,
    'tolls_amount': float,
    'improvement_surcharge': float,
    'total_amount': float,
    'ehail_fee': float,
    'congestion_surcharge': float,
}
cols_to_datetime = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

dfs = []
for month in range(10, 13):
    URL = BASE_URL.replace('?', f'{month}')
    df = pd.read_csv(URL, compression="gzip", sep=',',
                      dtype=dtypes, parse_dates=cols_to_datetime)
    dfs.append(df)

@data_loader
def load_green_taxi_from_api():
    return pd.concat(dfs, axis=0, ignore_index=True)

@test
def test_output(df, *args) -> None:
    assert df is not None, 'The output is undefined'

@test
def test_shape(df) -> None:
    assert df.shape != (0, 0), 'The dataframe has no rows'
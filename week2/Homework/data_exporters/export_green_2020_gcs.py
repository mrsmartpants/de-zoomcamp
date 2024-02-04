import pandas as pd
import pyarrow as pa
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/src/gcs_key/mages-key.json"

@data_exporter
def export_to_gcs(df) -> None:

    table = pa.Table.from_pandas(df)

    pa.parquet.write_to_dataset(
        table=table,
        root_path="gs://my-super-unique-bucket-xdddddddd",
        partition_cols=['lpep_pickup_date']
    )

    


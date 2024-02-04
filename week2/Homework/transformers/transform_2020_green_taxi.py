if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df):

    df = df[df["passenger_count"] > 0]
    df = df[df["trip_distance"] > 0]
    df['lpep_pickup_date'] = df['lpep_pickup_datetime'].dt.date
    return df


@test
def test_passenger_count(df) -> None:

    assert (df.passenger_count < 1).sum() == 0

@test
def test_trip_distance(df) -> None:

    assert(df.trip_distance == 0).sum() == 0
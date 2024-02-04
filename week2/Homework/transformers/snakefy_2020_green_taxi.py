import re
import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# Matches a lowercase character followed by an uppercase one
camel2snake = re.compile("(?P<one>[a-z])(?P<two>[A-Z])")

@transformer
def transform(df):

    # Store new column names in a list in order to make new pd.Index
    new_idx = []

    # Iterate over the dataframe's columns
    for col in df.columns:
        # Add an underscore in-between the lowercase and uppercase characters
        new_col = re.sub(camel2snake, "\g<one>_\g<two>", col)
        # Append to new_idx after converting all characters to lowercase
        new_idx.append(new_col.lower())

    df.columns = pd.Index(new_idx)

    return df


@test
def test_snakefy(df, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert 'vendor_id' in df.columns

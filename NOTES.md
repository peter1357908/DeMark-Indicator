## Accessing the data
(remember that we can chain modifier like ".head()")
* print(dataframe['Adj Close'])
* print(dataframe[['Date', 'Adj Close']])
* print(dataframe[dataframe['Adj Close'] > 1460])


## TODO


## Important Realizations
* don't forget to use the `parse_date` flag when reading with `pd.read_csv`... and know that dates in simple string are not automatically recognized by matplotlib...
* in fact, `pd.read_csv` has so many useful flags... just use them instead of trying to read the whole file and THEN manipulate the read dataframe...


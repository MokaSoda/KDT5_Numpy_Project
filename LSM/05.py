import pandas as pd

# Load the data
ilgan = pd.read_csv('/mnt/data/일간기온전처리.csv', encoding='euc-kr')
ilgan.columns = ['날짜', '지점', '평균기온', '최저기온', '최고기온']
ilgan['날짜'] = ilgan['날짜'].str.replace('\t', '')
ilgan['날짜'] = pd.to_datetime(ilgan['날짜'], format='%Y-%m-%d')

# Drop rows for missing data years as mentioned
ilgan = ilgan.drop(ilgan.index[15433:16463]) # 50~53년 결측치 제외

# Correcting seasonal data extraction
ilgan['봄'] = ilgan['날짜'].dt.month.isin([3, 4, 5])
ilgan['여름'] = ilgan['날짜'].dt.month.isin([6, 7, 8])
ilgan['가을'] = ilgan['날짜'].dt.month.isin([9, 10, 11])
ilgan['겨울'] = ilgan['날짜'].dt.month.isin([1, 2, 12])

# Now, we'll compute the seasonal statistics (like average temperatures) for each year
seasonal_avg_temps = ilgan.groupby(ilgan['날짜'].dt.year).agg({
    '봄': 'mean',
    '여름': 'mean',
    '가을': 'mean',
    '겨울': 'mean',
    '평균기온': ['mean', 'max', 'min'],
    '최고기온': 'max',
    '최저기온': 'min',
})

# Flatten the multi-level columns for easier manipulation
seasonal_avg_temps.columns = ['_'.join(col).strip() for col in seasonal_avg_temps.columns.values]

# Check the first few rows to ensure the data looks correct
seasonal_avg_temps.head()

# Filter dataset for each season and calculate statistics
seasons = {
    '봄': [3, 4, 5],
    '여름': [6, 7, 8],
    '가을': [9, 10, 11],
    '겨울': [1, 2, 12],
}

# Initialize a dictionary to store seasonal stats
seasonal_stats = {}

for season, months in seasons.items():
    # Filter for the current season
    season_data = ilgan[ilgan['날짜'].dt.month.isin(months)]
    # Calculate stats for the season
    stats = season_data.groupby(season_data['날짜'].dt.year).agg({
        '평균기온': ['mean', 'max', 'min'],
        '최고기온': 'max',
        '최저기온': 'min',
    })
    # Flatten the multi-level columns for easier manipulation
    stats.columns = [f'{season}_{col[0]}_{col[1]}' for col in stats.columns.values]
    seasonal_stats[season] = stats

# Combine seasonal stats into a single DataFrame
seasonal_stats_df = pd.concat(seasonal_stats.values(), axis=1)

# Check the first few rows of the combined seasonal statistics dataframe
seasonal_stats_df.head()

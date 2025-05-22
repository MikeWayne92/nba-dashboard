import pandas as pd
import os

def load_nba_data():
    """
    Load NBA player statistics from CSV file.
    Returns a pandas DataFrame with the data.
    """
    csv_path = 'PlayerIndex_nba_stats.csv'
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Could not find {csv_path}")
    
    df = pd.read_csv(csv_path)
    return df

def get_basic_stats(df):
    """
    Get basic statistics about the dataset.
    """
    stats = {
        'total_players': len(df),
        'active_players': len(df[df['ROSTER_STATUS'] == 1]),
        'unique_teams': df['TEAM_NAME'].nunique(),
        'years_range': f"{df['FROM_YEAR'].min()}-{df['TO_YEAR'].max()}"
    }
    return stats

def main():
    # Load the data
    print("Loading NBA player statistics...")
    df = load_nba_data()
    
    # Get and display basic stats
    stats = get_basic_stats(df)
    print("\nDataset Statistics:")
    print(f"Total Players: {stats['total_players']}")
    print(f"Active Players: {stats['active_players']}")
    print(f"Number of Unique Teams: {stats['unique_teams']}")
    print(f"Years Range: {stats['years_range']}")
    
    # Display the first few rows
    print("\nFirst few entries:")
    print(df.head())
    
    # Save processed data
    print("\nSaving processed data...")
    df.to_csv('processed_nba_stats.csv', index=False)

if __name__ == "__main__":
    main() 
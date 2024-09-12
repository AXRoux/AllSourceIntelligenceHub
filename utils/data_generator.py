import pandas as pd
import numpy as np

def generate_sample_intelligence_data(n_samples=100):
    """
    Generate a sample dataset of intelligence reports for demonstration purposes.
    """
    np.random.seed(42)  # For reproducibility

    sources = ['OSINT', 'HUMINT', 'SIGINT', 'GEOINT', 'MASINT']
    regions = ['North America', 'South America', 'Europe', 'Africa', 'Asia', 'Middle East']
    confidence_levels = ['Low', 'Medium', 'High']

    data = {
        'date': pd.date_range(start='2023-01-01', periods=n_samples),
        'source': np.random.choice(sources, n_samples),
        'region': np.random.choice(regions, n_samples),
        'confidence': np.random.choice(confidence_levels, n_samples),
        'importance': np.random.randint(1, 11, n_samples)
    }

    df = pd.DataFrame(data)
    return df

def get_source_distribution(df):
    """
    Calculate the distribution of intelligence sources.
    """
    return df['source'].value_counts().to_dict()

def get_confidence_by_source(df):
    """
    Calculate the average confidence level for each intelligence source.
    """
    confidence_map = {'Low': 1, 'Medium': 2, 'High': 3}
    df['confidence_num'] = df['confidence'].map(confidence_map)
    return df.groupby('source')['confidence_num'].mean().to_dict()

def get_importance_by_region(df):
    """
    Calculate the average importance for each region.
    """
    return df.groupby('region')['importance'].mean().to_dict()

if __name__ == "__main__":
    # Test the data generation and analysis functions
    sample_data = generate_sample_intelligence_data()
    print("Sample data shape:", sample_data.shape)
    print("\nSource distribution:")
    print(get_source_distribution(sample_data))
    print("\nConfidence by source:")
    print(get_confidence_by_source(sample_data))
    print("\nImportance by region:")
    print(get_importance_by_region(sample_data))

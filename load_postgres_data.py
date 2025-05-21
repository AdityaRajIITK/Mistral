import pandas as pd
from sqlalchemy import create_engine

def load_data_from_postgres(
    database_name,
    table_name,
    host="localhost",
    port="5432",
    user="your_username",
    password="your_password"
):
    """
    Load data from PostgreSQL table into a pandas DataFrame
    
    Parameters:
    -----------
    database_name : str
        Name of the PostgreSQL database
    table_name : str
        Name of the table to query
    host : str
        Database host address
    port : str
        Port number
    user : str
        Username for database
    password : str
        Password for database
    
    Returns:
    --------
    pandas.DataFrame
        Data loaded from the specified table
    """
    try:
        # Create the connection string
        connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
        
        # Create the SQLAlchemy engine
        engine = create_engine(connection_string)
        
        # You can either load the entire table
        df = pd.read_sql_table(table_name, engine)
        
        # Or use a custom query
        # query = "SELECT * FROM your_table WHERE some_condition"
        # df = pd.read_sql_query(query, engine)
        
        return df
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Example usage:
if __name__ == "__main__":
    # Replace these with your actual database details
    db_params = {
        "database_name": "your_database",
        "table_name": "your_table",
        "user": "your_username",
        "password": "your_password",
        "host": "localhost",
        "port": "5432"
    }
    
    df = load_data_from_postgres(**db_params)
    
    if df is not None:
        print("Data loaded successfully!")
        print("\nDataFrame Info:")
        print(df.info())
        print("\nFirst few rows:")
        print(df.head()) 
import vanna
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String, DateTime
from datetime import datetime

def create_temp_table_from_df(df, engine, table_name='node_data'):
    """
    Create a temporary table in PostgreSQL from the DataFrame
    """
    # Create table with appropriate data types
    metadata = MetaData()
    
    # Define table structure based on DataFrame dtypes
    columns = [
        Column('nodeid', String),
        Column('nodename', String),
        Column('clustername', String),
        Column('instancetype', String),
        Column('tags', String),
        Column('created', DateTime),
        Column('snapshottime', DateTime),
        Column('platform', String)
    ]
    
    # Create table
    temp_table = Table(table_name, metadata, *columns)
    metadata.create_all(engine)
    
    # Insert DataFrame into the table
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    
    return table_name

def setup_vanna_with_df(df, database_name, user, password, host="localhost", port="5432"):
    """
    Set up Vanna with DataFrame data
    """
    # Create PostgreSQL connection string
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
    
    # Create SQLAlchemy engine
    engine = create_engine(connection_string)
    
    # Create temporary table from DataFrame
    table_name = create_temp_table_from_df(df, engine)
    
    # Initialize Vanna
    vn = vanna.Vanna()  # Initialize without specifying a model
    vn.connect_to_postgres(
        host=host,
        port=port,
        database=database_name,
        user=user,
        password=password
    )
    
    return vn, table_name, engine

# Example usage in Jupyter notebook:
"""
# First, make sure you have your DataFrame 'df' loaded

# Setup connection parameters
db_params = {
    "database_name": "data",
    "user": "adityakumarraj",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

# Initialize Vanna and create temporary table
vn, table_name, engine = setup_vanna_with_df(
    df,
    database_name=db_params["database_name"],
    user=db_params["user"],
    password=db_params["password"],
    host=db_params["host"],
    port=db_params["port"]
)

# Get schema information and create training plan
df_information_schema = vn.run_sql(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS where table_name='{table_name}';")
print("Schema Information:")
print(df_information_schema)

# Generate and review training plan
plan = vn.get_training_plan_generic(df_information_schema)
print("\nTraining Plan:")
print(plan)

# Train the model
vn.train(plan=plan)

# View training data
training_data = vn.get_training_data()
print("\nTraining Data:")
print(training_data)

# Now you can ask questions about your data:
question = "What are the different instance types and their counts?"
sql = vn.generate_sql(question)
print("\nGenerated SQL:", sql)

# Execute the query
result = vn.run_sql(sql)
print("\nResult:")
print(result)

# Clean up
engine.dispose()
""" 
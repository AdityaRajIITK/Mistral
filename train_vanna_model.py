import vanna
from sqlalchemy import create_engine
import pandas as pd

def setup_vanna(database_name, user, password, host="localhost", port="5432"):
    """
    Set up Vanna with PostgreSQL connection
    """
    # Create PostgreSQL connection string
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
    
    # Initialize Vanna
    vn = vanna.VannaSQLPostgres(
        config={
            "connection_string": connection_string
        }
    )
    
    return vn

def analyze_and_train(vn, table_name):
    """
    Analyze table schema and train Vanna model
    """
    # Get schema information
    df_information_schema = vn.run_sql(
        f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS where table_name='{table_name}';"
    )
    print("\nTable Schema Information:")
    print(df_information_schema)
    
    # Generate training plan
    plan = vn.get_training_plan_generic(df_information_schema)
    print("\nTraining Plan:")
    print(plan)
    
    # Train the model
    print("\nStarting training...")
    vn.train(plan=plan)
    print("Training completed!")

if __name__ == "__main__":
    # Replace these with your actual database details
    db_params = {
        "database_name": "your_database",
        "user": "your_username",
        "password": "your_password",
        "host": "localhost",
        "port": "5432",
        "table_name": "gpu_jobs"  # Your target table
    }
    
    # Setup Vanna
    vn = setup_vanna(
        database_name=db_params["database_name"],
        user=db_params["user"],
        password=db_params["password"],
        host=db_params["host"],
        port=db_params["port"]
    )
    
    # Analyze schema and train
    analyze_and_train(vn, db_params["table_name"]) 
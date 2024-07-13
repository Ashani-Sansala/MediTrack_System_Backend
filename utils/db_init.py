import subprocess
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def init_db():
    # Get database name from environment variables
    DATABASE = os.getenv('DATABASE')

    # List of SQL files to execute in order
    sql_files = [
        'scripts/db/schema.sql',
        'scripts/db/seed.sql',
        'scripts/db/indexes.sql',
        'scripts/db/queries/query1.sql',
        'scripts/db/stored_procedures/auth_procedures.sql',
        'scripts/db/stored_procedures/dashboard_procedures.sql',
        'scripts/db/stored_procedures/managecamera_procedures.sql',
        'scripts/db/stored_procedures/manageuser_procedures.sql',
        'scripts/db/stored_procedures/profile_procedures.sql'
    ]

    # Iterate through each SQL file and execute it
    for sql_file in sql_files:
        # Ensure the file exists
        if not os.path.exists(sql_file):
            print(f"Error: File {sql_file} not found.")
            continue

        # Command to execute SQL file using MySQL client
        # Use --login-path=local for authenticated access
        command = f'mysql --login-path=local'

        # Append database name to command for all files except schema.sql
        if sql_file != sql_files[0]:
            command += f' {DATABASE}'
        
        # Redirect SQL file content into MySQL client for execution
        command += f' < "{os.path.abspath(sql_file)}"'
        
        try:
            # Execute the command using subprocess
            subprocess.run(command, shell=True, check=True)
            print(f"Executed {sql_file} successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error executing {sql_file}: {e}")
# good ol' python black magic
# by adding the local folder to the system path, we can import other python classes without a hassle
# and structure the setup for the database backend better
# not optimal for production1
import sys
import os
scriptpath = "."

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))

from db_schema import create_tables
from db_seeder import seed_db

try:
    create_tables(hard_reset=True)
    seed_db()
    print("Migrating tables and seeding data was completed successfully.")
except:
    print("Something went wrong while creating tables or seeding data.")

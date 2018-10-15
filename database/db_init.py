from db_schema import create_tables
from db_seeder import seed_db


create_tables(hard_reset=True)
seed_db()

try:
    print("Migrating tables and seeding data was completed successfully.")
except:
    print("Something went wrong while creating tables or seeding data.")

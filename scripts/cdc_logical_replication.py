import psycopg2
import logging
import os
import time
from dotenv import load_dotenv
from sql.utils import connect_to_db
from sql.utils import logging_setup

load_dotenv()
logging_setup()


def check_slot_and_publication(conn):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT slot_name FROM pg_replication_slots WHERE slot_name = 'cdc_tutorial_slot';"
        )
        slot_exists = cur.fetchone()
        cur.execute(
            "SELECT pubname FROM pg_publication WHERE pubname = 'cdc_tutorial_pub';"
        )
        publication_exists = cur.fetchone()
    return slot_exists and publication_exists


def cdc_setup(db, conn):
    with conn.cursor() as cur:
        db = db.lower()
        if db == "source":
            logging.info(f"Setting up Logical Replication on {db.upper()} node...")
            try:
                cur.execute(
                    "SELECT slot_name FROM pg_replication_slots WHERE slot_name = 'cdc_tutorial_slot';"
                )
                slot_exists = cur.fetchone()
                if not slot_exists:
                    cur.execute(
                        "SELECT pg_create_logical_replication_slot('cdc_tutorial_slot', 'pgoutput');"
                    )

                cur.execute(
                    "SELECT pubname FROM pg_publication WHERE pubname = 'cdc_tutorial_pub';"
                )
                publication_exists = cur.fetchone()
                if not publication_exists:
                    # cur.execute("CREATE PUBLICATION cdc_tutorial_pub FOR ALL TABLES;")
                    cur.execute(
                        "CREATE PUBLICATION cdc_tutorial_pub FOR TABLE public.products;"
                    )

                conn.commit()
                logging.info(
                    f"Succesfully enabled Logical Replication on {db.upper()} node."
                )
            except Exception as e:
                logging.error(f"Error setting up CDC in {db.upper()} node: {e}")
        else:
            try:
                logging.info(f"Setting up Logical Replication on {db.upper()} node...")
                cur.execute(
                    f"""
                        CREATE SUBSCRIPTION cdc_tutorial_subscription CONNECTION 'host={os.getenv("POSTGRES_SOURCE_HOST")} port=5432 dbname={os.getenv("POSTGRES_SOURCE_DB_NAME")} user={os.getenv("POSTGRES_SOURCE_USER")} password={os.getenv("POSTGRES_SOURCE_PASSWORD")}' PUBLICATION cdc_tutorial_pub WITH (copy_data=true, create_slot=false, enabled=true, slot_name=cdc_tutorial_slot);
                    """
                )
                conn.commit()
                logging.info(
                    f"Succesfully enabled Logical Replication on {db.upper()} node."
                )
            except Exception as e:
                logging.error(f"Error setting up CDC in {db.upper()} node: {e}")


if __name__ == "__main__":
    conn_source = connect_to_db("SOURCE")
    cdc_setup("SOURCE", conn_source)
    conn_source.close()

    # Wait for slot and publication to be created before proceeding
    time.sleep(10)

    conn_source = connect_to_db("SOURCE")
    while not check_slot_and_publication(conn_source):
        logging.info("Waiting for replication slot and publication to be ready...")
        time.sleep(5)
    conn_source.close()

    conn_target = connect_to_db("TARGET")
    cdc_setup("TARGET", conn_target)
    conn_target.close()

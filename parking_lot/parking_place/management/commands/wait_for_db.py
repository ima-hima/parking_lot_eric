"""
Implement wait_for_db() command so that Django doesn't attempt to start up
until the db is available.
"""

import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for db."""

    def handle(self, *args, **options):
        self.stdout.write("\nWaiting for database.")
        db_up = False
        while not db_up:
            try:
                self.check(databases=["default"])
                db_up = True
            except Psycopg2Error:
                self.stdout.write("PostgreSQL is not yet running. Waiting one second.")
            except OperationalError as e:
                if str(e):
                    self.stdout.write(f"Operational error: {e}. Waiting one second.")
                else:
                    self.stdout.write(
                        "PostgreSQL running, but db is not yet available. "
                        "Waiting one second."
                    )

                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database is available."))

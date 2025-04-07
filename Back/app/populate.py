from faker import Faker
from . import create_app, db
from app.models import Order
import random

fake = Faker()
app = create_app()

statuses = ["pending", "shipped", "delivered", "cancelled"]
BATCH_SIZE = 10_000
TOTAL_ORDERS = 1_000_000

def generate_orders():
    with app.app_context():
        db.drop_all()
        db.create_all()

        total_inserted = 0
        batch = []

        for i in range(TOTAL_ORDERS):
            order = Order(
                user=fake.name(),
                amount=round(random.uniform(10, 500), 2),
                status=random.choice(statuses),
                created_at=fake.date_time_this_year()
            )
            batch.append(order)

            if len(batch) >= BATCH_SIZE:
                db.session.bulk_save_objects(batch)
                db.session.commit()
                total_inserted += len(batch)
                print(f"{total_inserted} orders inserted...")
                batch = []

        if batch:
            db.session.bulk_save_objects(batch)
            db.session.commit()
            total_inserted += len(batch)
            print(f"{total_inserted} orders inserted. (final batch)")

if __name__ == "__main__":
    generate_orders()

from app.db.session import SessionLocal
from app.services.seed_demo_data import seed_demo_data, seed_initial_admin


def main() -> None:
    db = SessionLocal()
    try:
        seed_initial_admin(db)
        seed_demo_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()

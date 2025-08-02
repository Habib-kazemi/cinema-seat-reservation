from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.features.hall.models import Hall, Hall_position

DATABASE_URL = "postgresql://postgres:password@db:5432/cinema_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()


def populate_hall_positions():
    halls = db.query(Hall).all()
    for hall in halls:
        existing_positions = db.query(Hall_position).filter(
            Hall_position.hall_id == hall.id).count()
        if existing_positions == 0:
            for row in range(1, hall.rows + 1):
                for col in range(1, hall.columns + 1):
                    position = Hall_position(
                        hall_id=hall.id, row_index=row, column_index=col)
                    db.add(position)
            db.commit()
            print(f"Populated positions for hall {hall.id}")
        else:
            print(f"Hall {hall.id} already has positions")


if __name__ == "__main__":
    populate_hall_positions()
    db.close()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.features.hall.models import Hall_position
from src.features.reservation.models import Reservation
from src.features.showtime.models import Showtime

DATABASE_URL = "postgresql://postgres:password@db:5432/cinema_db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()


def migrate_seat_data():
    reservations = db.query(Reservation).all()
    print(f"Total reservations found: {len(reservations)}")

    if not reservations:
        print("No reservations found in the database.")
        return
    for res in reservations:
        if res.position_id is None and 'seat_number' in res.__dict__:
            seat = res.__dict__['seat_number'].upper()

            try:
                row_index = ord(seat[0]) - ord('A') + 1
                column_index = int(seat[1:])
                showtime = db.query(Showtime).filter(
                    Showtime.id == res.showtime_id).first()
                if not showtime:
                    print(f"No showtime found for reservation {res.id}")
                    continue
                position = db.query(Hall_position).filter(
                    Hall_position.hall_id == showtime.hall_id,
                    Hall_position.row_index == row_index,
                    Hall_position.column_index == column_index
                ).first()
                if position:
                    res.position_id = position.id
                    db.commit()
                    print(
                        f"Migrated reservation {res.id} to position_id {position.id}")
                else:
                    print(
                        f"No position found for seat {seat} in hall {showtime.hall_id}")
            except (ValueError, IndexError):
                print(f"Invalid seat format {seat} for reservation {res.id}")
        else:
            print(
                f"Skipping reservation {res.id}: position_id={res.position_id}")


if __name__ == "__main__":
    migrate_seat_data()
    db.close()

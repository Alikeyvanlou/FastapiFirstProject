from sqlalchemy import delete
from core.database.db import SessionLocal
from core.models.user import UserModel

def clean_up():
    db = SessionLocal()
    try:
        res = db.execute(delete(UserModel).where(UserModel.is_fake == True))
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    clean_up()
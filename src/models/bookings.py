from datetime import date
from sqlalchemy.ext.hybrid import hybrid_property
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class BookingsOrm(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    price: Mapped[int] = mapped_column()

    @hybrid_property
    def total_cost(self) -> int:
        return self.price * (self.date_to - self.date_from).days
    # Функция рассчитывает итоговую цену бронирования умножая цену за ночь на продолжительность бронирования в днях
    # Декоратор @hybrid_property позволяет использовать функцию как атрибут, что бы не вызывать booking.total_cost
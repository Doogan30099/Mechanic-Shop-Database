
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Date, ForeignKey, select
from datetime import date
from typing import List






# Create a base class for our models
class Base(DeclarativeBase):
    pass
 
#Instantiate your SQLAlchemy database

db = SQLAlchemy(model_class = Base)






customer_ticket = db.Table(
    'customer_ticket',
    Base.metadata,
    db.Column('customer_id', db.ForeignKey('customers.id')),
    db.Column('service_ticket_id', db.ForeignKey('service_tickets.id'))
)

class Mechanic(Base):
    __tablename__ = 'mechanics'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    DOB: Mapped[date] = mapped_column(Date, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(255), nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='mechanic') #New relationship attribute


class ServiceTicket(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    service_ticket_date: Mapped[date] = mapped_column(Date, nullable=False)
    customer : Mapped[str] = mapped_column(String(255), nullable=False)
    vehicle: Mapped[str] = mapped_column(String(255), nullable=False)
    task_description: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(100), nullable=False)
    mechanic_id: Mapped[int | None] = mapped_column(ForeignKey('mechanics.id'), nullable=True)


    mechanic: Mapped['Mechanic'] = db.relationship(back_populates='service_tickets') #New relationship attribute
    customers: Mapped[List['Customer']] = db.relationship(secondary=customer_ticket, back_populates='service_tickets')

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(255), nullable=False)
    vehicle: Mapped[str] = mapped_column(String(255), nullable=False)
    desc: Mapped[str] = mapped_column(String(255), nullable=False)

    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary=customer_ticket, back_populates='customers')

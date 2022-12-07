# -*- coding: utf-8 -*-
import pika, sys, os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Appeal(BaseModel):
    surname: str = Field(min_length=1)
    name: str = Field(min_length=1, max_length=100)
    patronymic: str = Field(min_length=1, max_length=100)
    phone: str = Field(min_length=12, max_length=12)
    appeal: str =Field(min_length=1)


APPEAL = []


@app.get("/")
def read_appeal(db: Session = Depends(get_db)):
    return db.query(models.Appeal).all()

@app.post("/")
def create_appeal(appeal: Appeal, db: Session = Depends(get_db)):
    
    appeal_model = models.Appeal()
    appeal_model.surname = appeal.surname
    appeal_model.name = appeal.name
    appeal_model.patronymic = appeal.patronymic
    appeal_model.phone = appeal.phone
    appeal_model.appeal = appeal.appeal

    db.add(appeal_model)
    db.commit()

    return appeal


@app.put("/{appeal_id}")
def update_appeal(appeal_id: int, appeal: Appeal, db: Session = Depends(get_db)):

    appeal_model = db.query(models.Appeal).filter(models.Appeal.id == appeal_id).first()

    if appeal_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {appeal_id} : Does not exist"
        )

    appeal_model.surname = appeal.surname
    appeal_model.name = appeal.name
    appeal_model.patronymic = appeal.patronymic
    appeal_model.phone = appeal.phone
    appeal_model.appeal = appeal.appeal

    db.add(appeal_model)
    db.commit()

    return appeal


@app.delete("/{appeal_id}")
def delete_appeal(appeal_id: int, db: Session = Depends(get_db)):

    appeal_model = db.query(models.Appeal).filter(models.Appeal.id == appeal_id).first()

    if appeal_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {appeal_id} : Does not exist"
        )

    db.query(models.Appeal).filter(models.Appeal.id == appeal_id).delete()

    db.commit()


def adding_appeal(appeal: Appeal, massage: str):
    db = SessionLocal()
    appeal_model = models.Appeal()
    appeal_model.surname,appeal_model.name, appeal_model.patronymic,appeal_model.phone,appeal_model.appeal = massage.split("_", 5)

    db.add(appeal_model)
    db.commit()

    return appeal

def main():
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        adding_appeal(Appeal, body.decode('utf8'))

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    
    

if __name__ == '__main__':
    try:
        main()
        
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)     
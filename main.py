from fastapi import FastAPI
import requests
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel

app2 = FastAPI()
Base = declarative_base()

class DataSchema(BaseModel):
    name: str
    image: str
    creationAt: str
    updatedAt: str

class DataBase(Base):
    __tablename__ = 'data'
    id = Column (Integer, primary_key = True, index = True, autoincrement = True)
    name = Column(String)
    image = Column (String)
    creationAt = Column (String)
    updatedAt = Column (String)

engine = create_engine('sqlite:///data.db')
SessionLocal = sessionmaker(bind = engine)
session = SessionLocal()
Base.metadata.create_all(bind = engine)

@app2.get("/get_url")
def get_url(url: str):
    response = requests.get(url)
    result = response.json()
    return JSONResponse(status_code = 200, content = jsonable_encoder(result))

@app2.get("/save_data")
def save_data(url: str):
    response = requests.get(url)
    data_base = response.json()

    for i in data_base:
        save = DataBase(**i)
        session.merge(save)
    session.commit()
    return JSONResponse(status_code = 200, content = {'message' : 'Base de datos guardados correctamente'})

@app2.get('/get_data')
def get_data():
    data = session.query(DataBase).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

@app2.get('/get_id/{id}')
def get_id(id : int):
    data = session.query(DataBase).get(id)
    if data:
        return JSONResponse(status_code=200, content = jsonable_encoder(data))
    else:
        return JSONResponse(status_code=404, content={'message': 'ID no encontrado'})
    
@app2.post("/new_category")
def create_category(category: DataSchema):
    new_category = DataBase(
        name=category.name,
        image=category.image,
        creationAt=category.creationAt,
        updatedAt=category.updatedAt
    )
    session.add(new_category)
    session.commit()
    return JSONResponse(status_code=201, contenent={'message': 'Categoría creada correctamente'})

@app2.put("/update_category/{id}")
def update_category(id: int, category : DataSchema):
    data = session.query(DataBase).get(id)
    if data:
        data.name = category.name
        data.image = category.image
        data.creationAt = category.creationAt
        data.updatedAt = category.updatedAt
        session.commit()
        return JSONResponse(status_code=200, content={'message': 'Categoría actualizada correctamente'})
    else:
        return JSONResponse(status_code=404, content={'message': 'ID no encontrado'})

@app2.delete('/delete_id/{id}')
def delete_id(id : int):
    data = session.query(DataBase).get(id)
    if data:
        session.delete(data)
        session.commit()
        return JSONResponse(status_code=200, content = {'message': 'ID eliminado'})
    else:
        return JSONResponse(status_code=404, content={'message': 'ID no encontrado'})

@app2.delete("/delete_data")
def delete_data():
    Base.metadata.drop_all(bind = engine)
    return JSONResponse(status_code = 200, content = {'message' : 'Base de datos borrada exitosamente'})


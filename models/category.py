from sqlalchemy import Column, String, Integer
from models import Base

class Category(Base):
    """
    Modelo para armazenar informações sobre as categorias dos livros.

    Attributes:
        id (int): ID único da categoria.
        name (str): Nome da categoria.
    """
    __tablename__ = 'book_lib_category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __init__(self, name):
        self.name = name

    def to_dict(self):
                return {
                    'id': self.id,
                    'name': self.name
                }



    def __repr__(self):
        return f"Category(name='{self.name}')"
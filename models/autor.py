from sqlalchemy import Column, String, Integer
from models import Base

class Autor(Base):
    """
    Modelo para armazenar informações sobre os autores dos livros.

    Attributes:
        id (int): ID único do autor.
        name (str): Nome do autor.
    """
    __tablename__ = 'book_lib_autor'

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
        return f"Autor(name='{self.name}')"

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class IndustryIdentifier(Base):
    """
    Modelo para armazenar informações sobre os identificadores industriais dos livros.

    Attributes:
        id (int): ID único do identificador industrial.
        type (str): Tipo de identificador (por exemplo, ISBN).
        identifier (str): Valor do identificador.
    """
    __tablename__ = 'book_lib_industry_identifiers'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    identifier = Column(String)

    def __init__(self, type, identifier):
        self.type = type
        self.identifier = identifier

    def to_dict(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "type": self.type
        }


    def __repr__(self):
        return f"IndustryIdentifier(type='{self.type}', identifier='{self.identifier}')"
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models import Base

class ImageLinks(Base):
    """
    Modelo para armazenar informações sobre os links de imagem dos livros.

    Attributes:
        id (int): ID único do link de imagem.
        smallThumbnail (str): URL da miniatura pequena.
        thumbnail (str): URL da miniatura.
    """
    __tablename__ = 'book_lib_image_links'

    id = Column(Integer, primary_key=True)
    smallThumbnail = Column(String)
    thumbnail = Column(String)

    def __init__(self, smallThumbnail, thumbnail):
        self.smallThumbnail = smallThumbnail
        self.thumbnail = thumbnail

    def to_dict(self):
        return {
            "id": self.id,
            "smallThumbnail": self.smallThumbnail,
            "thumbnail": self.thumbnail
        }

    def __repr__(self):
        return f"ImageLink(smallThumbnail='{self.smallThumbnail}', thumbnail='{self.thumbnail}')"
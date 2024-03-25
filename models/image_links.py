from sqlalchemy import Column, Integer, String
from models import Base

class ImageLinks(Base):
    """
    Modelo para armazenar informações sobre os links das imagens dos livros.

    Attributes:
        id (int): ID único do link de imagem.
        smallThumbnail (str): URL da miniatura pequena da imagem.
        thumbnail (str): URL da miniatura da imagem.
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
            'id': self.id,
            'smallThumbnail': self.smallThumbnail,
            'thumbnail': self.thumbnail
        }

    def __repr__(self):
        return f"ImageLinks(smallThumbnail='{self.smallThumbnail}', thumbnail='{self.thumbnail}')"
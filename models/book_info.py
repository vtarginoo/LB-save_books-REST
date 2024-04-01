from sqlalchemy import Column, String, Integer, UniqueConstraint, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from models import Base
from models.autor import *
from models.category import *
from models.industry_identifier import *
from models.image_links import *
from models.associations import *



class BookInfo(Base):
    
    __tablename__ = 'book_lib'

    id = Column("pk_book", Integer, primary_key=True)
    idGoogle = Column(String)  
    title = Column(String)
    subtitle = Column(String)
    publisher = Column(String)
    publishedDate = Column(String)  
    description = Column(String)
    pageCount = Column(Integer)
    printType = Column(String)
    averageRating = Column(Float)
    ratingsCount = Column(Integer)
    language = Column(String)
    status = Column(String)

    user_id = Column(Integer)

    dataInsercao = Column(DateTime, default=datetime.now())

    # Estabelecendo relacionamentos 
   
    autor = relationship('Autor', secondary=association_table_autor, backref='books')
    category = relationship('Category', secondary=association_table_category, backref='books')
    industryIdentifiers = relationship('IndustryIdentifier', secondary=association_table_industry_identifier, backref='books')
    imageLinks = relationship('ImageLinks', secondary=association_table_image_links, backref='books', uselist=False)
    
    __table_args__ = (UniqueConstraint("idGoogle","user_id", name="book_unique_id"),)

    def __init__(self, idGoogle, title, subtitle, publisher, publishedDate, description, pageCount, printType, averageRating, ratingsCount, language, status,user_id ,dataInsercao=None):
        """
        Cria um BookInfo

        Arguments:
            idGoogle: ID do Google associado ao livro.
            title: título do livro.
            subtitle: subtítulo do livro
            publisher: editora do livro
            publishedDate: data de publicação do livro
            description: Sinopse do livro
            pageCount: número de páginas do livro
            printType: tipo de impressão do livro
            averageRating: avaliação média do livro
            ratingsCount: número de avaliações do livro
            language: idioma do livro
            status: status do livro (e.g., "lido", "não lido", "lendo")
            author: autor do livro
            categories: categorias do livro
            industryIdentifiers: identificadores da indústria do livro
            imageLinks: links de imagens do livro
            dataInsercao: data de quando o livro foi inserido à base
            user_id: ID do usuário associado ao livro
        """
            
        self.idGoogle = idGoogle
        self.title = title
        self.dataInsercao = dataInsercao or datetime.now()
        self.subtitle = subtitle
        self.publisher = publisher
        self.publishedDate = publishedDate
        self.description = description
        self.pageCount = pageCount
        self.printType = printType
        self.averageRating = averageRating
        self.ratingsCount = ratingsCount
        self.language = language
        self.status = status
        self.user_id = user_id
        
        

def to_dict(self):
    return {
        "id": self.id,
        "idGoogle": self.idGoogle,
        "title": self.title,
        "dataInsercao": self.dataInsercao,
        "subtitle": self.subtitle,
        "publisher": self.publisher,
        "publishedDate": self.publishedDate,
        "description": self.description,
        "pageCount": self.pageCount,
        "printType": self.printType,
        "averageRating": self.averageRating,
        "ratingsCount": self.ratingsCount,
        "language": self.language,
        "status": self.status,
        "user_id": self.user_id,

        "dataInsercao": self.dataInsercao,
        "autor": [autor.to_dict() for autor in self.autor],
        "category": [category.to_dict() for category in self.category],
        "industryIdentifiers": [identifier.to_dict() for identifier in self.industryIdentifiers],
        "imageLinks": [imageLinks.to_dict() for imageLinks in self.imageLinks]
    }

# def __repr__(self):
#             """
#             Retorna uma representação do BookInfo em forma de texto.
#             """
#             return f"BookInfo(id={self.id}, title='{self.title}', publisher='{self.publisher}', published_date='{self.published_date}')"
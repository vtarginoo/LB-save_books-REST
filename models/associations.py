from sqlalchemy import Table, Column, Integer, ForeignKey
from models import Base 


association_table_autor = Table('association_autor', Base.metadata,
    Column('book_id', Integer, ForeignKey('book_lib.pk_book')),
    Column('autor_id', Integer, ForeignKey('book_lib_autor.id'))
)

association_table_category = Table('association_category', Base.metadata,
    Column('book_id', Integer, ForeignKey('book_lib.pk_book')),
    Column('category_id', Integer, ForeignKey('book_lib_category.id'))
)

association_table_industry_identifier = Table('association_industry_identifier', Base.metadata,
    Column('book_id', Integer, ForeignKey('book_lib.pk_book')),
    Column('industry_identifier_id', Integer, ForeignKey('book_lib_industry_identifiers.id')),
)

association_table_image_links = Table('association_image_links', Base.metadata,
    Column('book_id', Integer, ForeignKey('book_lib.pk_book')),
    Column('image_links_id', Integer, ForeignKey('book_lib_image_links.id')),
)
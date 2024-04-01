from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from schemas.others_schemas import *


class BookInfoSchema(BaseModel):
    """ Define como um novo livro a ser inserido deve ser representado.
    """
    idGoogle: str = "WFIsDwAAQBAJ"
    title: str = "Manual do guerreiro da luz"
    dataInsercao: Optional[datetime] = None
    autores: List[str] = ["Paulo Coelho"]
    categories: List[str] = ["quest", "adventure", "fantasy"]
    industryIdentifiers: List[IndustryIdentifiersSchema] 
    imageLinks: ImageLinksSchema 
    subtitle: str = "Livro"
    publisher: str = "Editora 1"
    publishedDate: str = "21/09/1999"
    description: str = "..."
    pageCount: int = 15
    printType: str = "Book"
    averageRating: float = 0
    ratingsCount: int = 0
    language: str = "en"
    status: str = "Lido"
    

class BookInfoViewSchema(BaseModel):
    """ Define como um livro será retornado.
    """
    id: int = 1
    idGoogle: str = "WFIsDwAAQBAJ"
    title: str = "Manual do guerreiro da luz"
    dataInsercao: Optional[datetime] = None
    autores: List[str] = ["Paulo Coelho"]
    categories: List[str] = ["quest", "adventure", "fantasy"]
    industryIdentifiers: List[IndustryIdentifiersSchema] 
    imageLinks: ImageLinksSchema 
    subtitle: str = "Livro"
    publisher: str = "Editora 1"
    publishedDate: str = "21/09/1999"
    description: str = "..."
    pageCount: int = 15
    printType: str = "Book"
    averageRating: float = 0
    ratingsCount: int = 0
    language: str = "en"
    status: str = "Lido"
    user_id: str = 1
    

class ListagemBookInfoSchema(BaseModel):
     """ Define como uma listagem de livros será retornada.
     """
     livros: List[BookInfoViewSchema]

class BookInfoDelSchema(BaseModel):
         """ Define como deve ser a estrutura do dado retornado após uma requisição
             de remoção de um livro.
         """
         message: str = "Livro removido com sucesso"
         id: int = 1


class BookInfoSearchByIDSchema(BaseModel):
     """ Define como deve ser a estrutura que representa a busca feita apenas com base no ID do livro.
     """
     id: int = 1 



class BookInfoSearchByTitleSchema(BaseModel):
     """ Define como deve ser a estrutura que representa a busca feita apenas com base no título do livro.
     """
     termo: str



class BookInfoSearchByStatus(BaseModel):
     """ Define como deve ser a estrutura que representa a busca feita por livros com determinado status.
     """
     status: str = "Lido"


class BookInfoAtualizaStatus(BaseModel):
     """ Define como deve ser a estrutura atualização de status de um livro.
     """
     id: int = 1
     status: str = "Lido"




class BookInfoAtualizaStatusView(BaseModel):
     """ Define como deve ser a estrutura atualização de status de um livro.
     """
     id: int = 1
     idGoogle: str = "WFIsDwAAQBAJ"
     title: str = "Manual do guerreiro da luz"
     status: str = "Lido"


class BookInfoVerifyStatusbyGoogleId(BaseModel):
     """ Define da Verificação de Existência de um livro na Library by Google ID
     """
     idGoogle: str = "WFIsDwAAQBAJ"









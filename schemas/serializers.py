from typing import List
from models.book_info import BookInfo



def apresenta_livro(livro: BookInfo):
    """ Retorna uma representação do livro seguindo o schema definido em
        BookInfoViewSchema.
    """
    autores = [autor.name for autor in livro.autor]
    categories = [category.name for category in livro.category]
    industryIdentifiers = [{
        "identifier": identifier.identifier,
        "type": identifier.type
    } for identifier in livro.industryIdentifiers]

    imageLinks = {
        "smallThumbnail": livro.imageLinks.smallThumbnail,
        "thumbnail": livro.imageLinks.thumbnail
    } if livro.imageLinks else None


    return {
        "id": livro.id,
        "idGoogle": livro.idGoogle,
        "title": livro.title,
        "dataInsercao": livro.dataInsercao,
        "autores": autores,
        "categories": categories,
        "industryIdentifiers": industryIdentifiers,
        "imageLinks": imageLinks,  
        "subtitle": livro.subtitle,
        "publisher": livro.publisher,
        "publishedDate": livro.publishedDate,
        "description": livro.description,
        "pageCount": livro.pageCount,
        "printType": livro.printType,
        "averageRating": livro.averageRating,
        "ratingsCount": livro.ratingsCount,
        "language": livro.language,
        "status": livro.status,
        "user_id":livro.user_id
         
    }


def apresenta_livros(livros: List[BookInfo]):
    """ Retorna uma representação dos livros seguindo o schema definido em ListagemBookInfoSchema.
    """
    result = []
    for livro in livros:
        autores = [autor.name for autor in livro.autor]
        categories = [category.name for category in livro.category]
        industryIdentifiers = [{
            "identifier": identifier.identifier,
            "type": identifier.type
        } for identifier in livro.industryIdentifiers]
        imageLinks = {
        "smallThumbnail": livro.imageLinks.smallThumbnail,
        "thumbnail": livro.imageLinks.thumbnail
    } if livro.imageLinks else None
        
      
        result.append({
            "id": livro.id,
            "idGoogle": livro.idGoogle,
            "title": livro.title,
            "dataInsercao": livro.dataInsercao,
            "autores": autores,
            "categories": categories,
            "industryIdentifiers": industryIdentifiers,
            "imageLinks": imageLinks,  
            "subtitle": livro.subtitle,
            "publisher": livro.publisher,
            "publishedDate": livro.publishedDate,
            "description": livro.description,
            "pageCount": livro.pageCount,
            "printType": livro.printType,
            "averageRating": livro.averageRating,
            "ratingsCount": livro.ratingsCount,
            "language": livro.language,
            "status": livro.status,
            
        })

    return {"livros": result}
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect,jsonify,request 
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from sqlalchemy.exc import IntegrityError
from logger import logger
from flask_cors import CORS
from urllib.parse import unquote

from schemas.book_info import *    
from schemas.error import *   
from schemas.serializers import *

from models import Session
from models.book_info import BookInfo
from models.autor import Autor
from models.category import Category
from models.industry_identifier import IndustryIdentifier
from models.image_links import ImageLinks

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

info = Info(title="MicroService of Book Save (Create a Library)", version="1.0.0")
app = OpenAPI(__name__, info=info)
app.config['JWT_SECRET_KEY'] = 'f548bc279fdb47da87b07d8911aed425'
app.config['JWT_TOKEN_LOCATION'] = ['headers']  # Defina a localização do token (por exemplo, nos cabeçalhos)
jwt = JWTManager(app)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
jwt_tag = Tag(name="Rotas Livro com JWT", description="Adição, visualização e remoção de livros na base de dados, estão presentes na aplicação front-end")
book_tag = Tag(name="Rotas Livro sem autenticação", description="Essas Rotas São adicionais mais ainda não presente na aplicação front-end")


# Redireciona para a página de documentação
@app.get('/', tags=[home_tag])
def home():
    return redirect('/openapi')

@app.post('/book', tags=[jwt_tag],  
          responses={"200": BookInfoSchema, "409": ErrorSchema, "400": ErrorSchema})
@jwt_required()  # Requer um token JWT válido no cabeçalho da solicitação
def add_livro(form: BookInfoSchema):
    """Adiciona um novo Livro à base de dados

    Retorna uma representação do Livro adicionado.
    """
    session = Session()
    logger.info("Iniciando o processamento para adicionar um livro.")
    try:
        #Verifica qual é o identificador do Token
        current_user = get_jwt_identity()    
        logger.info(f"Tipo de current_user: {current_user}")  # Adicione esta linha para verificar o tipo de current_user
       
        logger.info("user_id")
        
        # Cria um objeto BookInfo com os dados fornecidos no formulário
        livro = BookInfo(
            user_id=current_user,
            idGoogle=form.idGoogle,
            title=form.title,
            subtitle=form.subtitle,  
            publisher=form.publisher,
            publishedDate=form.publishedDate,
            description=form.description,
            pageCount=form.pageCount,
            printType=form.printType,
            averageRating=form.averageRating,
            ratingsCount=form.ratingsCount,
            language=form.language,
            status=form.status,
            dataInsercao=form.dataInsercao,
                    )

        # Adiciona o livro à sessão
        session.add(livro)
        logger.info("Livro adicionado ao banco de dados.")
        
        # Adiciona os identificadores da indústria ao livro
        for industryIdentifiers in form.industryIdentifiers:
            
            identifier = session.query(IndustryIdentifier).filter_by(identifier=industryIdentifiers.identifier).first()
            
            if not identifier:
               
                identifier = IndustryIdentifier(
                    identifier=industryIdentifiers.identifier,
                    type=industryIdentifiers.type
                )
                
                session.add(identifier)
                logger.info("Novo identificador da indústria criado.")
            else:
                logger.info("Identificador da indústria encontrado na base de dados.")
            livro.industryIdentifiers.append(identifier)
            logger.info("Identificador da indústria adicionado ao livro.")

        # Adiciona os links de imagem ao livro
        image = ImageLinks(
            smallThumbnail=form.imageLinks.smallThumbnail,
            thumbnail=form.imageLinks.thumbnail
        )
        # Verifica se os links de imagem já existem na base de dados
        existing_image = session.query(ImageLinks).filter_by(smallThumbnail=form.imageLinks.smallThumbnail, thumbnail=form.imageLinks.thumbnail).first()
        if not existing_image:
            # Se os links de imagem não existem, cria um novo registro para eles
            session.add(image)
            logger.info("Novos links de imagem criados.")
        else:
            # Se os links de imagem já existem, usa o registro existente
            image = existing_image
            logger.info("Links de imagem encontrados na base de dados.")
        # Associa os links de imagem ao livro
        livro.imageLinks = image
        logger.info("Links de imagem adicionados ao livro.")


        # Verifica se os autores já existem no banco de dados e os associa ao livro
        for autor_nome in form.autores:
            autor = session.query(Autor).filter_by(name=autor_nome).first()
            if not autor:
                # Se o autor não existe, cria um novo registro para ele
                autor = Autor(name=autor_nome)
                session.add(autor)
            # Adiciona o autor ao livro
            livro.autor.append(autor)
            logger.info("Autores associados ao livro.")

        # Verifica se as categorias já existem no banco de dados e as associa ao livro
        for category_name in form.categories:
            category = session.query(Category).filter_by(name=category_name).first()
            if not category:
                # Se a categoria não existe, cria um novo registro para ela
                category = Category(name=category_name)
                session.add(category)
                logger.info(f"Categoria '{category_name}' criada.")
            # Adiciona a categoria ao livro
            livro.category.append(category)
            logger.info("Categorias associadas ao livro.")

        # Realiza o commit da transação
        session.commit()
        logger.info("Livro adicionado com sucesso.")

        # Retorna uma representação do livro inserido
        return jsonify(apresenta_livro(livro)), 200

    except IntegrityError as e:
        # Retorna uma mensagem de erro se ocorrer uma violação de integridade (por exemplo, duplicidade de chave)
        error_msg = "Livro já existente na base de dados"
        logger.warning(f"Erro ao adicionar livro: {error_msg}")
        return jsonify({"message": error_msg}), 409

    except Exception as e:
        # Retorna uma mensagem de erro genérica para quaisquer outras exceções
        error_msg = "Erro ao adicionar livro"
        logger.warning(f"{error_msg}: {str(e)}")
        return jsonify({"message": error_msg}), 400

    finally:
        # Fecha a sessão
        session.close()


@app.get('/books/{book_status}', tags=[jwt_tag],
         responses={"200": ListagemBookInfoSchema, "409": ErrorSchema, "400": ErrorSchema})
@jwt_required()  # Requer um token JWT válido no cabeçalho da solicitação
def get_books_by_status(query: BookInfoSearchByStatus):
    """Faz a busca por todos os Livros cadastrados com no Status do Livro

    Retorna uma representação da listagem de Livros com base no título fornecido.
    """

    try:

        current_user = get_jwt_identity()   

        book_status = query.status
        session = Session()

        # Consulta os livros com base no status fornecido e no ID do usuário
        livros = session.query(BookInfo).filter(BookInfo.status == book_status, BookInfo.user_id == current_user).all()

        # Serializa os livros usando a função apresenta_livros
        livros_serializados = apresenta_livros(livros)

        return livros_serializados

    except Exception as e:
        error_msg = "Erro ao recuperar livros por título: " + str(e)
        print(error_msg)  # Apenas para depuração
        return {"message": error_msg}, 500 
    

    
@app.get('/book/{Google_id}', tags=[jwt_tag], 
            responses={"200": BookInfoAtualizaStatus, "400": ErrorSchema, "404": ValidateErrorSchema })
@jwt_required()
def getStatusbyGoogleId(query: BookInfoVerifyStatusbyGoogleId):
    """Faz a busca por um livro específico, usando Google Id

    Retorna uma O Id, Google Id, Título e Status

    Caso Contrário, informa que o livro não existe na Library
    """

    try:
        current_user = get_jwt_identity()
        livro_id = query.idGoogle

        # Inicia a sessão e busca o livro com o ID fornecido
        session = Session()
        livro = session.query(BookInfo).filter(BookInfo.idGoogle == livro_id, BookInfo.user_id == current_user).first()

        if not livro:
            # Serializa e retorna o livro não encontrado com o código de status 404
            livro_404 = {
                "id": "null",
                "idGoogle": livro_id,
                "title": "null",
                "status": "notFound"
            }
            return livro_404, 404
        else:
            # Serializa e retorna o livro encontrado com o código de status 200
            livro_serializado = {
                "id": livro.id,
                "idGoogle": livro.idGoogle,
                "title": livro.title,
                "status": livro.status
            }
            return livro_serializado, 200
    
    except Exception as e:
        # Loga a exceção
        error_msg = f"Erro ao buscar o livro com ID {livro_id}"
        logger.warning(f"{error_msg}: {str(e)}")
        # Retorna uma mensagem de erro genérica com o código de status 400
        return {"message": "Ocorreu um erro ao processar a solicitação."}, 400


@app.put('/book/{livro_id}', tags=[jwt_tag], 
            responses={"200": BookInfoAtualizaStatus, "404": ErrorSchema})
@jwt_required()
def put_livro(query: BookInfoAtualizaStatus):
     """Faz a busca por todos um livro de Id especifico para alterar seu status

    Retorna uma representação do livro com o status já alterado
    """

     try:
         
         current_user = get_jwt_identity()
         livro_id = query.id

         # Inicia a sessão e busca o livro com o ID fornecido
         session = Session()
         livro = session.query(BookInfo).filter(BookInfo.id == livro_id, BookInfo.user_id == current_user).first()
        
         if not livro:
             # Retorna uma mensagem de erro se o livro não for encontrado
             return {"message": f"Livro com ID {livro_id} não encontrado"}, 404
         else:
             # Atualiza o status do livro
             livro.status = query.status
             session.commit()
             
             # Serializa e retorna o livro atualizado
             livro_serializado = {
                 "id": livro.id,
                 "idGoogle": livro.idGoogle,
                 "title": livro.title,
                 "status": livro.status
             }
             return livro_serializado, 200
    
     except Exception as e:
         # Retorna uma mensagem de erro genérica para quaisquer exceções
         error_msg = f"Erro ao atualizar status do livro com ID {livro_id}"
         logger.warning(f"{error_msg}: {str(e)}")
         return {"message": error_msg}, 404

# Remove um livro específico com base no ID fornecido
@app.delete('/book/{livro_id}', tags=[jwt_tag], 
            responses={"200": BookInfoDelSchema, "404": ErrorSchema})
@jwt_required()
def del_livro(query: BookInfoSearchByIDSchema):
     """Deleta um livro a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
     try:
         current_user = get_jwt_identity()
         livro_id = query.id

         # Inicia a sessão e busca o livro com o ID fornecido
         session = Session()
         livro = session.query(BookInfo).filter(BookInfo.id == livro_id, BookInfo.user_id == current_user).first()
         
         if not livro:
             # Retorna uma mensagem de erro se o livro não for encontrado
             return {"message": f"Livro com ID {livro_id} não encontrado"}, 404
         else:
             # Remove o livro da base de dados
             session.delete(livro)
             session.commit()
             return {"message": "Livro removido com sucesso", "id": livro_id}, 200
    
     except Exception as e:
         # Retorna uma mensagem de erro genérica para quaisquer exceções
         error_msg = f"Erro ao remover livro com ID {livro_id}"
         logger.warning(f"{error_msg}: {str(e)}")
         return {"message": error_msg}, 404
     

    
###################### Rotas que não estão dentro do Front-end

 # Recupera todos os livros cadastrados na base de dados
@app.get('/books', tags=[book_tag], 
         responses={"200": ListagemBookInfoSchema, "409": ErrorSchema, "400": ErrorSchema})
@jwt_required()
def get_books():
    """Faz a busca por todos os Livros cadastrados

    Retorna uma representação da listagem de Livros.
    """

    try:
        session = Session()

        #Verifica qual é o identificador do Token
        current_user = get_jwt_identity()   

        # Consulta os livros relacionados ao usuário atual
        livros = session.query(BookInfo).filter_by(user_id=current_user).all()

        # Serializa os livros usando a função apresenta_livros
        livros_serializados = apresenta_livros(livros)

        return livros_serializados

    except Exception as e:
        error_msg = "Erro ao recuperar livros: " + str(e)
        print(error_msg)  # Apenas para depuração
        return {"message": error_msg}, 500


# Recupera um livro específico com base no ID fornecido
@app.get('/book/{livro_id}', tags=[book_tag], 
         responses={"200": BookInfoViewSchema, "404": ErrorSchema})
def get_book(query: BookInfoSearchByIDSchema):
     """Faz a busca por um Livro a partir do id do livro

    Retorna uma representação dos livros e seus atributos.
    """
     try:
         
         livro_id = query.id
         # Inicia a sessão e busca o livro com o ID fornecido
         session = Session()
         livro = session.query(BookInfo).filter(BookInfo.id == livro_id).first()
        
         if not livro:
             # Retorna uma mensagem de erro se o livro não for encontrado
             return {"message": f"Livro com ID {livro_id} não encontrado"}, 404
         else:
             # Retorna o livro com suas informações
             return apresenta_livro(livro), 200
    
     except Exception as e:
         # Retorna uma mensagem de erro genérica para quaisquer exceções
         error_msg = f"Erro ao recuperar livro com ID {livro_id}"
         logger.warning(f"{error_msg}: {str(e)}")
         return {"message": error_msg}, 404
    


@app.get('/search_book', tags=[book_tag],
          responses={"200": ListagemBookInfoSchema, "404": ErrorSchema})
def busca_livro(query: BookInfoSearchByTitleSchema):
     """Faz a busca por livros em que o termo passado está presente no título do livro.

     Retorna uma representação dos livros encontrados.
     """
     termo = unquote(query.termo)
     logger.info(f"Fazendo a busca por título com o termo: {termo}")
     # Criando conexão com o banco de dados
     session = Session()
     # Realizando a busca
     livros = session.query(BookInfo).filter(BookInfo.title.ilike(f"%{termo}%")).all()

     if not livros:
         # Se não há livros cadastrados
         return {"livros": []}, 200
     else:
         logger.info(f"{len(livros)} livros encontrados")
         # Retorna a representação dos livros
         return apresenta_livros(livros), 200    
     
     

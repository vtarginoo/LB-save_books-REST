from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Define como uma mensagem de eero será representada
    """
    mesage: str

class ValidateErrorSchema(BaseModel):
    """ Define como uma mensagem de eero será representada
    """
    id: int = "null"
    idGoogle: str = "WFIsDwAAQBAJ"
    title: str = "null"
    status: str = "notFound"



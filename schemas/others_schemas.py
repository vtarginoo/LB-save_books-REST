from pydantic import BaseModel


class IndustryIdentifiersSchema(BaseModel):
    identifier: str = "9788543809823"
    type: str = "ISBN_13"

class ImageLinksSchema(BaseModel):
    smallThumbnail: str = "http://books.google.com/books/content?id=WFIsDwAAQBAJ&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api"
    thumbnail: str = "http://books.google.com/books/content?id=WFIsDwAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api"

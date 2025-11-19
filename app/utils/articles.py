import requests
from .errors import InvalidAuth, ArticleNotFound, InvalidArticleId

def getArticle(authKey:str, articleId: str):
    """
    Obtiene un artículo específico desde el servicio de artículos
    authKey: string El header Authorization enviado por el cliente
    articleId: string El ID del artículo a obtener
    """
    if (not isinstance(authKey, str) or len(authKey) == 0):
        raise InvalidAuth()

    headers = {"Authorization": authKey}

    url = f"http://localhost:3002/articles/{articleId}"
    response = requests.get(url, headers=headers)
    print("Article service response status:", response.status_code)
    if (response.status_code == 401):
        raise InvalidAuth()
    
    if (response.status_code == 404):
        raise ArticleNotFound()
    
    if(response.status_code == 400):
        raise InvalidArticleId()
    
    if(response.status_code != 200):
        raise Exception("Error fetching article")
    

    result = response.json()

    return result
import requests
import redis
import json
from .errors import InvalidAuth

r = redis.Redis(host='localhost', port=6379, db=1)
def normalizeAuthKey(authKey: str):
    if not isinstance(authKey, str):
        return None

    authKey = authKey.strip()

    if authKey.lower().startswith("bearer "):
        # Solo convierte el prefijo a minúscula
        token = authKey[7:]          # lo que viene después de "Bearer "
        return f"bearer {token}"     # prefijo en minúscula, token intacto

    return authKey

def isValidToken(authKey:str):
    """
    Obtiene el currentUser desde el servicio de autentificación
    authKey: string El header Authorization enviado por el cliente
    """
    if (not isinstance(authKey, str) or len(authKey) == 0):
        raise InvalidAuth()

    authKeyNormalized = normalizeAuthKey(authKey)
    cached = r.get(authKeyNormalized)
    #cached = None
    if cached:
        print("User fetched from cache")
        return json.loads(cached)

    headers = {"Authorization": authKeyNormalized}

    url = "http://localhost:3000/users/current"
    response = requests.get(url, headers=headers)

    if (response.status_code != 200):
        raise InvalidAuth()

    result = response.json()
    if (len(result) == 0):
        raise InvalidAuth()

    r.setex(authKeyNormalized, 300, json.dumps(result))  
    return result

def removeTokenFromCache(authKey:str):
    """
    Elimina el token del cache de redis
    authKey: string El header Authorization enviado por el cliente
    """
    authKeyNormalized = normalizeAuthKey(authKey)
    return r.delete(authKeyNormalized) > 0
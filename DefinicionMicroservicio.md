# Microservicio de Preguntas

## Casos de uso

### CU: Crear una pregunta

- Camino normal:
    - Cuando se intenta crear una pregunta se verifica que el id del articulo sea valido
    - Si el articulo es valido y se encuentra habilitado se crea
- Caminos Alternativos
    - Si el articulo no se encuentra o no se encuentra habilitado no se crea la pregunta

### CU: Modificar pregunta
- Camino normal:
    - Se verifica que el id del usuario conincida con el de la pregunta
    - Se verifica que la pregunto no este contestada
    - Se modifica la pregunta
- Camino Alternativo
    - Si no se cumple alguna de las verificaciones no se modifica la pregunta


### CU: Crear una respuesta

- Camino normal:
    - Se verificia que el id del usuario conincida con el del articulo
    - Se verifica la pregunta no este contestada
    - Se verifica que la pregunta este habilitada
    - Se crea la respuesta

- Camino alternativo
    - Si no se cumple alguna de las verificaciones no se crea la pregunta


## Modelo de datos

**Question**
- id
- text
- user_id
- article_id
- enable

**Answer**
- id
- text
- user_id
- question_id
- enable


## Interfaz REST

# Microservicio de Preguntas

## Casos de uso

### CU: Crear una pregunta

- Camino normal:
    - Cuando se intenta crear una pregunta se verifica que el id del artículo sea válido.
    - Si el artículo es válido y se encuentra habilitado, se crea.
- Caminos alternativos:
    - Si el artículo no se encuentra o no se encuentra habilitado, no se crea la pregunta.

### CU: Modificar pregunta
- Camino normal:
    - Se verifica que el id del usuario coincida con el de la pregunta.
    - Se verifica que la pregunta no esté contestada.
    - Se modifica la pregunta.
- Camino alternativo:
    - Si no se cumple alguna de las verificaciones, no se modifica la pregunta.


### CU: Crear una respuesta

- Camino normal:
    - Se verifica que el id del usuario coincida con el del artículo.
    - Se verifica que la pregunta no esté contestada.
    - Se verifica que la pregunta esté habilitada.
    - Se crea la respuesta.

- Camino alternativo:
    - Si no se cumple alguna de las verificaciones, no se crea la respuesta.


## Modelo de datos

**Question**
- id
- text
- user_id
- article_id
- enable

**Answer**
- id
- text
- user_id
- question_id
- enable


## Interfaz REST

### Crear una pregunta

`POST /questions`

**Params path**

*no tiene*

**Params query**

*no tiene*

**Body**

```json
{
    "text": "¿Cuál es el precio?",
    "article_id": "fefsefofe67"
}
```

**Headers**

- Authorization: bearer token

**Response**

`201 OK`

```json
{
    "id":  2,
    "text":  "¿Cuál es el precio?",
    "user_id":  "gfs6af8",
    "article_id":  "fefsefofe67",
    "enable":  true
}
```
`401 Invalid authorization`
Si el microservicio de catálogo devuelve un 401

`400 Invalid article ID`
Si el id del artículo es inválido

`404 Article not found`
Si no se encuentra el artículo

`400 Cannot add question to a disabled article`
Si el artículo se encuentra deshabilitado (enable=False)

### Obtener preguntas de un artículo

`GET /questions/{articleId}`

**Params path**

- articleId: artículo para la consulta

**Params query**

*no tiene*

**Body**

*no tiene*

**Headers**

- Authorization: bearer token

**Response**

`200 OK`

```json
[
    {
        "id":  2,
        "text":  "¿Cuál es el precio?",
        "user_id":  "gfs6af8",
        "article_id":  "fefsefofe67",
        "enable":  true
    }
]
```

### Modificar una pregunta

`PUT /questions/{articleId}`

**Params path**

- articleId: artículo para la consulta

**Params query**

*no tiene*

**Body**

```json
{
    "text": "¿Cuál es la altura?"
}
```

**Headers**

- Authorization: bearer token

**Response**

`200 OK`

```json
{
    "id":  2,
    "text":  "¿Cuál es el precio?",
    "user_id":  "gfs6af8",
    "article_id":  "fefsefofe67",
    "enable":  true
}
```

`404 Question not found`
Si no se encuentra la pregunta

`400 Cannot answer a disabled question`
Si la pregunta está deshabilitada (enable=false)

`400 Question has already been answered`
Si la pregunta ya tiene una respuesta asociada

`403 Not authorized to update this question`
Si el id del usuario no coincide con user_id de la pregunta

### Crear una respuesta

`POST /answers`

**Params path**

*no tiene*

**Params query**

*no tiene*

**Body**

```json
{
    "text": "$200000",
    "question_id": 2
}
```

**Headers**

- Authorization: bearer token

**Response**

`201 OK`

```json
{
    "id":  2,
    "text":  "¿Cuál es el precio?",
    "user_id":  "gfs6af8",
    "question_id":  2,
    "enable":  true
}
```

`401 Invalid authorization`
Si el microservicio de catálogo devuelve un 401

`400 Invalid article ID`
Si el id del artículo es inválido

`404 Article not found`
Si no se encuentra el artículo

`404 Question not found`
Si no se encuentra la pregunta

`400 Cannot answer a disabled question`
Si la pregunta está deshabilitada (enable=false)

`400 Question has already been answered`
Si la pregunta ya tiene una respuesta asociada

`403 Not authorized to answer this question`
Si el id del usuario no coincide con el user_id del artículo

## Interfaz asincrónica (rabbit)

### Eliminación de un artículo
Recibe el id del artículo que se eliminó para poder deshabilitar todas las preguntas asociadas a ese artículo

### Logout de un usuario
Recibe el token del usuario que hizo logout para eliminarlo de redis

### Enviar datos a stats
Cada vez que se crea una pregunta se envía al microservicio de stats lo siguiente:

```json
"message": {
                "questionId": 2,
                "userId": "fnewfs"
            }
```
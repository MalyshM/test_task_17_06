resp_201 = {
    "description": "Мем успешно добавлен",
    "content": {
        "application/json": {
            "example": {
                "id": 5,
                "name": "rabotaet.jpg",
                "link": "https://asdasdasd/rabotaet.jpg"
            }
        }
    }
}
resp_200_one = {
    "description": "Мем успешно добавлен",
    "content": {
        "application/json": {
            "example": {
                "id": 5,
                "name": "rabotaet.jpg",
                "link": "https://asdasdasd/rabotaet.jpg"
            }
        }
    }
}
resp_200_many = {
    "description": "Мем успешно добавлен",
    "content": {
        "application/json": {
            "example": [
                {
                    "id": 5,
                    "name": "rabotaet.jpg",
                    "link": "https://asdasdasd/rabotaet.jpg"
                },
                {
                    "id": 6,
                    "name": "lol.jpg",
                    "link": "https://asdasdasd/lol.jpg"
                }
            ]
        }
    }
}
resp_409 = {
    "description": "Мем уже существует",
    "content": {
        "application/json": {
            "example": {
                "detail": "Meme with that name already exists"
            }
        }
    }
}
resp_500 = {
    "description": "Внутренняя ошибка сервера",
    "content": {
        "application/json": {
            "example": {
                "detail": "internal server error"
            }
        }
    }
}
resp_404 = {
    "description": "нет мема по id",
    "content": {
        "application/json": {
            "example": {
                "detail": "Meme with that id not found"
            }
        }
    }
}

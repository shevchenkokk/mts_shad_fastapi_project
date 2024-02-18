import pytest
from fastapi import status
from sqlalchemy import select

from src.models import books, sellers


# Тест на ручку создающую продавца
@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {
        "first_name": "Andrey",
        "last_name": "Gavrilov",
        "email": "andr23_3s@mail.ru",
        "password": "gg5sdeoR321!"
    }
    response = await async_client.post("/api/v1/seller/", json=data)

    assert response.status_code == status.HTTP_201_CREATED

    result_data = response.json()

    assert result_data == {
        "id": result_data["id"],
        "first_name": "Andrey",
        "last_name": "Gavrilov",
        "email": "andr23_3s@mail.ru",
    }


# Тест на ручку получения списка продавцов
@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):
    # Создаем продавцов вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    seller = sellers.Seller(
        first_name="Egor",
        last_name="Sinyavin",
        email="egorikk5_4@yandex.ru",
        password="lwd2323%!cJ"
    )
    seller_2 = sellers.Seller(
        first_name="Ekaterina",
        last_name="Davydkova",
        email="k_a_t_k_e12@mail.ru",
        password="bgkUDM22#edm"
    )

    db_session.add_all([seller, seller_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/seller/")

    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()["sellers"]) == 2  # Опасный паттерн! Если в БД есть данные, то тест упадет

    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
        "sellers": [
            {
                "id": seller.id,
                "first_name": "Egor",
                "last_name": "Sinyavin",
                "email": "egorikk5_4@yandex.ru",
            },
            {
                "id": seller_2.id,
                "first_name": "Ekaterina",
                "last_name": "Davydkova",
                "email": "k_a_t_k_e12@mail.ru",
            },
        ]
    }


# Тест на ручку получения одного продавца
@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):
    # Создаем продавцов вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    seller = sellers.Seller(
        first_name="Egor",
        last_name="Sinyavin",
        email="egorikk5_4@yandex.ru",
        password="lwd2323%!cJ"
    )
    seller_2 = sellers.Seller(
        first_name="Ekaterina",
        last_name="Davydkova",
        email="k_a_t_k_e12@mail.ru",
        password="bgkUDM22#edm"
    )

    db_session.add_all([seller, seller_2])
    await db_session.flush()

    book = books.Book(
        author="Pushkin",
        title="Eugeny Onegin",
        year=2001,
        count_pages=104,
        seller_id=seller.id
    )

    db_session.add(book)
    await db_session.flush()

    response = await async_client.get(f"/api/v1/seller/{seller.id}")

    assert response.status_code == status.HTTP_200_OK

    # Проверяем интерфейс ответа, на который у нас есть контракт.
    assert response.json() == {
        "id": seller.id,
        "first_name": "Egor",
        "last_name": "Sinyavin",
        "email": "egorikk5_4@yandex.ru",
        "books": [
            {   "id": book.id,
                "author": "Pushkin",
                "title": "Eugeny Onegin",
                "year": 2001,
                "count_pages": 104,
                "seller_id": seller.id
            }
        ]
    }


# Тест на ручку удаления продавца
@pytest.mark.asyncio
async def test_delete_book(db_session, async_client):
    # Создаем продавца вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    seller = sellers.Seller(
        first_name="Egor",
        last_name="Sinyavin",
        email="egorikk5_4@yandex.ru",
        password="lwd2323%!cJ"
    )

    db_session.add(seller)
    await db_session.flush()

    response = await async_client.delete(f"/api/v1/seller/{seller.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()

    all_sellers = await db_session.execute(select(sellers.Seller))
    res = all_sellers.scalars().all()
    assert len(res) == 0


# Тест на ручку обновления данных о продавце
@pytest.mark.asyncio
async def test_update_book(db_session, async_client):
    # Создаем продавца вручную, а не через ручку, чтобы нам не попасться на ошибку которая
    # может случиться в POST ручке
    seller = sellers.Seller(
        first_name="Egor",
        last_name="Sinyavin",
        email="egorikk5_4@yandex.ru",
        password="lwd2323%!cJ"
    )

    db_session.add(seller)
    await db_session.flush()

    response = await async_client.put(
        f"/api/v1/seller/{seller.id}",
        json={
            "id": seller.id,
            "first_name": "Egor",
            "last_name": "Melnikov",
            "email": "egororrdew23@mail.ru",
            "password": "viOvd65409!"
        }
    )

    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()

    # Проверяем, что обновились все поля
    res = await db_session.get(sellers.Seller, seller.id)
    assert res.id == seller.id
    assert res.first_name == "Egor"
    assert res.last_name == "Melnikov"
    assert res.email == "egororrdew23@mail.ru"

import pytest
from httpx import Response

from src.api.searches.search_dto import SearchCreateDTO
from src.api.users.user_dto import UserDTO
from src.client.client import JobParserClient


@pytest.mark.searches
@pytest.mark.api
async def test_user_searches(user_client: JobParserClient, faker):
    resource_url = "https://www.olx.pl/praca/pracownik-sklepu/"
    user = UserDTO(**await user_client.users.get_me())

    search_dto = SearchCreateDTO(
        title=faker.texts(max_nb_chars=100),
        url=resource_url,
        owner_id=user.id
    )

    search_response: Response = await user_client.searches.create_search(search_dto, return_response=True)
    assert search_response.status_code == 201
    search_id = search_response.json()['id']

    dto_to_fail = search_dto.copy()
    dto_to_fail.title = None
    search_response: Response = await user_client.searches.create_search(dto_to_fail, return_response=True)
    assert search_response.status_code == 422

    dto_to_fail = search_dto.copy()
    dto_to_fail.url = None
    search_response: Response = await user_client.searches.create_search(dto_to_fail, return_response=True)
    assert search_response.status_code == 422

    dto_to_fail = search_dto.copy()
    dto_to_fail.url = "Not URL"
    search_response: Response = await user_client.searches.create_search(dto_to_fail, return_response=True)
    assert search_response.status_code == 422

    search_response: Response = await user_client.searches.get_search_by_id(search_id, return_response=True)
    assert search_response.status_code == 200
    assert search_response.json()['id'] == search_id
    assert search_response.json()['title'] == search_dto.title

    search_dto.title = faker.texts(max_nb_chars=100)
    search_response: Response = await user_client.searches.update_search(search_dto, search_id, return_response=True)
    assert search_response.status_code == 200
    assert search_response.json()['id'] == search_id
    assert search_response.json()['title'] == search_dto.title

    search_response: Response = await user_client.searches.get_searches(return_response=True)
    assert search_response.json()['items']
    assert search_response.json()['total']
    assert search_response.json()['size']

    search_response: Response = await user_client.searches.delete_search(search_id, return_response=True)
    assert search_response.status_code == 204

    search_response: Response = await user_client.searches.get_search_by_id(search_id, return_response=True)
    assert search_response.status_code == 404

    search_response: Response = await user_client.searches.get_searches(return_response=True, limit=5, page=1)
    assert search_response.status_code == 200
    assert search_response.json()['limit'] == 5
    assert search_response.json()['page'] == 1

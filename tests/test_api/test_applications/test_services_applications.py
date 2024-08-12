import pytest
from httpx import Response

from src.api.applications.application_dto import ApplicationCreateDTO
from src.api.users.user_dto import UserDTO
from src.client.client import JobParserClient


@pytest.mark.appllications
@pytest.mark.api
async def test_service_applications(user_client: JobParserClient, service_client: JobParserClient, faker):
    user: UserDTO = await user_client.users.get_me()

    application_dto = ApplicationCreateDTO(
        title=faker.text(max_nb_chars=100),
        description=faker.text(max_nb_chars=1000),
        application_link=faker.url(),
        url=faker.url(),
        owner_id=user.id
    )

    application_response: Response = await service_client.applications.service.create_application(
        application_dto,
        return_response=True
    )
    assert application_response.status_code == 201
    application_id = application_response.json()['id']

    dto_to_fail = application_dto.copy()
    dto_to_fail.title = None
    application_response: Response = await service_client.applications.service.create_application(
        dto_to_fail,
        return_response=True
    )
    assert application_response.status_code == 422

    dto_to_fail = application_dto.copy()
    dto_to_fail.description = None
    application_response: Response = await service_client.applications.service.create_application(
        dto_to_fail,
        return_response=True
    )
    assert application_response.status_code == 422

    dto_to_fail = application_dto.copy()
    dto_to_fail.application_link = None
    application_response: Response = await service_client.applications.service.create_application(
        dto_to_fail,
        return_response=True
    )
    assert application_response.status_code == 422

    dto_to_fail = application_dto.copy()
    dto_to_fail.url = None
    application_response: Response = await service_client.applications.service.create_application(
        dto_to_fail,
        return_response=True
    )
    assert application_response.status_code == 422

    dto_to_fail = application_dto.copy()
    dto_to_fail.url = "Not URL"
    application_response: Response = await service_client.applications.service.create_application(
        dto_to_fail,
        return_response=True
    )
    assert application_response.status_code == 422

    application1 = application_dto.copy()
    application1.title = faker.text(max_nb_chars=100)

    application2 = application_dto.copy()
    application2.title = faker.text(max_nb_chars=100)

    application3 = application_dto.copy()
    application3.title = faker.text(max_nb_chars=100)

    response = await user_client.applications.service.create_multiple_applications(
        data=[application1, application2, application3],
        return_response=True
    )
    assert response.status_code == 201

    await service_client.applications.service.get_application(application_id)
    assert application_response.status_code == 200
    assert application_response.json()['id'] == application_id
    assert application_response.json()['title'] == application_dto.title
    assert application_response.json()['owner_id'] == user.id

    application_dto.title = faker.texts(max_nb_chars=100)
    application_response: Response = await service_client.applications.service.update_application(
        application_id,
        application_dto,
        return_response=True
    )
    assert application_response.status_code == 200
    assert application_response.json()['id'] == application_id
    assert application_response.json()['title'] == application_dto.title
    assert application_response.json()['owner_id'] == user.id

    await service_client.applications.service.get_application(application_id)
    assert application_response.status_code == 200
    assert application_response.json()['id'] == application_id
    assert application_response.json()['title'] == application_dto.title
    assert application_response.json()['owner_id'] == user.id

    await service_client.applications.service.get_all_applications(return_response=True)
    assert application_response.status_code == 200
    assert application_response.json()['size']
    assert application_response.json()['total']
    assert application_response.json()['items']

    await service_client.applications.service.delete_application(application_id)
    assert application_response.status_code == 204

    await service_client.applications.service.delete_application(application_id)
    assert application_response.status_code == 404

    await service_client.applications.service.get_application(application_id)
    assert application_response.status_code == 404

    await service_client.applications.service.get_all_applications(return_response=True, limit=5, page=1)
    assert application_response.status_code == 200
    assert application_response.json()['size'] == 5
    assert application_response.json()['total']
    assert application_response.json()['items']

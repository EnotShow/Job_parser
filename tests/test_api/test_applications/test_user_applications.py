import pytest

from src.api.applications.application_dto import ApplicationDTO
from src.api.users.user_dto import UserDTO
from src.client.client import JobParserClient


@pytest.mark.applications
@pytest.mark.api
async def test_get_user_applications(user_client: JobParserClient, faker):
    user = await UserDTO(**await user_client.users.get_me())

    application_dto = ApplicationDTO(
        title=faker.text(max_nb_chars=100),
        description=faker.text(max_nb_chars=1000),
        application_link=faker.url(),
        url=faker.url(),
        owner_id=user.id
    )

    response = await user_client.applications.service.create_application(
        data=application_dto,
        return_response=True
    )
    assert response.status_code == 201

    response = await user_client.applications.get_all_applications(
        return_response=True
    )
    assert response.status_code == 200
    assert application_dto.title in response.json()

    response = await user_client.applications.get_applied_applications(
        user.id,
        return_response=True
    )
    assert response.status_code == 200
    assert application_dto.title not in response.json()

    application_id = response.json()[0]['id']

    response = await user_client.applications.get_application(
        application_id,
        return_response=True
    )
    assert response.status_code == 200
    assert application_dto.title in response.json()

    update_dto = application_dto.copy()
    update_dto.title = 'Updated title'

    response = await user_client.applications.update_application(
        data=update_dto,
        application_id=application_id,
        return_response=True
    )
    assert response.status_code == 204

    response = await user_client.applications.get_application(
        application_id,
        return_response=True
    )
    assert response.status_code == 200
    assert update_dto.title in response.json()

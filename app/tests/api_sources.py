from django.urls import reverse

from currency.models import Source


# GET /api/currency/sources/
def test_get_source_list(api_client_auth):
    initial_count = Source.objects.count()
    response = api_client_auth.get(reverse('currency_api:source-list'))
    assert response.status_code == 200
    assert len(response.json()) == initial_count


def test_get_source_by_id(api_client_auth):
    source = Source.objects.create(name='TestSource',
                                   source_url='https://testsource.com',
                                   code_name='testsource')
    response = api_client_auth.get(reverse('currency_api:source-detail', args=(source.id,)))
    assert response.status_code == 200
    assert response.json() == {
        'id': source.id,
        'name': 'TestSource',
        'code_name': 'testsource',
        'source_url': 'https://testsource.com',
    }


def test_get_source_by_id_404(api_client_auth):
    response = api_client_auth.get(reverse('currency_api:source-detail', args=(00,)))
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found."}


# POST /api/currency/sources/
def test_post_source_list_empty_body(api_client_auth):
    response = api_client_auth.post(reverse('currency_api:source-list'))
    assert response.status_code == 400
    assert response.json() == {
        "name": ["This field is required."],
        "source_url": ["This field is required."],
        "code_name": ["This field is required."]
    }


def test_post_source_list_valid_data(api_client_auth):
    initial_count = Source.objects.count()
    payload = {
        "name": "TestSource",
        "source_url": "https://testsource.com",
        "code_name": "testsource"
    }

    response = api_client_auth.post(reverse('currency_api:source-list'), data=payload)
    assert response.status_code == 201
    assert Source.objects.count() == initial_count + 1


def test_post_source_list_invalid_data_codename_already_exist_400(api_client_auth):
    Source.objects.create(name='TestSource',
                          source_url='https://testsource.com',
                          code_name='testsource')
    payload = {
        "name": "TestSource",
        "source_url": "https://testsource.com",
        "code_name": "testsource"
    }
    response = api_client_auth.post(reverse('currency_api:source-list'), data=payload)

    assert response.status_code == 400
    assert response.json() == {
        "code_name": ["Source with this Code name already exists."]
    }


def test_post_source_list_enter_valid_url_400(api_client_auth):
    payload = {
        "name": "TestSource",
        "source_url": "https://testsource",
        "code_name": "testsource"
    }
    response = api_client_auth.post(reverse('currency_api:source-list'), data=payload)

    assert response.status_code == 400
    assert response.json() == {
        "source_url": ["Enter a valid URL."]
    }


# PUT /api/currency/sources/<id>/

def test_put_source_list_200(api_client_auth):
    source = Source.objects.create(name='TestSource',
                                   source_url='https://testsource.com',
                                   code_name='testsource')

    payload = {
        "name": "TestSourceUpdated",
        "source_url": "https://testsource.com",
        "code_name": "testsource"
    }

    response = api_client_auth.put(reverse('currency_api:source-detail', args=(source.id,)), data=payload)
    assert response.status_code == 200
    assert response.json() == {
        "id": source.id,
        "name": "TestSourceUpdated",
        "source_url": "https://testsource.com",
        "code_name": "testsource"
    }

def test_put_source_list_404(api_client_auth):
    payload = {
        "name": "TestSourceUpdated",
        "source_url": "https://testsource.com",
        "code_name": "testsource"
    }

    response = api_client_auth.put(reverse('currency_api:source-detail', args=(00,)), data=payload)
    assert response.status_code == 404
    assert response.json() == {"detail":"Not found."}


# PATCH /api/currency/sources/<id>/

def test_patch_source_list_200(api_client_auth):
    source = Source.objects.create(name='TestSource',
                                   source_url='https://testsource.com',
                                   code_name='testsource')

    payload = {
        "name": "TestSourceUpdated",
    }

    response = api_client_auth.patch(reverse('currency_api:source-detail', args=(source.id,)), data=payload)
    assert response.status_code == 200
    assert response.json() == {
        "id": source.id,
        "name": "TestSourceUpdated",
        "source_url": "https://testsource.com",
        "code_name": "testsource"
    }


# DELETE /api/currency/sources/<id>/

def test_delete_source_list_204(api_client_auth):
    source = Source.objects.create(name='TestSource',
                                   source_url='https://testsource.com',
                                   code_name='testsource')

    response = api_client_auth.delete(reverse('currency_api:source-detail', args=(source.id,)))
    assert response.status_code == 204


def test_delete_source_list_404(api_client_auth):
    response = api_client_auth.delete(reverse('currency_api:source-detail', args=(00,)))
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found."}

from aiogram import types


def get_main_manu_lang(lang: str, part: str, message: types.Message):
    translate = {
        'ru': {
            'command_start': f'Здравствуйте, {message.from_user.full_name}, чем могу помочь вам сегодня!',
        },
        'pl': {
            'command_start': f'Czesc, {message.from_user.full_name}, co chcesz zrobic dzisiaj?',
        },
        'en': {
            'command_start': f'Hi, {message.from_user.full_name}, what can I help you with today?',
        },
    }
    return translate[lang][part]


def get_statistics_lang(lang: str, part: str):
    translate = {
        'ru': {
            'statistics': 'Найденно для тебя работ: 0!',
        },
        'pl': {
            'statistics': 'Dla Ciebie pracy: 0!',
        },
        'en': {
            'statistics': 'For you work: 0!',
        },
    }
    return translate[lang][part]


def get_searches_lang(lang: str, part: str):
    translate = {
        'ru': {
            'searches_manu': 'Что хочешь сделать?',
            'resource_url': 'Отправь ссылку на поисковой запрос для olx.pl или pracuj.pl',
            'resource_title': "Напиши название поискового запроса",
            'resource_created': 'Поисковый запрос успешно создан',
            'unsupported_resource': 'Данный ресурс не поддерживается! Попробуйте еще раз.',
        },
        'pl': {
            'searches_manu': 'Co chcesz zrobic?',
            'resource_url': 'Wpisz link do wyszukiwarki olx.pl lub pracuj.pl',
            'resource_title': 'Wpisz tytul wyszukiwarki',
            'resource_created': 'Wyszukiwarka została utworzona pomyslnie',
            'unsupported_resource': 'Dany zasob nie jest wspierany! Sproboj ponownie.',
        },
        'en': {
            'searches_manu': 'What do you want to do?',
            'resource_url': 'Enter the link to the search query for olx.pl or pracuj.pl',
            'resource_title': 'Enter the title of the search query',
            'resource_created': 'Search query created successfully',
            'unsupported_resource': 'This resource is not supported! Try again.',
        }
    }
    return translate[lang][part]

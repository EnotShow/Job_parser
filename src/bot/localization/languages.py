from aiogram import types


def get_main_manu_lang(lang: str, part: str, message: types.Message):
    translate = {
        'ru': {
            'command_start': f'Здравствуйте, {message.from_user.full_name}, чем могу помочь вам сегодня!',
            'unsupported_command': 'Команда не поддерживается',
            'settings_menu': 'Меню настроек:',
            'language_select': 'Выберите язык',
            'settings_changed': 'Настройки изменены!',
            'auth': 'Для авторизации перейдите по ссылке ниже:',
        },
        'pl': {
            'command_start': f'Czesc, {message.from_user.full_name}, co chcesz zrobic dzisiaj?',
            'unsupported_command': 'Ta komenda nie jest obsługiwana',
            'settings_menu': 'Menu ustawien:',
            'language_select': 'Wybierz jezyk',
            'settings_changed': 'Ustawienia zmienione!',
            'auth': 'Aby zalogowac, przejdz do linku:',
        },
        'en': {
            'command_start': f'Hi, {message.from_user.full_name}, what can I help you with today?',
            'unsupported_command': 'This command is not supported',
            'settings_menu': 'Settings menu:',
            'language_select': 'Select language',
            'settings_changed': 'Settings changed!',
            'auth': 'To log in, go to the link:',
        },
    }
    return translate[lang][part]


def get_statistics_lang(lang: str, part: str, count: int):
    translate = {
        'ru': {
            'statistics': f'Найденно для тебя работ: {count}!',
        },
        'pl': {
            'statistics': f'Znaleziono prace dla Ciebie: {count}!',
        },
        'en': {
            'statistics': f'Found jobs for you: {count}!',
        },
    }
    return translate[lang][part]


def get_referrals_lang(lang: str, part: str, ref_link: str, ref_count: int):
    translate = {
        'ru': {
            'referrals': f'Количество вашых рефералов: {ref_count}!\nВаша реферальная ссылка:\n{ref_link}',
        },
        'pl': {
            'referrals': f'Ilosc twoich referalow: {ref_count}!\nTwoja referalowa linka:\n{ref_link}',
        },
        'en': {
            'referrals': f'Number of your referrals: {ref_count}!\nYour referral link:\n{ref_link}',
        },
    }
    return translate[lang][part]


def get_searches_lang(lang: str, part: str):
    translate = {
        'ru': {
            'searches_manu': 'Что хочешь сделать?',
            'resource_url': 'Отправь ссылку на поисковой запрос для olx.pl или pracuj.pl',
            'resource_title': "Напиши название поискового запроса",
            'resource_new_link': "Отправь новую ссылку для пооискового запроса",
            'resource_updated': 'Запись обновленна!',
            'resource_created': 'Поисковый запрос успешно создан',
            'resource_deleted': 'Поисковый запрос успешно удален',
            'unsupported_resource': 'Данный ресурс не поддерживается! Попробуйте еще раз.',
            'no_resources': 'Вы пока не создали ни одного поискового запроса',
            'no_resource_found': 'Такого запроса не найденно!',
        },
        'pl': {
            'searches_manu': 'Co chcesz zrobic?',
            'resource_url': 'Wpisz link do wyszukiwarki olx.pl lub pracuj.pl',
            'resource_title': 'Wpisz tytul wyszukiwarki',
            'resource_new_link': 'Wpisz nowy link do wyszukiwarki',
            'resource_updated': 'Wyszukiwarka została zaktualizowana',
            'resource_created': 'Wyszukiwarka została utworzona pomyslnie',
            'resource_deleted': 'Wyszukiwarka została usunięta pomyslnie',
            'unsupported_resource': 'Dany zasob nie jest wspierany! Sproboj ponownie.',
            'no_resources': 'Nie utworzyles jeszcze zadnego wyszukiwarki',
            'no_resources_found': 'Nie znaleziono takiego zapytania!',
        },
        'en': {
            'searches_manu': 'What do you want to do?',
            'resource_url': 'Enter the link to the search query for olx.pl or pracuj.pl',
            'resource_title': 'Enter the title of the search query',
            'resource_new_link': 'Enter the new link for the search query',
            'resource_updated': 'Search query updated successfully',
            'resource_created': 'Search query created successfully',
            'resource_deleted': 'Search query deleted successfully',
            'unsupported_resource': 'This resource is not supported! Try again.',
            'no_resources': 'You have not created any search queries yet',
            'no_resources_found': 'No such query found!',
        }
    }
    return translate[lang][part]

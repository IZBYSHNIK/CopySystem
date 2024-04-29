import os, requests, json, sys

VERSION = '0.0.4'
URL = 'https://cloud-api.yandex.net/v1/disk/resources'
TOKEN = ''

CONFIG_DEFAULT = {
    'URL': URL,
    'TOKEN': TOKEN,
    'ORIGINAL_LOCATION': '',
    'NEW_LOCATION': '',
    #'CONNECT_FOLDERS': {'TEST1': {'ORIGINAL_LOCATION': 'home/user'}, 'TEST2': {'ORIGINAL_LOCATION': 'c://ddd/qww'}}
    'CONNECT_FOLDERS': {}
}
CONFIG = {}
EXIT_SIGNALS = ('Q', 'EXIT')
dirname, filename = os.path.split(os.path.abspath(__file__))


def save_config():
    global CONFIG, CONFIG_DEFAULT
    if not CONFIG:
        with open('config.json', 'w', encoding='UTF-8') as f:
            json.dump(CONFIG_DEFAULT, f,)
        CONFIG = CONFIG_DEFAULT.copy()
    else:
        with open('config.json', 'w', encoding='UTF-8') as f:
            json.dump(CONFIG, f)

def load_config():
    global CONFIG
    with open('config.json', 'r', encoding='UTF-8') as f:
        CONFIG = json.load(f)
        



if not os.path.isfile(os.path.join(dirname, 'config.json')):
    save_config()
else:
    load_config()

headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {CONFIG["TOKEN"]}'}

def create_folder(path):
    """Создание папки. \n path: Путь к создаваемой папке."""
    print(requests.put(f'{URL}?path={path}', headers=headers))


def upload_file(loadfile, savefile, replace=False):
    """Загрузка файла.
    savefile: Путь к файлу на Диске
    loadfile: Путь к загружаемому файлу
    replace: true or false Замена файла на Диске"""
    res = requests.get(f'{URL}/upload?path={savefile}&overwrite={replace}', headers=headers).json()
    with open(loadfile, 'rb') as f:
        try:
            requests.put(res['href'], files={'file':f})
        except KeyError:
            print(res)


def download_file(savefile, loadfile):
    """Скачивание файла.
    savefile: Путь к файлу на Диске
    loadfile: Путь к загружаемому файлу
    """
    res = requests.get(f'{URL}/download?path={savefile}', headers=headers).json()
    with open(loadfile, 'wb') as f:
        try:
            requests.put(res['href'], files={'file':f})
        except KeyError:
            print(res)


HOME_DIR = 'CopySystem'

create_folder(HOME_DIR)

NAME_WORK_DIR = ''

def get_status_message(fun):
    try:
        fun()
    except:
        print('При выполнении операции произошла ошибка')
    else:
        print('Операция успешно выполнена')


def get_request_for_changes(message=None):
    if message:
        print(message)
    answer = input('Вы точно хотите продолжить? (Y/n)(Д/н)')
    if answer == 'Y' or answer == 'Д':
        return 1
    return 0


def add_folder():
    global NAME_WORK_DIR
    while True:
        name_folder = input('Придумайте имя для хранилища в облаке: ').strip() 
        if name_folder.upper() in EXIT_SIGNALS:
            return
        if not name_folder.isidentifier():
            print(f'*Указано недопустимое название: {name_folder}')
            continue
        break
    while True:
        if name_folder.upper()in EXIT_SIGNALS:
            return
        path_folder = input('Локальный путь до папки: ').strip() 
        if not os.path.isdir(path_folder):
            print(f'Указан недопустимый путь: {path_folder}')
            continue
        break
    
    if get_request_for_changes(message=f'Будет добавлено новое хранилище для работы с названием {name_folder}, по пути {path_folder}'):
        CONFIG['CONNECT_FOLDERS'] |= {name_folder: {'ORIGINAL_LOCATION': path_folder}}
        NAME_WORK_DIR = name_folder
        try:
            save_config()
        except BaseException:
            print('Не удалось выполнить команду сохранения изменений')
        else:
            print('Изменения успешно применены')


def active_folder():
    global NAME_WORK_DIR
    print('Доступные хранилица')
    show_available_folders()
    name_folder = input('Выберите название хранилища и введите его: ').strip()
    for folder in CONFIG['CONNECT_FOLDERS']:
        if folder == name_folder:
            NAME_WORK_DIR = folder
            break
    else:
        print('Указаного хранилища нет')
               

def show_available_folders(get_total=False, marker=' - '):
    list_folder = [marker+i+'\n' for i in CONFIG['CONNECT_FOLDERS']]
    print(*list_folder, sep='')
    if get_total:
        print(f'Всего хранилищ - {len(list_folder)}')


def save():
    if NAME_WORK_DIR:
        # print(NAME_WORK_DIR)
        # print(CONFIG['CONNECT_FOLDERS'][NAME_WORK_DIR]['ORIGINAL_LOCATION'])
        dirs = list(os.walk(top=CONFIG['CONNECT_FOLDERS'][NAME_WORK_DIR]['ORIGINAL_LOCATION']))
        root_dir = os.path.join(HOME_DIR, NAME_WORK_DIR)
        # create_folder(os.path.join(HOME_DIR, NAME_WORK_DIR))
        for d in range(len(dirs)):
            path_ = dirs[d][0].replace(dirs[0][0], '')
            if not path_:
                path_ = os.sep
            
            print(root_dir + path_)
            if path_:
                # print(os.path.join(HOME_DIR, path_))
                create_folder(root_dir + path_)
                for f in dirs[d][2]:
                    print(f'COPY: {f} | {os.path.join(dirs[d][0], f)} -> {os.path.join(root_dir + path_, f)}')
                    upload_file(os.path.join(dirs[d][0], f), os.path.join(root_dir + path_, f), replace=True)
    else:
        print('Для выполнения этой команды выберите активное хранилище с помощью команды: 2 или CHOOSE_FOLDER')

def scan_folder(root_dir, result=None):
    if not result:
        result = {}
    res = requests.get(f'{URL}?path={root_dir}', headers=headers).json()
    f = []
    for i in res['_embedded']['items']:
        if i['type'] == 'dir':
            print('DIR', i['name'])
            result = scan_folder(os.path.join(root_dir, i['name']), result=result)
        if i['type'] == 'file':
            f.append((i['name'], i['file']))
            print('FILE', i['name'])
    result[root_dir] = f
    return result

def load():
    if NAME_WORK_DIR:
        root_dir = os.path.join(HOME_DIR, NAME_WORK_DIR)
        print('Сканирование хранилища ...')
        dirs = scan_folder(root_dir)
        print('Сканирование завершено')
        print(f'Обноружено {str(len(dirs))} папок и {sum([len(dirs[i]) for i in dirs])} файов')
        if get_request_for_changes():
            print(f"Файлы и папки будут сохранены по пути {CONFIG['CONNECT_FOLDERS'][NAME_WORK_DIR]['ORIGINAL_LOCATION']}")
            print('Создание папок ...')
            for i in sorted(dirs, key=lambda x: len(x.split(os.sep))):
                if not os.path.isdir(CONFIG['CONNECT_FOLDERS'][NAME_WORK_DIR]['ORIGINAL_LOCATION'] + i.replace(root_dir, '')) and i.replace(root_dir, ''):
                    print(f"CREATE FOLDER {i.replace(root_dir, '')}")
                    os.mkdir(CONFIG['CONNECT_FOLDERS'][NAME_WORK_DIR]['ORIGINAL_LOCATION'] + i.replace(root_dir, ''))
            
            print('Скачивание файлов ...')
            for i in dirs:
                for file in dirs[i]:
                    print("DOWNLOAD", file[0])
                    with open(CONFIG['CONNECT_FOLDERS'][NAME_WORK_DIR]['ORIGINAL_LOCATION'] + os.sep + i.replace(root_dir, '') + os.sep + file[0], 'wb') as f: 
                        requests.get(file[1])       
        else:
            return
        print('Скачивание успешно завершено')
    else:
        print('Для выполнения этой команды выберите активное хранилище с помощью команды: 2 или CHOOSE_FOLDER')
    

COMMANDS = {
    "COMIT_FOLDER": {'NAME': 'Подключить хранилище', 'COMMAND': add_folder},
    "SHOW_FOLDERS": {'NAME': 'Показать доступные хранилища данных', 'COMMAND': lambda : show_available_folders(get_total=True)},
    "CHOOSE_FOLDER": {'NAME': 'Выбрать рабочее хранилище', 'COMMAND': active_folder},

    "SAVE": {'NAME': 'Сохранить в облако', 'COMMAND': save},
    "DOWNLOAD": {'NAME': 'Загрузить из облака', 'COMMAND': load},

}


SYS_COMMANDS = {
    "SHOW": lambda : ['Сприсок доступных команд\n'] + [f'{i}, {c} - {COMMANDS[c]["NAME"]}\n' for i, c in zip(range(len(COMMANDS)), COMMANDS.keys()) ]
}
_dir = NAME_WORK_DIR
prefix = f'{f"$({_dir}) " if _dir else ""}> '

def init():
    print(f'Добро пожаловать в CopySystem {VERSION}!')
        
    if not CONFIG['TOKEN']:
        print('Для работы программы нужно ввести токен на доступ к вашему сетевому хранилищу')
        while True:
            value = input(' > ').strip()
            if value.upper() in EXIT_SIGNALS:
                sys.exit()
            CONFIG['TOKEN'] = value
            headers['Authorization'] = f'OAuth {CONFIG["TOKEN"]}'
            create_folder(HOME_DIR)
            save_config()
            break
       

    print('---Для вывода доступных команд введите show---')
    while True:
        _dir = NAME_WORK_DIR
        prefix = f'{f"$({_dir}) " if _dir else ""}> '

        command = input(f'{prefix} ').strip().upper()
        if command:
            if command.strip() in EXIT_SIGNALS:
                print('Завершение программы ...\nДо новых встреч!')
                break
            
            if command in SYS_COMMANDS:
                print(*SYS_COMMANDS[command](), sep='')
            elif command in COMMANDS or command.isnumeric():
                if command.isnumeric():
                    if 0 <= int(command) < len(list(COMMANDS.keys())):
                        COMMANDS[list(COMMANDS.keys())[int(command)]]['COMMAND']()
                    else:
                        print('Команда не найдена')
                else:
                    COMMANDS[command]['COMMAND']()
                
            else:
                print('Команда не найдена')


if __name__ == '__main__':
    init()

input()

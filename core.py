import json, requests, os

class CopyManager:
    NETWORK_URLs = ('https://cloud-api.yandex.net/v1/disk/resources', )
    HOME_DIR = 'CopySystem'
    TYPE_CONNECT = ('NETWORK', 'BETWEEN', 'LOCATION')
    WORK_DIR = ''
    CONFIG_DEFAULT = {'CONNECT_FOLDERS': {}}

    def __init__(self) -> None:
        dirname, filename = os.path.split(os.path.abspath(__file__))
        if not os.path.isfile(os.path.join(dirname, 'config.json')):
            self.save_config()
        else:
            self.load_config()

        # self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {CONFIG["TOKEN"]}'}


    def save_config(self):
        if not ( hasattr(self, 'CONFIG') and self.CONFIG):
            with open('config.json', 'w', encoding='UTF-8') as f:
                json.dump(self.CONFIG_DEFAULT, f,)
            self.CONFIG = self.CONFIG_DEFAULT.copy()
        else:
            with open('config.json', 'w', encoding='UTF-8') as f:
                json.dump(self.CONFIG, f)

    def load_config(self):
        with open('config.json', 'r', encoding='UTF-8') as f:
            self.CONFIG = json.load(f)

    @classmethod
    def is_valid_name(cls, name):
        return isinstance(name, str) and name.isidentifier()
    
    @classmethod
    def is_valid_type(cls, type_):
        return type_ in cls.TYPE_CONNECT
    

    def fix_folder(self, name, original_location, type, mode, parametrs):
        if self.is_valid_name(name) and self.is_valid_type(type):
            self.CONFIG['CONNECT_FOLDERS'][name] = {"ORIGINAL_LOCATION":original_location, "TYPE":type, "MODE":mode, 'PARAMETRS': parametrs}
        else:
            raise ValueError('Incorrect folder name or type')


    def activate_folder(self, name):
        if not (name in self.CONFIG['CONNECT_FOLDERS']):
            raise ValueError("Couldn't find a folder with that name")
        self.WORK_DIR = name

    
    def generate_head(self):
        if not self.WORK_DIR:
            raise ValueError("There are no active folder")
        if self.CONFIG['CONNECT_FOLDERS'][self.WORK_DIR]['TYPE'] != 'NETWORK':
            raise ValueError("This folder has no network type")

        return {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f"OAuth {self.CONFIG['CONNECT_FOLDERS'][self.WORK_DIR]['PARAMETRS']['TOKEN']}"}

    def create_folder_network(self, path):
        """Создание папки. \n path: Путь к создаваемой папке."""
        requests.put(f"{self.NETWORK_URLs[0]}?path={path}", headers=self.generate_head())


    def upload_file_network(self, loadfile, savefile, replace=False):
        """Загрузка файла.
        savefile: Путь к файлу на Диске
        loadfile: Путь к загружаемому файлу
        replace: true or false Замена файла на Диске"""
     
        res = requests.get(f"{self.CONFIG['CONNECT_FOLDERS'][self.WORK_DIR]['PARAMETRS']['URL']}/upload?path={savefile}&overwrite={replace}", headers=self.generate_head()).json()
        with open(loadfile, 'rb') as f:
            try:
                requests.put(res['href'], files={'file':f})
            except KeyError:
                print(res)


    def download_file_network(self, savefile, loadfile):
        """Скачивание файла.
        savefile: Путь к файлу на Диске
        loadfile: Путь к загружаемому файлу
        """
        res = requests.get(f"{self.CONFIG['CONNECT_FOLDERS'][self.WORK_DIR]['PARAMETRS']['URL']}/download?path={savefile}", headers=self.generate_head()).json()
        with open(loadfile, 'wb') as f:
            try:
                requests.put(res['href'], files={'file':f})
            except KeyError:
                print(res)

    def scan_folder_network(self, root_dir, result=None):
        if not result:
            result = {}
        res = requests.get(f"{self.CONFIG['CONNECT_FOLDERS'][self.WORK_DIR]['PARAMETRS']['URL']}?path={root_dir}", headers=self.generate_head()).json()
        f = []
        for i in res['_embedded']['items']:
            if i['type'] == 'dir':
                result = self.scan_folder(os.path.join(root_dir, i['name']), result=result)
            if i['type'] == 'file':
                f.append((i['name'], i['file']))
        result[root_dir] = f
        return result

    def download_files_network(self, dirs):
        root_dir = os.path.join(self.HOME_DIR, self.WORK_DIR)
     
        dirs = self.scan_folder_network(root_dir)
        
        for i in sorted(dirs, key=lambda x: len(x.split(os.sep))):
            if not os.path.isdir(self.CONFIG['CONNECT_FOLDERS'][self.WORK_DIR]['ORIGINAL_LOCATION'] + i.replace(root_dir, '')) and i.replace(root_dir, ''):
                print(f"CREATE FOLDER {i.replace(root_dir, '')}")
                os.mkdir(self.CONFIG['CONNECT_FOLDERS'][self.WORK_DIR]['ORIGINAL_LOCATION'] + i.replace(root_dir, ''))
        
        for i in dirs:
            for file in dirs[i]:
                print("DOWNLOAD", file[0])
                with open(self.CONFIG['CONNECT_FOLDERS'][self.WORK_DIR]['ORIGINAL_LOCATION'] + os.sep + i.replace(root_dir, '') + os.sep + file[0], 'wb') as f: 
                    requests.get(file[1])       
   
       
        





if __name__ == '__main__': 
    print(CopyManager().CONFIG)


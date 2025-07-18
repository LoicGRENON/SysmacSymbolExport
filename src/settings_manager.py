import configparser
import logging
import shutil
from platformdirs import user_config_dir
from pathlib import Path

from src import APP_NAME


logger = logging.getLogger(__name__)


class SettingsManager:
    def __init__(self, config_filename: str = "config.ini"):
        self.config_dir = Path(user_config_dir(APP_NAME))
        self.config_file = self.config_dir / config_filename
        logger.info(f"Config file: {self.config_file}")
        self.config = configparser.ConfigParser()

        self._load_or_create()

    def _load_or_create(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)

        if self.config_file.exists():
            self.config.read(self.config_file)
        else:
            self.restore_default()

    def restore_default(self):
        self.config['general'] = {
            'solution_path': 'C:\\OMRON\\Data\\Solution'
        }
        self.save()

    def export_to(self, filename):
        shutil.copyfile(self.config_file, filename)

    def import_from(self, filename):
        shutil.copyfile(filename, self.config_file)
        self.__init__()

    def get(self, section: str, key: str, fallback=None):
        return self.config.get(section, key, fallback=fallback)

    def set(self, section: str, key: str, value: str):
        if section not in self.config:
            self.config.add_section(section)
        self.config[section][key] = value

    def save(self):
        with self.config_file.open('w') as f:
            self.config.write(f)

    def as_dict(self):
        return {section: dict(self.config[section]) for section in self.config.sections()}

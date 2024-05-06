from configparser import ConfigParser
import os.path


def config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()

    path_to_file = os.path.join("..", filename)

    parser.read(path_to_file)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db


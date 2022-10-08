"""
This script handles the saving of variables to reuse them.
"""

import os
import json


class SaveSystem:

    # file path structure
    SAVE_FOLDER = './saves/'
    SAVE_FILE_SETTINGS = os.path.join(SAVE_FOLDER, 'settings.json')


    def __init__(self):
        # make sure files exist
        self.check_files_exists()


    def check_files_exists(self):
        """Check if files exist"""

        # if save folder does not exist create one
        if not os.path.exists(self.SAVE_FOLDER):
            os.makedirs(self.SAVE_FOLDER)
            print('created folder: {0}'.format(self.SAVE_FOLDER))

        # if save file does not exist create one
        if not os.path.exists(self.SAVE_FILE_SETTINGS):
            with open(self.SAVE_FILE_SETTINGS, 'w') as f:
                f.write('{}')
                f.close()
            print('created file: {0}'.format(self.SAVE_FILE_SETTINGS))

    @staticmethod
    def save_variable(file_path: str, variable_key: str, variable_value):
        """
        Save a variable

        :param file_path: path to save file
        :param variable_key: key of the variable
        :param variable_value: value of the variable
        :return
        """

        try:
            # read file and save content in data variable
            f = open(file_path, 'r', errors='replace')
            data = json.load(f)
            f.close()

            # print(f"read data from file '{file_path}': {data}")

        except Exception as save_read_err:
            print('ERROR: SAVE FILE READ ERROR:', save_read_err)
            return

        try:
            # save or overwrite save variable
            data[variable_key] = variable_value

            # save to file
            f = open(file_path, 'w', errors='replace')
            json.dump(data, f, indent=4)
            f.close()

        except Exception as save_write_err:
            print('ERROR: SAVE FILE WRITE ERROR:', save_write_err)
            return

    @staticmethod
    def load_variable(file_path: str, variable_key: str):
        """
        Load a variable from save file.
        If variable_key is not in save_file, return None.
        """

        try:
            # read file and save content in data variable
            f = open(file_path, 'r', errors='replace')
            data = json.load(f)
            f.close()

            # print(f"read data from file '{file_path}': {data}")

        except Exception as save_read_err:
            print('ERROR: SAVE FILE READ ERROR:', save_read_err)
            return None

        if variable_key in data:
            return data[variable_key]
        else:
            return None


# SaveSystem().save_variable(SAVE_FILE_SETTINGS, 'dark_mode', True)
# print(SaveSystem().load_variable(SAVE_FILE_SETTINGS, 'dark_mode'))

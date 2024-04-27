import os

from xml_file import SettingsXmlFile, InputXmlFile


class App:
    def __init__(self):
        self.settings_file, self.input_file_list = self.read_input_data2()
        self.run_sorting()

    @staticmethod
    def read_input_data():
        # text_file = 'input_data.txt'
        text_file = input('Enter file name: ')
        with open(text_file, "r") as input_data:
            settings_file = SettingsXmlFile(input_data.readline()[:-1])
            input_files_list = list(map(lambda name: InputXmlFile(name), input_data.readline().split(', ')))

        return settings_file, input_files_list

    @staticmethod
    def read_input_data2():
        directory = input('Enter directory name: ')
        files = os.listdir(directory)
        settings_file = None
        input_files_list = []
        for file in files:
            file = directory + '/' + file
            if 'settings.xml' in file:
                settings_file = SettingsXmlFile(file)
            else:
                input_files_list.append(InputXmlFile(file))

        return settings_file, input_files_list

    def run_sorting(self):
        for input_file in self.input_file_list:
            self.settings_file.sort(input_file.get_file_name())


if __name__ == '__main__':
    app = App()

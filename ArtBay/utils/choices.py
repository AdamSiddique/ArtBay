import os
import pandas as pd

absolute_path = os.path.dirname(__file__)
relative_path = '../../dataset/archive/artworks.csv'
DATASET_PATH = os.path.join(absolute_path, relative_path)

def get_label_name(string):
    return string.replace("_", " ").capitalize()


class ModelChoices:
    def __init__(self, choices_list):
        for item in choices_list:
            setattr(self, item.lower(), get_label_name(item))

    def choices(self):
        return [(k, v) for k, v in self.__dict__.items()]

    def values(self):
        return [v for v in self.__dict__.keys()]

    def labels(self):
        return [l for l in self.__dict__.values()]

ArtMediumChoices = ModelChoices(['painting', 'sculpture'])

df = pd.read_csv(DATASET_PATH, sep=',', on_bad_lines='skip')

if __name__ == '__main__':
    print(ArtItemChoices.choices())

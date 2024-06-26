import nltk


def download_nltk_data_packages():
    """
    This function installs all required NLTK packages.
    """
    nltk_data_packages = [
        'punkt',
        'averaged_perceptron_tagger',
        'maxent_ne_chunker',
        'words'
    ]

    for package in nltk_data_packages:
        nltk.download(package)
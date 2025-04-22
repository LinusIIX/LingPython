# wordlists.py
# Author: Philipp Gelfuss
# if you want to see more detailed information about the individual contributors of the code files, 
# please have a look at the "contributors.txt" file (in the "project" directory)

from utils.path_utils import PathUtils
from pathlib import Path
import random


class WordLists:
    """Manages word lists by either loading words from files or using a fallback set."""

    # Used to get the correct file path independent of the current working directory.
    _pu = PathUtils()

    # Initial files to load that I placed in src/wordlists.
    # Those files were downloaded from https://wortschatz.uni-leipzig.de/en/download/
    # and then manually processed by me.
    # Also defines the language to which those words belong.
    _lists = {
        # "arabic": "ara.txt", # not present in default font
        "danish": "dan.txt",
        "german": "deu.txt",
        # "greek": "ell.txt", # not present in default font
        "english": "eng.txt",
        "french": "fra.txt",
        # "hindi": "hin.txt", # not present in default font
        "italian": "ita.txt",
        # "japanese": "jpn.txt", # not present in default font
        # "korean": "kor.txt", # not present in default font
        "norwegian": "nor.txt",
        # "polish": "pol.txt",  # some letters are missing from the default font
        "russian": "rus.txt",
        "spanish": "spa.txt",
        "swedish": "swe.txt",
        # "turkish": "tur.txt",  # some letters are missing from the default font
        # "chinese": "zho.txt", # not present in default font
    }

    # The list of languages accessible from the outside.
    LANGUAGES = list(_lists.keys())

    # The list of words gets loaded once and is then constant.
    # Also accessible from the outside.
    # The key is a word, the value is the list of languages in which the wort appears.
    WORDS: dict[str, list[str]] = {}

    # The amount of languages loaded, only used for debug logs.
    _loaded_langs = 0

    def __init__(self, debug_mode=False):
        self._debug_mode = debug_mode

        # Grab each language and the associated word file path.
        for lang, path in self._lists.items():
            # Add the folder name to the file name and get the correct path.
            path = self._pu.get_resource_path(Path("wordlists") / path)

            try:
                # Open the word file for reading.
                with open(path, "r") as f:
                    for word in f:
                        # Remove the trailing newline and other whitespace.
                        word = word.strip()

                        if word in self.WORDS:
                            # Word has been loaded from another language already,
                            # just add the current language to its valid options.
                            if lang not in self.WORDS[word]:
                                self.WORDS[word].append(lang)
                        else:
                            # Add the new word to the dataset.
                            self.WORDS[word] = [lang]

                self._loaded_langs += 1

            except Exception as e:
                # Opening one language file failed.
                # Log the error and continue with the next.
                self._log("WARNING", f'Can\'t load word file for "{lang}": {e}')

        self._log("INFO", f"Loaded {self._loaded_langs} language files.")

        # Use the fallback dataset defined at the bottom if not enough languages were loaded from files.
        if self._loaded_langs < 5:
            self._log("ERROR", "Loaded less than 5 languages, using fallback instead.")
            self.WORDS = self._fallback

    def load_list(self, language: str, path: Path) -> bool:
        """
        Tries to add a new wordlist from a file to the dataset.
        Returns True if the list was loaded successfully.
        """

        # Get the correct path for the new file.
        path = self._pu.get_resource_path(path, "r")

        # Add the language to the list if it doesn't exist already.
        if language not in self.LANGUAGES:
            self.LANGUAGES.append(language)

        try:
            # Open the file in read mode.
            with open(path) as f:
                for word in f:
                    # Remove the trailing newline and other whitespace.
                    word = word.strip()

                    if word in self.WORDS:
                        # Word has been loaded from another language already,
                        # just add the current language to its valid options.
                        if language not in self.WORDS[word]:
                            self.WORDS[word].append(language)
                    else:
                        # Add the new word to the dataset.
                        self.WORDS[word] = [language]

            # Return success.
            return True

        except Exception as e:
            # Opening one language file failed.
            # Log the error and return failure.
            self._log(
                "ERROR", f'Can\'t load additional word file for "{language}": {e}'
            )
            return False

    def get_word(self, exclude: list[str] = []) -> tuple[str, list[str]]:
        """
        Randomly selects a word from the loaded dataset that is not present in the "exclude" list.
        The "exclude" list could e.g. be the list of already used words to prevent duplicates.
        """

        # Choose a random word from the dataset.
        word = random.choice(list(self.WORDS.keys()))

        while word in exclude:
            # Select a new word if the previous selection appears in the exclude list.
            word = random.choice(list(self.WORDS.keys()))

        self._log("INFO", f"Selected word: {word} with languages {self.WORDS[word]}")

        # Return a tuple of the word and the list of associated languages.
        return (word, self.WORDS[word])

    def get_language(self, languages: list[str] = []) -> str:
        """
        Randomly selects a language from the dataset that is not present in the list.
        The "languages" list could e.g. be the languages of the current word to prevent unwanted additional correct answers.
        """

        # Choose a random language from the dataset.
        lang = random.choice(self.LANGUAGES)

        while lang in languages:
            # Select a new language if the previous selection appears in the exclude list.
            lang = random.choice(self.LANGUAGES)

        self._log("INFO", f"Selected language: {lang}")

        # Return the language string.
        return lang

    def _log(self, level, message):
        """Prints a log message in debug mode."""
        if self._debug_mode:
            print(f"[WORDS][{level}] {message}")

    # Fallback list that is used when less than 5 languages were loaded from files.
    _fallback = {
        "sich": ["german"],
        "es": ["german", "spanish"],
        "dem": ["german"],
        "nicht": ["german"],
        "im": ["german"],
        "wurde": ["german"],
        "war": ["german", "english"],
        "an": ["german", "english"],
        "zu": ["german"],
        "auch": ["german"],
        "aus": ["german"],
        "hat": ["german", "english"],
        "einen": ["german"],
        "ein": ["german"],
        "einer": ["german"],
        "um": ["german", "english"],
        "noch": ["german"],
        "sie": ["german"],
        "eine": ["german"],
        "mittelfristig": ["german"],
        "mitten": ["german", "english"],
        "mobilen": ["german"],
        "morgens": ["german"],
        "musikalische": ["german"],
        "musikalischen": ["german"],
        "mußt": ["german"],
        "mühsam": ["german"],
        "müßte": ["german"],
        "nachgebildet": ["german"],
        "nachträglich": ["german"],
        "nachvollziehbar": ["german"],
        "namens": ["german"],
        "natürlich": ["german"],
        "ne": ["german"],
        "nett": ["german"],
        "neuerliche": ["german"],
        "neueste": ["german"],
        "ordentliche": ["german"],
        "ostdeutschen": ["german"],
        "paar": ["german"],
        "passende": ["german"],
        "passt": ["german"],
        "permanent": ["german", "english"],
        "persönlich": ["german"],
        "persönlicher": ["german"],
        "planen": ["german"],
        "platzte": ["german"],
        "pleite": ["german"],
        "plötzlich": ["german"],
        "polnische": ["german"],
        "positive": ["german", "english"],
        "potenzielle": ["german"],
        "pro": ["german", "english"],
        "produziert": ["german"],
        "último": ["spanish"],
        "con": ["spanish", "english"],
        "bien": ["spanish"],
        "habían": ["spanish"],
        "hecho": ["spanish"],
        "tipo": ["spanish"],
        "caso": ["spanish"],
        "nivel": ["spanish"],
        "población": ["spanish"],
        "segundo": ["spanish"],
        "hijo": ["spanish"],
        "otra": ["spanish"],
        "varias": ["spanish"],
        "centro": ["spanish"],
        "enero": ["spanish"],
        "eran": ["spanish"],
        "hizo": ["spanish"],
        "un": ["spanish"],
        "menos": ["spanish"],
        "siguiente": ["spanish"],
        "película": ["spanish"],
        "medio": ["spanish"],
        "grandes": ["spanish"],
        "guerra": ["spanish"],
        "importante": ["spanish"],
        "principal": ["spanish", "english"],
        "veces": ["spanish"],
        "comenzó": ["spanish"],
        "esto": ["spanish"],
        "haber": ["spanish"],
        "sino": ["spanish"],
        "cuerpo": ["spanish"],
        "llamado": ["spanish"],
        "porque": ["spanish"],
        "punto": ["spanish"],
        "pesar": ["spanish"],
        "total": ["spanish", "english", "german"],
        "época": ["spanish"],
        "edad": ["spanish"],
        "partir": ["spanish"],
        "temporada": ["spanish"],
        "hombres": ["spanish"],
        "tarde": ["spanish"],
        "manera": ["spanish"],
        "momento": ["spanish"],
        "estas": ["spanish"],
        "construcción": ["spanish"],
        "familia": ["spanish"],
        "millones": ["spanish"],
        "padre": ["spanish"],
        "tenía": ["spanish"],
        "desde": ["spanish"],
        "mayo": ["spanish", "english", "german"],
        "bande": ["french", "german"],
        "banque": ["french"],
        "bataille": ["french"],
        "bras": ["french"],
        "camp": ["french", "english"],
        "carrière": ["french"],
        "catégorie": ["french"],
        "certaine": ["french"],
        "chambres": ["french"],
        "championnat": ["french"],
        "charge": ["french", "english"],
        "cible": ["french"],
        "ciel": ["french"],
        "classe": ["french"],
        "client": ["french", "english"],
        "clients": ["french", "english"],
        "coeur": ["french"],
        "collaboration": ["french", "english"],
        "ces": ["french"],
        "pour": ["french"],
        "des": ["french", "german", "spanish"],
        "son": ["french", "spanish", "english"],
        "sera": ["french", "spanish"],
        "c'est": ["french"],
        "alors": ["french"],
        "travail": ["french"],
        "beaucoup": ["french"],
        "va": ["french", "spanish"],
        "faut": ["french"],
        "leur": ["french"],
        "je": ["french"],
        "lui": ["french"],
        "sans": ["french"],
        "doit": ["french"],
        "me": ["french", "spanish", "english"],
        "avant": ["french"],
        "enfants": ["french"],
        "faire": ["french"],
        "ligne": ["french"],
        "mois": ["french"],
        "points": ["french", "english"],
        "comment": ["french", "english"],
        "choix": ["french"],
        "d'une": ["french"],
        "demande": ["french"],
        "ensuite": ["french"],
        "peu": ["french"],
        "projet": ["french"],
        "semble": ["french"],
        "trouve": ["french"],
        "choses": ["french"],
        "fois": ["french"],
        "ma": ["french", "english", "german"],
        "porte": ["french"],
        "simple": ["french", "english"],
        "ville": ["french"],
        "this": ["english"],
        "can": ["english"],
        "they": ["english"],
        "but": ["english"],
        "her": ["english"],
        "other": ["english"],
        "on": ["english"],
        "she": ["english"],
        "more": ["english"],
        "called": ["english"],
        "many": ["english"],
        "who": ["english"],
        "used": ["english"],
        "two": ["english"],
        "a": ["english", "spanish", "french"],
        "been": ["english"],
        "about": ["english"],
        "time": ["english"],
        "made": ["english"],
        "there": ["english"],
        "all": ["english"],
        "them": ["english"],
        "into": ["english"],
        "after": ["english"],
        "when": ["english"],
        "its": ["english"],
        "several": ["english"],
        "well": ["english"],
        "important": ["english"],
        "now": ["english"],
        "does": ["english"],
        "each": ["english"],
        "game": ["english"],
        "october": ["english"],
        "back": ["english"],
        "found": ["english"],
        "as": ["english", "french", "german"],
        "united": ["english"],
        "left": ["english"],
        "person": ["english"],
        "both": ["english"],
        "life": ["english"],
        "january": ["english"],
        "may": ["english"],
        "university": ["english"],
        "death": ["english"],
        "get": ["english"],
        "just": ["english"],
        "state": ["english"],
        "what": ["english"],
        "much": ["english"],
        "under": ["english", "norwegian"],
        "september": ["english"],
        "lived": ["english"],
        "series": ["english"],
        "national": ["english", "german"],
        "band": ["english", "german"],
        "even": ["english"],
        "good": ["english"],
        "government": ["english"],
        "har": ["norwegian"],
        "at": ["norwegian", "english"],
        "hadde": ["norwegian"],
        "også": ["norwegian"],
        "han": ["norwegian", "spanish"],
        "seg": ["norwegian"],
        "den": ["norwegian", "german", "english"],
        "etter": ["norwegian"],
        "ved": ["norwegian"],
        "men": ["norwegian"],
        "det": ["norwegian"],
        "om": ["norwegian"],
        "første": ["norwegian"],
        "ikke": ["norwegian"],
        "sin": ["norwegian", "spanish", "english"],
        "to": ["norwegian", "english"],
        "år": ["norwegian"],
        "fikk": ["norwegian"],
        "hans": ["norwegian"],
        "andre": ["norwegian"],
        "da": ["norwegian", "spanish", "german"],
        "de": ["norwegian", "spanish"],
        "over": ["norwegian", "english"],
        "hun": ["norwegian", "english"],
        "mot": ["norwegian"],
        "flere": ["norwegian"],
        "eller": ["norwegian"],
        "kom": ["norwegian"],
        "ut": ["norwegian"],
        "opp": ["norwegian"],
        "meter": ["norwegian", "english", "german"],
        "senere": ["norwegian"],
        "blitt": ["norwegian"],
        "tre": ["norwegian"],
        "denne": ["norwegian"],
        "der": ["norwegian", "german"],
        "mellom": ["norwegian"],
        "dette": ["norwegian"],
        "vant": ["norwegian"],
        "inn": ["norwegian", "english"],
        "sammen": ["norwegian"],
        "gikk": ["norwegian"],
        "blant": ["norwegian"],
        "mange": ["norwegian"],
        "ha": ["norwegian", "spanish"],
        "sitt": ["norwegian"],
        "kan": ["norwegian"],
        "før": ["norwegian"],
        "på": ["norwegian"],
        "tilbake": ["norwegian"],
    }

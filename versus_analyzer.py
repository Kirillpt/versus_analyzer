class Versus:
    def __init__(self, versus_text, first_mc, second_mc):
        self.versus_text = versus_text
        self.first_mc    = first_mc
        self.second_mc   = second_mc
        self._rhyme      = None

    def get_rhymes(self):
        if self._rhyme is None:
            self._rhyme = set()
            first_word = ""
            second_word = ""
            for word in self.versus_text.split("\n"):
                if word.split() == []:
                    continue
                second_word = word.split()[-1].strip(" ,.!;:?").lower()
                if first_word != "":
                    for i in range(0, len(second_word)):
                        if first_word.endswith(second_word[i:]):
                            self._rhyme.add((first_word, second_word))
                first_word = second_word
        return self._rhyme

    def is_word_in_versus(self, target_word):
        if self.versus_text.find(target_word) != -1:
            return self.first_mc
        else:
            return None

# singleton class - storage for versus objects
class VersusStorage(object):

    versus_list = []

    def ___new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClass, cls).__new__(cls)
            return cls.instance

    def __parse_names(self, versus_name):
        firts_mc = ""
        second_mc = ""
        delimeter = " "
        mc_names = []

        if versus_name.find("против") != -1:
            delimeter = "против"
        elif versus_name.find("VS") != -1:
            delimeter = "VS"
        elif versus_name.find("vs") != -1:
            delimeter = "vs"
        elif versus_name.find("&") != -1:
            delimeter = "&"

        mc_names = versus_name.split(delimeter)

        if mc_names != []:
            first_mc = mc_names[0].strip()
            second_mc = mc_names[1].strip()
        else:
            return (None, None)
        return (first_mc, second_mc)

    def add_versus(self, versus_name, versus_text):
        first_mc, second_mc = self.__parse_names(versus_name)
        if first_mc == None:
            return
        else:
            self.versus_list.append(Versus(versus_text, first_mc, second_mc))

    def get_artists_used_word(self, target_word):
        artists = set()
        for versus in self.versus_list:
            artist = versus.is_word_in_versus(target_word)
            if artist != None:
                artists.add(artist)
        return artists

    def find_all_plagiat(self):

#        print(self.versus_list[0].get_rhymes())
        all_rhymes = set()
        result = dict()
        for versus in self.versus_list:
            all_rhymes.update(versus.get_rhymes())
        for rhyme in all_rhymes:
            for versus in self.versus_list:
                if rhyme in versus.get_rhymes():
                    if result.get(rhyme) is None:
                        result[rhyme] = set([versus.first_mc])
                    else:
                        result[rhyme].update([versus.first_mc])
        return result

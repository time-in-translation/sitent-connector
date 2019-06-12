class Annotation(object):
    def __init__(self, pk, words, indices, sentence):
        self.pk = pk
        self.words = list(filter(None, words))
        self.indices = list(filter(None, indices))
        self.sentence = sentence

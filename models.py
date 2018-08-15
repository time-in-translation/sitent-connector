class Annotation(object):
    def __init__(self, pk, words, indices, sentence):
        self.pk = pk
        self.words = filter(None, words)
        self.indices = filter(None, indices)
        self.sentence = sentence

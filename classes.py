class User:
    def __init__(self, username, password, email, self_id):
        self.user_name = username
        self.ID = self_id
        self.user_password = password
        self.user_email = email
        self.cardsCreated = 0


class Flashcard:
    def __init__(self, question, answer, creator_id, set_id, self_id=0):
        self.ID = self_id
        self.Question = question
        self.Answer = answer
        self.User = creator_id
        self.Set = set_id


class Set:
    def __init__(self, creator_id, description, self_id=None, Flashcards=[0]):
        self.ID = self_id
        self.Creator = creator_id
        self.Flashcards = Flashcards
        self.description = description

    def addFlashcard(self, Flashcard):
        if self.Flashcards[0] == 0:
            self.Flashcards[0] = Flashcard
        else:
            self.Flashcards.append(Flashcard)

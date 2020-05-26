from bson import ObjectId
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
from kivy.lang import Builder
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from bson.json_util import dumps
import editdistance
import random
import pymongo
import DBConnection
import classes
from kivy.uix.togglebutton import ToggleButton

kv = Builder.load_file("my.kv")


class WindowManager(ScreenManager):
    pass

sm = WindowManager()


mail = ""
flashcard_set = classes.Set("1", "a")
current_sets = {}

db_x = DBConnection.DBConnection()


class Pop(FloatLayout):
    pass


class Pop1(FloatLayout):
    pass


class Pop2(FloatLayout):
    pass


class Pop3(FloatLayout):
    pass


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    font_size_large = NumericProperty(20)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            x = db_x.add_user(self.namee.text, self.email.text, self.password.text)
            if x == 1:
                self.show_popup2()
                # db_u.add_user(self.email.text, self.password.text, self.namee.text)
                # db_x.add_user(self.namee.text, self.email.text, self.password.text)
                self.reset()
                sm.current = "login"
            elif x == -1:
                self.show_popup3()
                self.reset_pass()
                sm.current = "create"
            elif x == -2:
                self.show_popup4()
                self.reset()
                sm.current = "create"
        else:
            self.reset()
            self.show_popup1()
            sm.current = "create"

    def reset_pass(self):
        self.password.text = ""

    def show_popup1(self):
        show = Pop()
        popupWindow = Popup(title="Error!", content=show, size_hint=(None, None), size=(200, 200))
        popupWindow.open()

    def show_popup2(self):
        show = Pop1()
        popupWindow = Popup(title="Account created!", content=show, size_hint=(None, None), size=(300, 200))
        popupWindow.open()

    def show_popup3(self):
        show = Pop2()
        popupWindow = Popup(title="Error!", content=show, size_hint=(None, None), size=(400, 200))
        popupWindow.open()

    def show_popup4(self):
        show = Pop3()
        popupWindow = Popup(title="Error!", content=show, size_hint=(None, None), size=(200, 200))
        popupWindow.open()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class HomeScreenWindow(Screen):

    def log_out(self):
        sm.current = "login"

    def create_set(self):
        sm.current = "createSet"

    def searchSet(self):
        sm.current = "searchSet"

    def all_sets(self):
        global current_sets
        current_sets.clear()
        current_sets = db_x.all_sets()
        sm.current="availableSets"


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        # if db_u.validate(self.email.text, self.password.text):
        x = db_x.user_auth(self.email.text, self.password.text)
        if x == 1:
            global mail
            mail = self.email.text
            #HomeWindow.current = self.email.text
            self.reset()
            sm.current = "homeScreenWindow"
        elif x == -1:
            self.reset()
            self.show_popup1()
            sm.current = "login"
        else:
            self.reset()
            self.show_popup2()
            sm.current = "login"

    def show_popup1(self):
        show = P()
        popupWindow = Popup(title="Login error", content=show, size_hint=(None, None), size=(200, 200))
        popupWindow.open()

    def show_popup2(self):
        show = P1()
        popupWindow = Popup(title="Login error", content=show, size_hint=(None, None), size=(200, 200))
        popupWindow.open()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

    def back(self):
        sm.current = "login"


# class MyLabel(Label):
#     def on_size(self, *args):
#         self.canvas.before.clear()
#         with self.canvas.before:
#             Color(0, 1, 0, 0.25)
#             Rectangle(pos=(self.pos[0] + self.size[0] * 0.1, self.pos[1] + self.size[1] * 0.1),
#                       size=(self.size[0] * 0.8, self.size[1] * 0.8))

class LearningMethodWindow(Screen):
    def __init__(self, **kwargs):
        super(LearningMethodWindow, self).__init__(**kwargs)

    def reviewBtn(self):
        sm.current = "review"

    def testBtn(self):
        sm.current = "test"

    def quizBtn(self):
        if len(flashcard_set.Flashcards) >= 4:
            sm.current = "quiz"
        else:
            self.show_popup()

    def show_popup(self):
        show = Pop1()
        popupWindow = Popup(title="Too few flashcards in set!", content=show, size_hint=(None, None), size=(200, 200))
        popupWindow.open()


    def mainMenu(self):
        sm.current = "homeScreenWindow"


class LearningWindow(Screen):
    def __init__(self, **kwargs):
        super(LearningWindow, self).__init__(**kwargs)

    def browse_sets(self):
        self.reset()
        sm.current = "searchSet"

    def learningMethod(self):
        sm.current = "learningMethod"
        self.reset()

    def allSets(self):
        global current_sets
        current_sets.clear()
        current_sets = db_x.all_sets()
        self.reset()
        sm.current = "availableSets"


class ReviewWindow(LearningWindow):
    def __init__(self, **kwargs):
        super(ReviewWindow, self).__init__(**kwargs)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.card_button_texts = dict()

    def on_enter(self, *args):
        for card in flashcard_set.Flashcards:
            texts = (card.Question, card.Answer)
            button_term = ToggleButton(text=texts[0], halign='center', valign='middle')
            button_term.size_hint = (0.65, 0.35)
            button_term.bind(on_press=self.switched)
            self.card_button_texts[button_term] = texts
            self.ids.grid.add_widget(button_term)

    def switched(self, instance):
        texts = self.card_button_texts[instance]
        if instance.text == texts[0]:
            instance.text = texts[1]
        else:
            instance.text = texts[0]

    def reset(self, *args):
        for button in self.card_button_texts.keys():
            self.ids.grid.remove_widget(button)


class TestWindow(LearningWindow):
    def __init__(self, **kwargs):
        super(TestWindow, self).__init__(**kwargs)
        self.question_ids = None
        self.current_question = None

    def on_enter(self, *args):
        self.question_ids = set(range(len(flashcard_set.Flashcards)))
        self.next_question()

    def validate(self):
        user_answer = self.ids.answer.text
        correct_answer = flashcard_set.Flashcards[self.current_question].Answer
        editdist = editdistance.eval(user_answer, correct_answer)
        if editdist == 0:
            self.send_message('Correct!')
            self.question_ids.remove(self.current_question)
            Clock.schedule_once(lambda dt: self.next_question(), 0.8)
        elif editdist == 1:
            self.ids.result.text = 'You had a typo, correct answer: \'{}\''.format(correct_answer)
            self.question_ids.remove(self.current_question)
            Clock.schedule_once(lambda dt: self.next_question(), 2)
        else:
            self.ids.result.text = 'Wrong! Correct answer: \'{}\''.format(correct_answer)
            Clock.schedule_once(lambda dt: self.next_question(), 2.5)

    def send_message(self, message):
        self.ids.result.text = message

    def next_question(self):
        self.reset()
        if len(self.question_ids) != 0:
            self.current_question = random.choice(tuple(self.question_ids))
            self.ids.question.text = flashcard_set.Flashcards[self.current_question].Question
        else:
            self.ids.question.text = ""
            self.ids.result.text = 'Congratulations, you finished this set!'

    def reset(self, *args):
        self.ids.answer.text = ""
        self.ids.result.text = ""


class QuizWindow(LearningWindow):
    def __init__(self, **kwargs):
        super(QuizWindow, self).__init__(**kwargs)
        self.question_ids = None
        self.current_question = None
        self.buttons = [self.ids.but1, self.ids.but2, self.ids.but3, self.ids.but4]
        for button in self.buttons:
            button.background_normal = ''

    def on_enter(self, *args):
        self.question_ids = set(range(len(flashcard_set.Flashcards)))
        self.next_question()

    def validate(self, instance):
        user_answer = instance.text
        correct_answer = flashcard_set.Flashcards[self.current_question].Answer
        if user_answer == correct_answer:
            instance.background_color = (0.133, 0.545, 0.133, 1.0)
            self.question_ids.remove(self.current_question)
            Clock.schedule_once(lambda dt: self.next_question(), 0.8)
        else:
            instance.background_color = (0.698, 0.133, 0.133, 1.0)
            for button in self.buttons:
                if button.text == correct_answer:
                    button.background_color = (0.133, 0.545, 0.133, 1.0)
                    break
            # self.ids.result.text = 'Wrong! Correct answer: \'{}\''.format(correct_answer)
            Clock.schedule_once(lambda dt: self.next_question(), 2.5)

    def next_question(self):
        self.reset()
        if len(self.question_ids) != 0:
            self.current_question = random.choice(tuple(self.question_ids))
            self.ids.question.text = flashcard_set.Flashcards[self.current_question].Question
            current_flashcard = flashcard_set.Flashcards[self.current_question]
            answers = [f.Answer for f in flashcard_set.Flashcards if f != current_flashcard]
            answers = random.sample(answers, 3)
            answers.append(current_flashcard.Answer)
            random.shuffle(answers)
            for button, answer in zip(self.buttons, answers):
                button.text = answer
        else:
            self.ids.question.text = 'Congratulations, you finished this set!'
            self.reset()

    def reset(self, *args):
        for button in self.buttons:
            button.text = ""
            button.background_color = (0.4, 0.4, 0.4, 1.0)


class CreateSet(Screen):
    description = ObjectProperty(None)

    def log_out(self):
        sm.current = "login"
        self.reset()

    def mainMenu(self):
        sm.current = "homeScreenWindow"
        self.reset()

    def reset(self):
        self.description.text = ""

    def createSet(self):
        global flashcard_set
        flashcard_set = classes.Set(db_x.get_id(mail), self.description.text)
        # print(flashcard_set.ID)
        # print(flashcard_set.Flashcards)
        self.reset()
        sm.current = "createFlashcard"


class CreateFlashcard(Screen):
    front = ObjectProperty(None)
    back = ObjectProperty(None)

    def log_out(self):
        sm.current = "login"

    def mainMenu(self):
        sm.current = "homeScreenWindow"

    def reset(self):
        self.front.text = ""
        self.back.text = ""

    def show_popup1(self):
        show = P2()
        popupWindow = Popup(title="Create flashcard", content=show, size_hint=(None, None), size=(300, 200))
        popupWindow.open()


    def show_popup2(self):
        show = P3()
        popupWindow = Popup(title="Create flashcard", content=show, size_hint=(None, None), size=(300, 200))
        popupWindow.open()

    def addFlashcard(self):
        flashcard = classes.Flashcard(self.front.text, self.back.text, db_x.get_id(mail), flashcard_set.ID)
        flashcard_set.addFlashcard(flashcard)
        # print(flashcard_set.Flashcards)
        self.show_popup2()
        self.reset()

    def uploadSet(self):
        db_x.upload_set(flashcard_set)
        sm.current = "homeScreenWindow"


class SearchSet(Screen):
    keyword = ObjectProperty(None)

    def mainMenu(self):
        sm.current = "homeScreenWindow"
        self.reset()

    def searchSet(self):
        global current_sets
        current_sets.clear()
        current_sets = db_x.sets_list_for_selection(self.keyword.text)

        sm.current = "availableSets"
        self.reset()

    def reset(self):
        self.keyword.text = ""


# class AvailableSets(RecycleView):
#     # def mainMenu(self):
#     #     sm.current="homeScreenWindow"
#     def __init__(self, **kwargs):
#         super(AvailableSets, self).__init__(**kwargs)
#         print("im here!!!")
#         self.data = [{'text': cardsset.description} for cardsset in current_sets]
#         # for cardset in current_sets:
#         #     print(cardset.description)
#         # # self.data = [{'text': str(x)} for x in range(10)]
#         # self.data = [{'text': cardsset.description} for cardsset in current_sets]


class AvailableSets(Screen):
    def __init__(self, **kwargs):
        super(AvailableSets, self).__init__(**kwargs)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.sets = []

    def on_enter(self, *args):
        for (key, cardsSet) in current_sets.items():
            button = Button(text=cardsSet.description + " : ID:"+str(cardsSet.ID))
            button.size_hint = (0.8, 0.35)
            button.bind(on_press=self.pressed)
            self.sets.append(button)
            self.ids.grid.add_widget(button)

    def pressed(self, instance):
        setID = instance.text.split(':')[2]
        global flashcard_set
        del flashcard_set
        flashcard_set = current_sets[ObjectId(setID)]
        current_sets.clear()
        sm.current = "learningMethod"
        self.reset()

    def mainMenu(self):
        sm.current = "homeScreenWindow"
        self.reset()

    def reset(self):
        for button in self.sets:
            self.ids.grid.remove_widget(button)


class P(FloatLayout):
    pass

class P1(FloatLayout):
    pass

class P2(FloatLayout):
    pass

class P3(FloatLayout):
    pass


screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),
           ReviewWindow(name="review"),  #MySetsWindow(name="my_sets")
           HomeScreenWindow(name="homeScreenWindow"), CreateFlashcard(name="createFlashcard"),
           CreateSet(name="createSet"), SearchSet(name="searchSet"),
           AvailableSets(name="availableSets"), LearningMethodWindow(name="learningMethod"),
           TestWindow(name="test"), QuizWindow(name="quiz")]


for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    font_size_large = NumericProperty(20)

    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()

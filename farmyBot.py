from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

my_bot = ChatBot(name='PyBot', read_only=True,
                 logic_adapters=['chatterbot.logic.MathematicalEvaluation',
                                 'chatterbot.logic.BestMatch'])


small_talk = ['Sorry,I am unable to get you!',
              'Hi,welcome to farmy!',
              'hi there!',
              'hi!',
              'how do you do?',
              'how are you?',
              'i\'m cool.',
              'fine, you?',
              'always cool.',
              'i\'m ok',
              'glad to hear that.',
              'i\'m fine',
              'glad to hear that.',
              'i feel awesome',
              'excellent, glad to hear that.',
              'not so good',
              'sorry to hear that.',
              'what\'s your name?',
              'i\'m FarmyBot. ask me a question, please.',
              'what is farmy?',
              'Farmy is Platform to connect farmers and agricultural authorities for solving issues/queries of farmers.',
              'who developed farmy?',
              'Our Team\n1.Venu Bura\n2.Hemant Dyavarkonda\n3.Omsai Kalekar\nMahesh Rachha.']

math_talk_1 = ['pythagorean theorem',
               'a squared plus b squared equals c squared.']
math_talk_2 = ['law of cosines',
               'c**2 = a**2 + b**2 - 2 * a * b * cos(gamma)']

list_trainer = ListTrainer(my_bot)
for item in (small_talk, math_talk_1, math_talk_2):
    list_trainer.train(item)

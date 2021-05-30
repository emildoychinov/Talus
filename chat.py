from chatterbot import ChatBot
from chatterbot.trainers import UbuntuCorpusTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
class chat ():
    def __init__(self):
        self.chatbot = ChatBot('Talus')
        self.flag = 0
    def train(self):
        trainer = ChatterBotCorpusTrainer(self.chatbot)
        trainer.train('chatterbot.corpus.english')
    def respond(self, msg):
        if self.flag == 0:
            self.train()
            self.flag = 1
        return self.chatbot.get_response(msg)

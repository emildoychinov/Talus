import re
import random
import numpy as np
from tensorflow import keras
from keras.layers import *
from keras.models import Model
from keras.models import load_model
class utils:
    def __init__(self):
        self.pairs = []
        self.inputTokens = set()
        self.inputSequence = []
        self.targetTokens = set()
        self.targetSequence = []
        self.inputDict = {}
        self.inv_inputDict = {}
        self.targetDict = {}
        self.inv_targetDict = {}
        self.encSeqLen = 0
        self.decSeqLen = 0
        self.encoderInput = None
        self.decoderInput = None
        self.decoderTarget = None
        self.decoderLSTM = None
        self.decoderDense = None
        self.decoderInputs = None
        self.decoderModel = None
        self.encoderModel = None
        self.flag = False


    def getData(self):
        reg_pattern = re.compile(pattern = "["
                u"\U0001F600-\U0001F64F"
                u"\U0001F300-\U0001F5FF"
                u"\U0001F680-\U0001F6FF"
                u"\U0001F1E0-\U0001F1FF"
                "]+", flags = re.UNICODE)
        with open('human_text.txt', 'r', encoding='utf-8') as f:
            humanInput = f.read().split('\n')
            humanInput = [reg_pattern.sub(r'', text) for text in humanInput]
            humanInput = [re.sub(r"\[\w+\]",'hi',line) for line in humanInput]
            humanInput = [' '.join(re.findall(r'\w+',line)) for line in humanInput]
        with open('robot_text.txt', 'r', encoding='utf-8') as f:
            botOutput = f.read().split('\n')
            botOutput = botOutput = [reg_pattern.sub(r'', text) for text in botOutput]
            botOutput = [re.sub(r"\[\w+\]",'',line) for line in botOutput]
            botOutput = [' '.join(re.findall(r"\w+",line)) for line in botOutput]
        self.pairs = list(zip(humanInput, botOutput))
        return self.pairs

    def tokenize(self, size = 450):
        self.getData()
        for pair in self.pairs[:size]:
            inpt, target = pair[0:]
            target = " ".join(re.findall("[\w']+|[^\s\w]", target))
            target = '<START> ' + target + ' <END>'
            for token in re.findall(r"[\w']+|[^\s\w]", inpt):
                if token not in self.inputTokens:
                    self.inputTokens.add(token)
            for token in target.split():
                if token not in self.targetTokens :
                    self.targetTokens.add(token)
        self.inputTokens, self.targetTokens = sorted(list(self.inputTokens)), sorted(list(self.targetTokens))
        return [self.inputTokens, self.targetTokens]

    def makeSequences(self, size = 450):
        self.getData()
        for pair in self.pairs[:size]:
            inpt, target = pair[0:]
            self.inputSequence.append(inpt)
            target = '<START> '+" ".join(re.findall(r"[\w']+|[^\s\w]", target))+' <END>'
            self.targetSequence.append(target)
        return [self.inputSequence, self.targetSequence]

    def makeDicts(self):
        invertDict = lambda dict : {i : token for token, i in dict.items()}
        self.tokenize()
        self.inputDict = dict([(token, i) for i, token in enumerate(self.inputTokens)])
        self.targetDict = dict([(token, i) for i, token in enumerate(self.targetTokens)])
        self.inv_inputDict = invertDict(self.inputDict)
        self.inv_targetDict = invertDict(self.targetDict)
        return [self.inputDict, self.targetDict, self.inv_inputDict, self.inv_targetDict]

    def makeMatrices(self):
        self.makeSequences()
        self.makeDicts()
        self.encSeqLen = max([len(re.findall(r"[\w']+|[^\s\w]", line)) for line in self.inputSequence])
        self.decSeqLen = max([len(re.findall(r"[\w']+|[^\s\w]", line)) for line in self.targetSequence])
        self.encoderInput = np.zeros((len(self.inputSequence), self.encSeqLen, len(self.inputTokens)), dtype = 'float32')
        self.decoderInput = np.zeros((len(self.inputSequence), self.decSeqLen,  len(self.targetTokens)), dtype = 'float32')
        self.decoderTarget = np.zeros((len(self.inputSequence), self.decSeqLen,  len(self.targetTokens)), dtype = 'float32')
        for line, (inpt, target) in enumerate(zip(self.inputSequence, self.targetSequence)) :
            for timestep, token in enumerate(re.findall(r"[\w']+|[^\s\w]", inpt)) :
                self.encoderInput[line, timestep, self.inputDict[token]] = 1.
            for timestep, token in enumerate(target.split()):
                self.decoderInput[line, timestep, self.targetDict[token]] = 1.
                if timestep > 0 :
                    self.decoderTarget[line, timestep-1, self.targetDict[token]] = 1.
        return [self.encoderInput, self.decoderInput, self.decoderTarget, self.encSeqLen, self.decSeqLen]

    def makeModel(self, dimensionality = 256, epochs = 1200, batch_size = 32):
        self.makeMatrices()

        encoderInputs = Input(shape=(None, len(self.inputTokens)))
        encoderLSTM = LSTM(dimensionality, return_state = True)
        encoderOutputs, stateHidden, stateCell = encoderLSTM(encoderInputs)
        encoderStates = [stateHidden, stateCell]

        self.decoderInputs = Input(shape=(None, len(self.targetTokens)))
        self.decoderLSTM = LSTM(dimensionality, return_sequences = True, return_state = True)
        decoderOutputs, decoderStateHidden, decoderStateCell = self.decoderLSTM(self.decoderInputs, initial_state = encoderStates)
        self.decoderDense = Dense(len(self.targetTokens), activation = 'softmax')
        decoderOutputs = self.decoderDense(decoderOutputs)

        trainingModel = Model([encoderInputs, self.decoderInputs], decoderOutputs)
        trainingModel.compile(optimizer = 'rmsprop', loss='categorical_crossentropy', metrics=['accuracy'], sample_weight_mode='temporal')

        trainingModel.fit([self.encoderInput, self.decoderInput], self.decoderTarget, batch_size = batch_size, epochs = epochs, validation_split = 0.2)

        trainingModel.save('model.h5')

        return [self.decoderLSTM, self.decoderDense, self.decoderInputs]

    def testModel(self, latent_dim = 256):
        self.makeModel()

        trainingModel = load_model('model.h5')
        encoderInputs = trainingModel.input[0]
        encoderOutputs, stateHiddenEncoder, stateCellEncoder = trainingModel.layers[2].output
        encoderStates = [stateHiddenEncoder, stateCellEncoder]
        self.encoderModel = Model(encoderInputs, encoderStates)

        decoderStateInputHidden = Input(shape=(latent_dim,))
        decoderStateInputCell = Input(shape=(latent_dim,))
        decoderStatesInputs = [decoderStateInputHidden, decoderStateInputCell]

        decoderOutputs, stateHidden, stateCell = self.decoderLSTM(self.decoderInputs, initial_state = decoderStatesInputs)
        decoderStates = [stateHidden, stateCell]
        decoderOutputs = self.decoderDense(decoderOutputs)
        self.decoderModel = Model([self.decoderInputs]+decoderStatesInputs, [decoderOutputs] + decoderStates)
        self.flag = True
        return[self.encoderModel, self.decoderModel]

    def decode(self, inp):
        if not self.flag:
            self.testModel()
        statesValue = self.encoderModel.predict(inp)
        targetSeq = np.zeros((1,1,len(self.targetTokens)))
        targetSeq[0,0,self.targetDict['<START>']] = 1.
        decoded = ''
        stop = False
        while not stop:
            outputTokens, hiddenState, cellState = self.decoderModel.predict([targetSeq]+statesValue)
            tokenIndex = np.argmax(outputTokens[0,-1,:])
            token = self.inv_targetDict[tokenIndex]
            decoded += token + ' '
            if token == '<END>' or len(decoded) > self.decSeqLen :
                stop = True
            targetSeq = np.zeros((1,1,len(self.targetTokens)))
            targetSeq[0,0,tokenIndex] = 1.
            statesValue = [hiddenState, cellState]

        decoded = decoded.split()
        if '<END>' in decoded :
            decoded.remove('<END>')
        if '<START>' in decoded:
            decoded.remove('<START>')
        decoded = ' '.join(decoded)
        return decoded

class ChatBot :
    def __init__(self):
        self.utils = utils()
    def prepare(self):
        self.utils.testModel()
    def strToMatrix(self, userInput):
        tokens = re.findall(r"[\w']+|[^\s\w]", userInput)
        userInputMatrix = np.zeros((1, self.utils.encSeqLen, len(self.utils.inputTokens)),dtype = 'float32')
        for timestep, token in enumerate(tokens):
            if token in self.utils.inputDict :
                userInputMatrix[0,timestep,self.utils.inputDict[token]] = 1.
        return userInputMatrix

    def respond(self, userInput):
        inputMatrix = self.strToMatrix(userInput)
        botResponse = self.utils.decode(inputMatrix)
        return botResponse

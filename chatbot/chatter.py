import re
import random
import numpy as np
from tensorflow import keras
from keras.layers import *
from keras.models import Model
from keras.models import load_model
def getData():
    #a regex pattern that will be used to remove the emojis from the dataset i am using
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
    pairs = list(zip(humanInput, botOutput))
    return pairs

def tokenize(size = 1500):
    inputTokens = set()
    targetTokens = set()
    pairs = getData()
    #random.shuffle(pairs)
    for pair in pairs[:size]:
        inpt, target = pair[0:]
        target = " ".join(re.findall("[\w']+|[^\s\w]", target))
        target = '<START> ' + target + ' <END>'
        for token in re.findall(r"[\w']+|[^\s\w]", inpt):
            if token not in inputTokens:
                inputTokens.add(token)
        for token in target.split():
            if token not in targetTokens :
                targetTokens.add(token)
    return [list(sorted(list(inputTokens))), list(sorted(list(targetTokens)))]

def makeSequences(size = 1500):
    inputSequence = []
    targetSequence = []
    pairs = getData()
    #random.shuffle(pairs)
    for pair in pairs[:size]:
        inpt, target = pair[0:]
        inputSequence.append(inpt)
        target = '<START> '+" ".join(re.findall(r"[\w']+|[^\s\w]", target))+' <END>'
        targetSequence.append(target)
    return [inputSequence, targetSequence]

def makeDicts():
    invertDict = lambda dict : {i : token for token, i in dict.items()}
    inputTokens, targetTokens = tokenize()[0:]
    inputDict = dict([(token, i) for i, token in enumerate(inputTokens)])
    targetDict = dict([(token, i) for i, token in enumerate(targetTokens)])
    inv_inputDict = invertDict(inputDict)
    inv_targetDict = invertDict(targetDict)
    return [inputDict, targetDict, inv_inputDict, inv_targetDict]

def makeMatrices():
    inputSequence, targetSequence = makeSequences()[0:]
    inputTokens, targetTokens = tokenize()[0:]
    inputDict, targetDict, inv_inputDict, inv_targetDict = makeDicts()[0:]
    encSeqLen = max([len(re.findall(r"[\w']+|[^\s\w]", line)) for line in inputSequence])
    decSeqLen = max([len(re.findall(r"[\w']+|[^\s\w]", line)) for line in targetSequence])
    encoderInput = np.zeros((len(inputSequence), encSeqLen, len(inputTokens)), dtype = 'float32')
    decoderInput = np.zeros((len(inputSequence), decSeqLen,  len(targetTokens)), dtype = 'float32')
    decoderTarget = np.zeros((len(inputSequence), decSeqLen,  len(targetTokens)), dtype = 'float32')
    for line, (inpt, target) in enumerate(zip(inputSequence, targetSequence)) :
        for timestep, token in enumerate(re.findall(r"[\w']+|[^\s\w]", inpt)) :
            encoderInput[line, timestep, inputDict[token]] = 1.
        for timestep, token in enumerate(target.split()):
            decoderInput[line, timestep, targetDict[token]] = 1.
            if timestep > 0 :
                decoderTarget[line, timestep-1, targetDict[token]] = 1.
    return [encoderInput, decoderInput, decoderTarget, encSeqLen, decSeqLen]

def makeModel(dimensionality=256, epochs=35, batch_size=10):
    encoderInput, decoderInput, decoderTarget, encSeqLen, decSeqLen = makeMatrices()[0:]
    inputSequence, targetSequence = makeSequences()[0:]
    inputTokens, targetTokens = tokenize()[0:]
    inputDict, targetDict, inv_inputDict, inv_targetDict = makeDicts()[0:]

    encoderInputs = Input(shape=(None, len(inputTokens)))
    encoderLSTM = LSTM(dimensionality, return_state = True)
    encoderOutputs, stateHidden, stateCell = encoderLSTM(encoderInputs)
    encoderStates = [stateHidden, stateCell]
    
    decoderInputs = Input(shape=(None, len(targetTokens)))
    decoderLSTM = LSTM(dimensionality, return_sequences = True, return_state = True)
    decoderOutputs, decoderStateHidden, decoderStateCell = decoderLSTM(decoderInputs, initial_state = encoderStates)
    decoderDense = Dense(len(targetTokens), activation = 'softmax')
    decoderOutputs = decoderDense(decoderOutputs)

    trainingModel = Model([encoderInputs, decoderInputs], decoderOutputs)
    trainingModel.compile(optimizer = 'rmsprop', loss='categorical_crossentropy', metrics=['accuracy'], sample_weight_mode='temporal')

    trainingModel.fit([encoderInput, decoderInput], decoderTarget, batch_size = batch_size, epochs = epochs, validation_split = 0.2)
    trainingModel.save('model.h5')

    return [decoderLSTM, decoderDense, decoderInputs]

def testModel(latent_dim = 256):
    decoderLSTM, decoderDense, decoderInputs = makeModel()[0:]

    trainingModel = load_model('model.h5')
    encoderInputs = trainingModel.input[0]
    encoderOutputs, stateHiddenEncoder, stateCellEncoder = trainingModel.layers[2].output
    encoderStates = [stateHiddenEncoder, stateCellEncoder]
    encoderModel = Model(encoderInputs, encoderStates)

    decoderStateInputHidden = Input(shape=(latent_dim,))
    decoderStateInputCell = Input(shape=(latent_dim,))
    decoderStatesInputs = [decoderStateInputHidden, decoderStateInputCell]

    decoderOutputs, stateHidden, stateCell = decoderLSTM(decoderInputs, initial_state = decoderStatesInputs)
    decoderStates = [stateHidden, stateCell]
    decoderOutputs = decoderDense(decoderOutputs)
    decoderModel = Model([decoderInputs]+decoderStatesInputs, [decoderOutputs] + decoderStates)

    return[encoderModel, decoderModel]

def decode(inp):
    encoderInput, decoderInput, decoderTarget, encSeqLen, decSeqLen = makeMatrices()[0:]
    inputSequence, targetSequence = makeSequences()[0:]
    inputTokens, targetTokens = tokenize()[0:]
    inputDict, targetDict, inv_inputDict, inv_targetDict = makeDicts()[0:]

    encoderModel, decoderModel = testModel()[0:]
    statesValue = encoderModel.predict(inp)
    targetSeq = np.zeros((1,1,len(targetTokens)))
    targetSeq[0,0,targetDict['<START>']] = 1.
    decoded = ''
    stop = False
    while not stop:
        outputTokens, hiddenState, cellState = decoderModel.predict([targetSeq]+statesValue)
        tokenIndex = np.argmax(outputTokens[0,-1,:])
        token = inv_targetDict[tokenIndex]
        decoded += token + ' '
        if token == '<END>' or len(decoded) > decSeqLen :
            stop = True
        targetSeq = np.zeros((1,1,len(targetTokens)))
        targetSeq[0,0,tokenIndex] = 1.
        statesValue = [hiddenState, cellState]
    
    return decoded

class ChatBot :
    encoderInput, decoderInput, decoderTarget, encSeqLen, decSeqLen = makeMatrices()[0:]
    inputSequence, targetSequence = makeSequences()[0:]
    inputTokens, targetTokens = tokenize()[0:]
    inputDict, targetDict, inv_inputDict, inv_targetDict = makeDicts()[0:]
    def start_chat(self):
        userResponse = input("hello\n")
        if userResponse == 'no' : return
        self.chat(userResponse)
    def chat(self, reply):
        while reply != 'quit' : 
            reply = input(self.generateResponse(reply)+'\n')
    def strToMatrix(self, userInput):
        tokens = re.findall(r"[\w']+|[^\s\w]", userInput)
        userInputMatrix = np.zeros((1, self.encSeqLen, len(self.inputTokens)),dtype = 'float32')
        for timestep, token in enumerate(tokens):
            if token in self.inputDict :
                userInputMatrix[0,timestep,self.inputDict[token]] = 1.
        return userInputMatrix

    def generateResponse(self, userInput):
        inputMatrix = self.strToMatrix(userInput)
        botResponse = decode(inputMatrix)
        botResponse.replace('<START>', '')
        botResponse.replace(' <END>', '')
        return botResponse


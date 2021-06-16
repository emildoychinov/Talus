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

    #reading the data from the datasets we are using
    def getData(self):
        #a regex pattern that will be used to remove all the emojis from the dataset
        reg_pattern = re.compile(pattern = "["
                u"\U0001F600-\U0001F64F"  
                u"\U0001F300-\U0001F5FF"  
                u"\U0001F680-\U0001F6FF"  
                u"\U0001F1E0-\U0001F1FF"
                "]+", flags = re.UNICODE)
        #we clean the human responses
        with open('human_text.txt', 'r', encoding='utf-8') as f:
            #splitting the text that we just got from the file
            humanInput = f.read().split('\n')
            #since the dataset is not ideal and it has text like '[voice]', if a thing like that is encountered we just replace it with hi
            humanInput = [re.sub(r"\[\w+\]",'hi',line) for line in humanInput]
            #we turn the list of reponses into a string
            humanInput = [' '.join(re.findall(r'\w+',line)) for line in humanInput]
        #we clean the bot responses
        with open('robot_text.txt', 'r', encoding='utf-8') as f:
            botOutput = f.read().split('\n')
            botOutput = [re.sub(r"\[\w+\]",'',line) for line in botOutput]
            botOutput = [' '.join(re.findall(r"\w+",line)) for line in botOutput]
        #we make a human - bot response list of tuples (for ex (hello, hi), where hello is part of the human speech and hi - a part of the robot speech)
        self.pairs = list(zip(humanInput, botOutput))
        #we return the pairs
        return self.pairs
    #here we tokenize the data
    def tokenize(self, size = 450):
        #we read from the corpus
        self.getData()
        #size can be altered
        #the higher the size the better the accuracy
        for pair in self.pairs[:size]:
            #we get the input token and the target token
            inpt, target = pair[0:]
            #we remove any aphostrophes from the token
            target = " ".join(re.findall("[\w']+|[^\s\w]", target))
            #since we are doing a seq2seq algorithm, we add <START> and <END> so our model will know where to start and end text generation
            target = '<START> ' + target + ' <END>'
            #we go through the tokens
            for token in re.findall(r"[\w']+|[^\s\w]", inpt):
                #if the token hasn't been already added we add it
                #that way we will only have unique words
                if token not in self.inputTokens:
                    self.inputTokens.add(token)
            #we do the same for the target tokens
            for token in target.split():
                if token not in self.targetTokens :
                    self.targetTokens.add(token)
        #we return the tokens
        self.inputTokens, self.targetTokens = sorted(list(self.inputTokens)), sorted(list(self.targetTokens))
        return [self.inputTokens, self.targetTokens]

    def makeSequences(self, size = 450):
        #we load the corpus
        self.getData()
        #here we make the sequences for our bot
        #the first one is the input(human) sequence and the second one is the target(bot) sequence
        for pair in self.pairs[:size]:
            inpt, target = pair[0:]
            self.inputSequence.append(inpt)
            target = '<START> '+" ".join(re.findall(r"[\w']+|[^\s\w]", target))+' <END>'
            self.targetSequence.append(target)
        return [self.inputSequence, self.targetSequence]
    #we need dictionaries so the encoder - decoder process can be easier
    #we have an input and a target features dictionary, they will store the word as the key and the value as the index
    #similarly, we have a reversed input and a reversed target features dict, since we will need them for the decoding process
    def makeDicts(self):
        #a lambda function to reverse a dict
        invertDict = lambda dict : {i : token for token, i in dict.items()}
        self.tokenize()
        #we make the input and the tareget dict
        self.inputDict = dict([(token, i) for i, token in enumerate(self.inputTokens)])
        self.targetDict = dict([(token, i) for i, token in enumerate(self.targetTokens)])
        #we reverse them
        self.inv_inputDict = invertDict(self.inputDict)
        self.inv_targetDict = invertDict(self.targetDict)
        return [self.inputDict, self.targetDict, self.inv_inputDict, self.inv_targetDict]
    #to train our seq2seq model we will use three matrices of one-hot vectors
    #one for the encoder (input data) and two for the decoder(input and output data)
    #we need two matrices for the decoder since the method we are using is teacher forcing 
    #teacher forcing is a technique where the target word is passed as the next input to the decoder
    def makeMatrices(self):
        #we make the sequences and the dictionaries
        self.makeSequences()
        self.makeDicts()
        #this is the maximum lenght for an encoder sequence
        self.encSeqLen = max([len(re.findall(r"[\w']+|[^\s\w]", line)) for line in self.inputSequence])
        #the maximum lenght for a decoder sequence
        self.decSeqLen = max([len(re.findall(r"[\w']+|[^\s\w]", line)) for line in self.targetSequence])
        #we make the three matrices
        self.encoderInput = np.zeros((len(self.inputSequence), self.encSeqLen, len(self.inputTokens)), dtype = 'float32')
        self.decoderInput = np.zeros((len(self.inputSequence), self.decSeqLen,  len(self.targetTokens)), dtype = 'float32')
        self.decoderTarget = np.zeros((len(self.inputSequence), self.decSeqLen,  len(self.targetTokens)), dtype = 'float32')
        
        for line, (inpt, target) in enumerate(zip(self.inputSequence, self.targetSequence)) :
            #we assign for the current, line, timestep and word in the encoder input data
            for timestep, token in enumerate(re.findall(r"[\w']+|[^\s\w]", inpt)) :
                self.encoderInput[line, timestep, self.inputDict[token]] = 1.
            #we do the same for the decoder input data
            for timestep, token in enumerate(target.split()):
                self.decoderInput[line, timestep, self.targetDict[token]] = 1.
                if timestep > 0 :
                    #if the timestep is different from 0 then we assign for the decoder target data
                    #the reason is that teacher forcing basically can be done when we use a token from the previous timestep to train for the next one
                    self.decoderTarget[line, timestep-1, self.targetDict[token]] = 1.
        return [self.encoderInput, self.decoderInput, self.decoderTarget, self.encSeqLen, self.decSeqLen]
    #here we make the deep learning model of the bot
    #batch_size, epochs and dimensionality can be changed and they will give different results
    #the epochs define how many times we will "feed" the algorithm a full dataset
    #the batch size defines the size of the splits of data we will pass to the algorithm, since we can't pass an entire datase
    def makeModel(self, dimensionality = 256, epochs = 5000, batch_size = 10):
        #we make the matrices
        self.makeMatrices()
        #the input layer will define a matrix for holding the one-hot vectors
        encoderInputs = Input(shape=(None, len(self.inputTokens)))
        #the LSTM layer will be needed, since our seq2seq model works on the basis of predictions
        #this reccurent neural network layer is good for dealing with predictions and processing series of data
        encoderLSTM = LSTM(dimensionality, return_state = True)
        #we make the state data for the algorithm
        encoderOutputs, stateHidden, stateCell = encoderLSTM(encoderInputs)
        encoderStates = [stateHidden, stateCell]
        #the decoder mdel is pretty close to the encoder model in this case, but here we will pass in the state data with the decoder inputs
        self.decoderInputs = Input(shape=(None, len(self.targetTokens)))
        self.decoderLSTM = LSTM(dimensionality, return_sequences = True, return_state = True)
        decoderOutputs, decoderStateHidden, decoderStateCell = self.decoderLSTM(self.decoderInputs, initial_state = encoderStates)
        #the dense layer, also called the Fully-connected layer will be because that is the layer where each neuron is connected to the neurons in the next layer
        #we use it for outputting a prediction
        self.decoderDense = Dense(len(self.targetTokens), activation = 'softmax')
        decoderOutputs = self.decoderDense(decoderOutputs)
        #we make our training model
        trainingModel = Model([encoderInputs, self.decoderInputs], decoderOutputs)
        #we compile it
        trainingModel.compile(optimizer = 'rmsprop', loss='categorical_crossentropy', metrics=['accuracy'], sample_weight_mode='temporal')
        #here we train it
        trainingModel.fit([self.encoderInput, self.decoderInput], self.decoderTarget, batch_size = batch_size, epochs = epochs, validation_split = 0.2)
        #after the training has been done, we save it
        trainingModel.save('model.h5')

        return [self.decoderLSTM, self.decoderDense, self.decoderInputs]
    #to handle an input that the model has not met before we will need a model that decodes step by step
    #that is because our model only works when the target sequence is known
    #and since it only works when the target sequence is known, we will have to build a seq2se1 model in individual pieces
    def testModel(self, latent_dim = 256):
        #we make the model
        self.makeModel()
        #we load the model
        trainingModel = load_model('model.h5')
        #we get the inputs for the encoder 
        encoderInputs = trainingModel.input[0]
        #we get the states from layer 3
        encoderOutputs, stateHiddenEncoder, stateCellEncoder = trainingModel.layers[2].output
        encoderStates = [stateHiddenEncoder, stateCellEncoder]
        #we make our encoder model
        self.encoderModel = Model(encoderInputs, encoderStates)
        #as we do not in fact know what hidden state we will get, we wioll need to create placeholders for the input states of the decoder
        decoderStateInputHidden = Input(shape=(latent_dim,))
        decoderStateInputCell = Input(shape=(latent_dim,))
        decoderStatesInputs = [decoderStateInputHidden, decoderStateInputCell]
        #we will need new states and outputs for the decoder
        #we are using the decoder LSTM and Dense layer that we created earlier
        decoderOutputs, stateHidden, stateCell = self.decoderLSTM(self.decoderInputs, initial_state = decoderStatesInputs)
        decoderStates = [stateHidden, stateCell]
        decoderOutputs = self.decoderDense(decoderOutputs)
        #we set up the decoder model with the decoder input layer, the final states from the encoder, the decoder outputs from the dense layer and the decoder output states - this is the memory from one word to next during the network
        self.decoderModel = Model([self.decoderInputs]+decoderStatesInputs, [decoderOutputs] + decoderStates)
        self.flag = True
        return[self.encoderModel, self.decoderModel]
    #here we can test our model with decoding a passed one-hot vector
    def decode(self, inp):
        #we test the call the above method only if the model has not yet been created
        if not self.flag:
            self.testModel()
        #getting the output states to pass into the decoder
        statesValue = self.encoderModel.predict(inp)
        #generating an empty target sequence
        targetSeq = np.zeros((1,1,len(self.targetTokens)))
        #the first token of the target sequence is set with the last token
        targetSeq[0,0,self.targetDict['<START>']] = 1.
        decoded = ''
        stop = False
        while not stop:
            #predicting output tokens
            outputTokens, hiddenState, cellState = self.decoderModel.predict([targetSeq]+statesValue)
            #choosing the token with the highest probability
            tokenIndex = np.argmax(outputTokens[0,-1,:])
            token = self.inv_targetDict[tokenIndex]
            decoded += token + ' '
            #if we hit the max lenght of a sequence or we have found the stop token we stop the loop
            if token == '<END>' or len(decoded) > self.decSeqLen :
                stop = True
            #we update the target sequence
            targetSeq = np.zeros((1,1,len(self.targetTokens)))
            targetSeq[0,0,tokenIndex] = 1.
            #we update the states
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
    #we prepare the bot for deployment : by calling testModel(), everything that needs to be initialized for the chatbot will be initialized
    def prepare(self):
        self.utils.testModel()
    #a method to convert the given user input to a matrix
    def strToMatrix(self, userInput):
        tokens = re.findall(r"[\w']+|[^\s\w]", userInput)
        userInputMatrix = np.zeros((1, self.utils.encSeqLen, len(self.utils.inputTokens)),dtype = 'float32')
        for timestep, token in enumerate(tokens):
            #if the word is in our vocabulary we put 1 in the matrix
            if token in self.utils.inputDict :
                userInputMatrix[0,timestep,self.utils.inputDict[token]] = 1.
        return userInputMatrix
    #we respond based on the user input
    def respond(self, userInput):
        inputMatrix = self.strToMatrix(userInput)
        botResponse = self.utils.decode(inputMatrix)
        return botResponse


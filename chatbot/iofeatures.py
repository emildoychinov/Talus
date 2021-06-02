import sqnc
def makeFeatures():
    print(type(sqnc.makeSequences()[2]))
    inputTkns, outputTokens = sqnc.makeSequences()[2], sqnc.makeSequences()[3]
    inputFeatures = dict([(token, i) for i, token in enumerate(inputTkns)])
    outputFeatures = dict([(token, i) for i, token in enumerate(outputTkns)])
    inv_inputFeatures = {i : token for i, token in inputFeatures.items()}
    inv_outputFeatures = {i : token for i, token in outputFeatures.items()}
    return inputFeatures, outputFeatures, inv_inputFeatures, inv_outputFeatures

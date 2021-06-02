from cleanup import cleanUp
import re
def makeSequences():
    pairs = cleanUp()
    inputSqc = []
    outputSqc = []
    inputTkns = set()
    outputTkns = set()
    for pair in pairs[:2000]:
        inpt, outpt = pair[0], pair[1]
        inputSqc.append(inpt)
        outpt = ' '.join(re.findall('[\w]+|[^\s\w]', outpt))
        outpt = '<START>' + outpt + '<END>'
        outputSqc.append(outpt)
        for word in re.findall('[\w]+|[^\s\w]', inpt):
            if word not in inputTkns : inputTkns.add(word)
        for word in outpt.split():
            if word not in outputTkns : outputTkns.add(word)
    return inputSqc, outputSqc, sorted(list(inputTkns)), sorted(list(outputTkns)), len(inputTkns), len(outputTkns)

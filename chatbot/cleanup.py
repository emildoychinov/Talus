import re
def cleanUp() :
    with open('input.txt', 'r', encoding = 'utf-8') as f : humanDialog = f.read().split('\n')
    with open('output.txt', 'r', encoding = 'utf-8') as f : botDialog = f.read().split('\n')
    humanDialog = [re.sub(r'\[\w+\]','hi',hd) for hd in humanDialog]
    humanDialog = [' '.join(re.findall(r'\w+', hd)) for hd in humanDialog]
    botDialog = [re.sub(r'\[\w+\]','hi',bd) for bd in botDialog]
    botDialog = [' '.join(re.findall(r'\w+', bd)) for bd in botDialog]
    return list(zip(humanDialog, botDialog))

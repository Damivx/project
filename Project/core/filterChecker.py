from core.checker import checker

def filterChecker(url, params, headers, GET, delay, occurences, timeout, encoding):
    #initializes variables
    positions = occurences.keys()#extracts keys in the occurence and stores them in positions 
    sortedEfficiencies = {}#creates an empty dictionary to store efficiencies sorted by positions
    environments = set(['<', '>'])# adding < > to environments anyway because they can be used in all contexts
    #iterates through each position in positions and creates a dictionary for each one
    for i in range(len(positions)):
        sortedEfficiencies[i] = {}
    #iterates over the occurences to add a 'score' dictionary and determine the context
    for i in occurences:
        occurences[i]['score'] = {}
        context = occurences[i]['context']
        if context == 'comment':
            environments.add('-->')
        elif context == 'script':
            environments.add(occurences[i]['details']['quote'])
            environments.add('</scRipT/>')
        elif context == 'attribute':
            if occurences[i]['details']['type'] == 'value':
                if occurences[i]['details']['name'] == 'srcdoc':  # srcdoc attribute accepts html data with html entity encoding
                    environments.add('&lt;')  # so let's add the html entity
                    environments.add('&gt;')  # encoded versions of < and >
            if occurences[i]['details']['quote']:
                environments.add(occurences[i]['details']['quote'])
    for environment in environments:
        if environment:
            efficiencies = checker(
                url, params, headers, GET, delay, environment, positions, timeout, encoding)
            efficiencies.extend([0] * (len(occurences) - len(efficiencies)))
            for occurence, efficiency in zip(occurences, efficiencies):
                occurences[occurence]['score'][environment] = efficiency
    return occurences
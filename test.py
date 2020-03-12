import string


def transition_table(pattern:string):
    result = []
    alphabet = set()
    for a in pattern:
        alphabet.add(a)
    for q in range(0, len(pattern) + 1):
        result.append({})
        for a in alphabet:
            k = min(len(pattern) + 1, q + 2)
            found = False
            while not found:
                k = k - 1
                suffix = pattern[:q] + a
                prefix = pattern[:k]
                if prefix == '':
                    found = True
                for i in range(q+1):
                    if suffix[i:] == prefix:
                        found = True
                        break
            result[q][a] = k
    return result

def finite_automaton_pattern_matching(text:string, pattern:string):
    q = 0
    delta = transition_table(pattern)
    result = []
    for s in range(0, len(text)):
        if text[s] in delta[q]:
            q = delta[q][text[s]]
            if q == len(delta) - 1:
                result.append(s + 1 - q)
        else:
            q=0
    return result

pattern = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab"
text = "qwertyuiopwertyuio"

print(finite_automaton_pattern_matching(text, pattern))

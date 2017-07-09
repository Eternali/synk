import difflib

indices = []
diffs = []


"""

def largest_substring(strings):
    substr = ""
    count = 0
    if len(strings) > 1 and len(strings[0]):
        for i in range(len(strings[0])):
            for j in range(len(strings[0]) - i + 1):
                print("\r" + str(count), end='')
                if j > len(substr) and strings[0][i:i + j] != ["\a" for a in range(j)] and all(strings[0][i:i + j] in s for s in strings):
                    substr = strings[0][i:i + j]
                    # print(substr)
                count += 1
    return substr


def calc_diffs(old, new):
    ls = largest_substring([old, new])
    # print(ls)
    if len(ls):
        start, end = new.index(ls), new.index(ls) + len(ls)
        indices.append([start, end])
        diffs.append([old.index(ls), old.index(ls) + len(ls)])
        newl = list(new)
        newl[start:end] = ["\a" for n in range(end - start)]
        new = ''.join(newl)
        calc_diffs(old, new)
    else:
        i = 0
        while i < len(new):
            if new[i] != "\a":
                lastNone = new[i + 1:].index("\a") + i + 1
                indices.append(''.join(new[i:lastNone]))
                diffs.append(i)
                i = lastNone
            i += 1
    print(old)
    print(new)

"""


def get_local_changes(file, cached_file):
    global indices, diffs
    # it is assumed there is a difference between the file and the
    # cached_file
    with open(file, 'r') as nf:
        nlines = "".join(nf.readlines())
    with open(cached_file, 'r') as cf:
        clines = "".join(cf.readlines())

    # print(clines)
    # print(nlines)
    # return [nlines, clines]
    # calc_diffs(clines, nlines)
    '''
    s = difflib.SequenceMatcher(None, clines, nlines)
    for block in s.get_matching_blocks():
        indices.append([block.a, block.b])
        diffs.append(["", block.size])

    offset = 0
    tmpdiff = [None, None]
    diff = indices[0][1] - indices[0][0]
    if diff > 0:
        tmpdiff[0] = "+"
        tmpdiff[1] = nlines[0:indices[0][1]]
    elif diff < 0:
        tmpdiff[0] = "-"
        tmpdiff[1] = clines[0:indices[0][0]]
    offset += diff
    for i in range(0, (len(s.get_matching_blocks()) - 2) * 2, 2):
        indices.insert(i + 1, [indices[i][0] +
                       diffs[i][1], indices[i][1] + diffs[i][1]])
        diffs.insert(i + 1, [None, None])
        if indices[i + 2][1] - indices[i + 2][0] - offset > 0:
            diffs[i + 1][0] = "+"
            diffs[i + 1][1] = nlines[indices[i + 2][0] + offset:indices[i + 2][1]]
            offset += indices[i + 2][1] - indices[i + 2][0]
        elif indices[i + 2][1] - indices[i + 2][0] - offset < 0:
            diffs[i + 1][0] = "-"
            diffs[i + 1][1] = clines[indices[i + 2][1] - offset:indices[i + 2][0]]
            offset += indices[i + 2][1] - indices[i + 2][0]
        else:
            diffs[i + 1][0] = ""
    if None not in tmpdiff:
        indices.insert(0, [0, 0])
        diffs.insert(0, tmpdiff)
'''

    # print(indices)
    # print(diffs)

    sames = []
    s = difflib.SequenceMatcher(None, clines, nlines)
    for block in s.get_matching_blocks():
        sames.append([block.a, block.b, block.size])

    changes = []
    offset = 0

    # sames are of the form: [indexA, indexB, size]
    # changes are of the form: [indexAStart, indexBStart, '-'/'+'/'', stringChange]
    for i in range(len(sames) - 1):
        if sames[i][1] - sames[i][0] - offset > 0:
            changes.append([sames[i][0] + sames[i][2], sames[i][1] + sames[i][2], '+', ])
        elif sames[i][1] - sames[i][0] - offset < 0:
            changes.append([, , '-', ])
        else:
            changes.append([, , '', ])

    """
    for i in range(0, (len(s.get_matching_blocks()) - 1) * 2, 2):
        print(s.get_matching_blocks())
        if indices[i][1] - indices[i][0] - offset > 0:
            indices.insert(i + 1, [indices[i - 2][0] + diffs[i - 2][1], indices[i - 2][1] + diffs[i - 2][1]] if i - 2 >= 0 else [0, 0])
            diffs.insert(i + 1, ["+", nlines[indices[i][0] + offset:indices[i][1]]])
            offset = indices[i][1] - indices[i][0]
        elif indices[i][1] - indices[i][0] - offset < 0:
            indices.insert(i + 1, [indices[i - 2][0] + diffs[i - 2][1], indices[i - 2][1] + diffs[i - 2][1]] if i - 2 >= 0 else [0, 0])
            diffs.insert(i + 1, ["-", clines[indices[i][1] - offset:indices[i][0]]])
            offset = indices[i][1] - indices[i][0]
"""


get_local_changes("/home/fa11en/.config/sublime-text-3/Installed Packages/synk-pre/synk2cp2.py",
                  "/home/fa11en/.config/sublime-text-3/Installed Packages/synk-pre/synk2cp.py")
print(indices)
print(diffs)


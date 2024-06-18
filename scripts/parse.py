import collections
import nltk
import bs4
import re
import os

def split(row):
    pair = row.split(maxsplit=1)
    key  = pair[0][:-1].lower()
    val  = pair[1]

    return key, val


def text(file):
    """
    Processes a file into a structured format,
    extracting key information from the header
    (fest, year, place, dates) and returning a
    dictionary containing these values alongside
    a list of names from the body.
    """
    data  = re.split('\n', file)
    start = data.index('')

    # Split the data into header and body
    head  = data[:start]
    body  = data[start + 1:]
    names = [r for r in body if r]

    pairs = {
        k:v for k,v in
        map(split, head)
    }

    f, p, y, d =         \
        'fest', 'place', \
        'year', 'dates'

    # Extract values
    fest  = pairs[f]
    year  = pairs[y]
    place = pairs[p]
    dates = re.sub(
        r', \d{4}',
        '', pairs[d]
    )

    wrap  = {
        f: fest,
        y: int(year),
        p: (fest, p,       place),
        d: (fest, d, year, dates)
    }

    return wrap, names


def count(lst):
    """
    Counts the frequency of each element and
    returns the most common one.
    """
    nums = collections.Counter(lst)
    top  = nums.most_common(1)

    return top[0][0]


def trim(lst):
    # Trims common prefixes and suffixes
    rev = [s[::-1] for s in lst]
    pre = len(os.path.commonprefix(lst))
    pst = len(os.path.commonprefix(rev))

    return [
        s[pre:len(s) - pst]
        for s in lst
    ]


def html(data):
    """
    Parses HTML data to identify the festival
    and year, and returns this information
    along with a list of trimmed artist names.
    """
    soup = bs4.BeautifulSoup(
        data, 'html.parser'
    )

    tags = []
    noun = []
    nums = []

    for child in soup.descendants:
        # Skip non-leaf nodes
        if hasattr(child, 'children'):
            continue

        parent = child.parent

        if parent.has_attr('class'):
            css = ' '.join(parent['class'])
            tags.append((parent.name, css))

        # Skip non-text elements and non-word text
        if not isinstance(child, bs4.NavigableString):
            continue

        if not re.match('[\w\s]+$', child):
            continue

        # Tokenize the text and extract nouns and numbers
        lex = child.lower().split()
        tag = nltk.pos_tag(lex)

        let = [
            x for x,y in tag
            if x != 'lineup'
            and 'NN' in y
        ]

        num = [
            x for x,y in tag
            if re.match('\d{4}$', x)
        ]

        noun.extend(let)
        nums.extend(num)

    # Find the most common type of leaf node
    tag, css = count(tags)
    name = soup.find_all(tag, class_=css)

    # Extract artist names
    sets = [
        str(s.string or s.img['alt'])
        for s in name
    ]

    # Use the most common noun and number
    wrap = {
        'fest' :     count(noun),
        'year' : int(count(nums))
    }

    return wrap, trim(sets)

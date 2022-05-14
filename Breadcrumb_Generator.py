def generate_short(element: str):
    words = ["the","of","in","from","by","with","and", "or", "for", "to", "at", "a"]
    ls = element.split('-')
    ls = [st.lower() for st in ls]
    ls = [st[0].upper() for st in ls if st not in words]
    return ''.join(ls)


def generate_span(element: str):
    # in case it's the first element
    if element == 'HOME':
        return '<span class="active">HOME</span>'

    # shortening elements greater than 30 chars
    if len(element) > 30:
        element = generate_short(element)
    else:
        # should parse that string
        element = element.upper()
        element = element.replace('-', ' ')

    return '<span class="active">' + element + '</span>'


def generate_a(url_array: list, i: int):
    # in case it's the first element
    if i == 0:
        return '<a href="/">HOME</a>'

    short = url_array[i].upper()
    # shortening elements greater than 30 chars
    if len(url_array[i]) > 30:
        short = generate_short(url_array[i])
    if i == 1:
        result = url_array[1]
    else:
        result = '/'.join(url_array[1:i+1])
    ls = short.split('-')
    short = ' '.join(ls)
    return '<a href="/' + result + '/">' + short + '</a>'


def generate_bc(url: str, separator: str):
    # eliminating parameters and anchors and the http protocol
    if '#' in url:
        anchor_index = url.index('#')
        url = url[:anchor_index]
    if '?' in url:
        parameter_index = url.index('?')
        url = url[:parameter_index]
    if url[:8] == 'https://':
        url = url[8:]
    if url[:7] == 'http://':
        url = url[7:]
    if url[-1] == '/':
        url = url[:-1]

    # splitting the url based on the slash /
    url_array = url.split('/')
    url_array[0] = 'HOME'

    # in case it's only a website
    if len(url_array) == 1:
        return generate_span(url_array[0])

    # deleting index sense it's irrelevant
    if 'index' in url_array[-1]:
        del url_array[-1]

    # removing the last element's file type
    if '.' in url_array[-1]:
        point_index = url_array[-1].index('.')
        url_array[-1] = url_array[-1][:point_index]

    # creating the final array of results
    final = [generate_a(url_array, i) for i in range(len(url_array)-1)]
    final.append(generate_span(url_array[-1]))
    return separator.join(final)


def main():
    print(generate_bc('google.ca/files/with-bed-bladder-cauterization-and-surfer/files/the-kamehameha-diplomatic-bioengineering/index.html#bottom?order=desc&filter=adult', ' : '))


if __name__ == '__main__':
    main()

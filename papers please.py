import operator


class Inspector:
    countries = ['Arstotzka', 'Antegria', 'Impor', 'Kolechia', 'Obristan', 'Republia', 'United Federation']
    allow_list = []  # list of the countries allowed to enter
    wanted_name = ''  # names of wanted criminals
    vaccinations = {}  # a list that contains vaccine name and a list of countries need to get it
    documents = {'passport': [], 'ID_card': [], 'access_permit': [], 'work_pass': []}
    documents.update({'grant_of_asylum': [], 'certificate_of_vaccination': [], 'diplomatic_authorization': []})
    bullet_sentences = []
    # a dictionary that contains type of documents and which groups need them

    @classmethod
    def require_document(cls, words: list):
        is_more = 'less' if 'longer' in words else 'more'
        if words[:2] == ['Citizens', 'of']:
            words = words[2:]
            require_index = words.index('require')
            countries = words[:require_index]
        else:  # include anything that is not 'citizens of'
            require_index = words.index('require')
            if words[0] == 'Foreigners':
                countries = cls.countries[:]
                countries.remove('Arstotzka')
            if words[0] == 'Workers':
                countries = [words[0]]
            else:
                countries = cls.countries[:]
        # now we find the document that we should add or removed
        document = '_'.join(words[require_index + 1:])
        if is_more == 'more':
            cls.documents[document] += countries
            cls.documents[document] = list(dict.fromkeys(cls.documents[document]))
        else:
            cls.documents[document] = [x for x in cls.documents[document] if x not in countries]

    @classmethod
    def vaccination_bullet(cls, words, vax_names: list, vac_addition: str):
        if words[:2] == ['Citizens', 'of']:
            del words[:2]
        require_index = words.index('require')  # the index of the end of the countries list
        if words[0].lower() == 'entrants':
            countries = cls.countries[:]
        elif words[0].lower() == 'foreigners':
            countries = cls.countries[:]
            countries.remove('Arstotzka')
        else:
            countries = words[:require_index]  # countries equal here to the correct value
        for vax in vax_names:
            if vax not in cls.vaccinations:
                cls.vaccinations[vax] = []
            if vac_addition == 'more':
                cls.vaccinations[vax] += countries
                cls.vaccinations[vax] = list(dict.fromkeys(cls.vaccinations[vax]))
            else:
                cls.vaccinations[vax] = [x for x in cls.vaccinations[vax] if x not in countries]
        if 'hepatitis' in cls.vaccinations.keys():
            if 'B' in cls.vaccinations.keys():
                cls.vaccinations['hepatitis'] += cls.vaccinations['B']
                del cls.vaccinations['B']
                cls.vaccinations['hepatitis B'] = cls.vaccinations.pop('hepatitis')
        if 'yellow' in cls.vaccinations.keys():
            if 'fever' in cls.vaccinations.keys():
                cls.vaccinations['yellow'] += cls.vaccinations['fever']
                del  cls.vaccinations['fever']
                cls.vaccinations['yellow fever'] = cls.vaccinations.pop('yellow')


    @classmethod
    def allow_or_deny(cls, words: list):
        countries = words[3:]
        for i in range(len(countries)):
            if words[0] == 'Allow':
                if words[1] == 'entrants':
                    cls.allow_list = countries
                elif countries[i] not in cls.allow_list:
                    cls.allow_list.append(countries[i])
            else:
                if words[1] == 'entrants':
                    cls.allow_list = []
                if countries[i] in cls.allow_list:
                    cls.allow_list.remove(countries[i])

    @classmethod
    def receive_bulletin(cls, bulletin: str):
        cls.wanted_name = ''
        sentences = bulletin.split('\n')
        print(f'sentences are: {sentences}')
        cls.bullet_sentences.append(sentences)
        for sentence in sentences:
            words = sentence.split(' ')
            words = [word.strip() for word in words if word.strip() != '']
            i = 0  # eliminating commas
            while i < len(words):
                if words[i][-1] == ',':
                    words[i] = words[i][:-1]
                if words[i].strip() == '':
                    del words[i]
                    i -= 1
                i += 1
            if words[0] == 'Allow' or words[0] == 'Deny':
                cls.allow_or_deny(words)
                continue
            elif words[0] == 'Wanted':
                cls.wanted_name = words[-2] + ' ' + words[-1]  # last two words
                continue
            elif 'vaccination' in words:
                vax_index = words.index('vaccination')
                require_index = words.index('require')
                vax_addition = 'less' if 'longer' in words else 'more'
                vax_names = words[require_index+1:vax_index]  # since the name is before the word 'vaccination'
                cls.vaccination_bullet(words, vax_names, vax_addition)
                continue
            else:
                cls.require_document(words)

    @classmethod
    def get_name(cls, entrant: dict):
        name = ''
        for doc in entrant.keys():
            for attribute in entrant[doc].keys():
                if attribute == 'NAME':
                    name = entrant[doc]['NAME'].split(',')
                    name = name[1] + ' ' + name[0]
        return name

    @classmethod
    def check_expiration(cls, entrant: dict):
        for doc in entrant.keys():
            for attribute in entrant[doc]:
                if attribute == 'EXP':
                    exp_date = entrant[doc][attribute].split('.')
                    exp_date = [int(item) for item in exp_date]
                    if exp_date[0] < 1982 or (exp_date[0] == 1982 and exp_date[1] < 11) or (
                            exp_date[0] == 1982 and exp_date[1] == 11 and exp_date[2] < 22):
                        return doc.replace('_', ' ')
        return False

    @classmethod
    def check_matched_docs(cls, entrant: dict):
        # returns True if all match or the mismatched attribute's name
        ls = []
        for doc in entrant.keys():
            for attribute in entrant[doc].keys():
                ls.append([attribute, entrant[doc][attribute]])
        # now ls contains all the attributes of all the docs together
        ls = sorted(ls, key=operator.itemgetter(0))
        for i in range(len(ls) - 1):
            if ls[i][0] == ls[i+1][0]:  # same attribute over different doc
                if ls[i][1] != ls[i+1][1]:
                    if ls[i][0] in ['NAME', 'NATION', 'DOB', 'ID#']:
                        translate = {'NATION': 'nationality', 'NAME': 'name', 'DOB': 'date of birth', 'ID#': 'ID number'}
                        return translate[ls[i][0]]
                    elif ls[i][0] != 'EXP':
                        return ls[i][0]
        return False

    @classmethod
    def check_vaccines(cls, entrant: dict, nation: str):
        vaccines = []
        if 'certificate_of_vaccination' in entrant.keys():
            vaccines = entrant['certificate_of_vaccination']['VACCINES'].split(',')
            vaccines = [x.strip() for x in vaccines]
        for vax in cls.vaccinations:
            if nation in cls.vaccinations[vax]:
                if 'certificate_of_vaccination' not in entrant.keys():
                    return 'missing certificate_of_vaccination'
                if vax not in vaccines:
                    return 'not vaccinated'
        return 'vaccinated'


    @classmethod
    def inspect(cls, entrant: dict):
        print(f'entrant is: {entrant}\n')
        print(f'\nvaccines are: {cls.vaccinations}')
        if not entrant.keys():
            return 'Entry denied: missing required passport.'
        # now we convert each key to it's dictionary format
        for key in entrant.keys():
            entrant[key] = entrant[key].split('\n')
            entrant[key] = [x.split(':') for x in entrant[key]]
            entrant[key] = {item[0].strip(): item[1].strip() for item in entrant[key]}
        # now the entrants should be in a good format
        name = cls.get_name(entrant)
        if name.strip() in cls.wanted_name:
            return 'Detainment: Entrant is a wanted criminal.'
        is_matched_docs = cls.check_matched_docs(entrant)
        if is_matched_docs != 'EXP' and is_matched_docs != False:  # case there is a mismatch
            return f'Detainment: {is_matched_docs} mismatch.'
        is_expired = cls.check_expiration(entrant)
        if is_expired:  # it's equal to the doc name if it is expired or else false
            return f'Entry denied: {is_expired} expired.'
        nation = ''
        for doc in cls.documents:
            if doc in entrant.keys():
                if 'NATION' in entrant[doc]:
                    nation = entrant[doc]['NATION']
                    if nation.lower().strip() in 'united federation' and 'United' in cls.allow_list:
                        break
                    if nation not in cls.allow_list:
                        return f'Entry denied: citizen of banned nation.'
        if 'access_permit' in entrant.keys() and 'PURPOSE' in entrant['access_permit'].keys() and entrant['access_permit']['PURPOSE'] == 'WORK':
                if 'Workers' in cls.documents['work_pass'] and 'work_pass' not in entrant.keys():
                    return 'Entry denied: missing required work pass.'
        if nation == '':
            return 'Entry denied: missing required passport.'
        # now we check that all documents exists
        if 'diplomatic_authorization' in entrant.keys():
            if 'ACCESS' not in entrant['diplomatic_authorization'].keys() or 'Arstotzka' not in entrant['diplomatic_authorization']['ACCESS']:
                return 'Entry denied: invalid diplomatic authorization.'
        for doc in cls.documents:
            if nation in cls.documents[doc]:
                if doc == 'access_permit' and 'grant_of_asylum' in entrant.keys():
                    continue
                elif doc == 'access_permit' and 'diplomatic_authorization' in entrant.keys():
                    if 'Arstotzka' in entrant['diplomatic_authorization']['ACCESS']:
                        continue
                elif doc == 'access_permit' and nation == 'Arstotzka':
                    continue
                if doc not in entrant.keys():
                    doc = doc.replace('_', ' ')
                    return f'Entry denied: missing required {doc}.'

        vax_result = cls.check_vaccines(entrant, nation)
        if vax_result == 'not vaccinated':
            return 'Entry denied: missing required vaccination.'
        if vax_result == 'missing certificate_of_vaccination':
            return 'Entry denied: missing required certificate of vaccination.'
        # from here all tests have work and entrant should pass
        print(f'\n{cls.bullet_sentences}\n')
        if nation == 'Arstotzka':
            return 'Glory to Arstotzka.'
        else:
            return 'Cause no trouble.'


def main():
    inspector = Inspector()
    bulletin = """Entrants require passport
    Allow citizens of Arstotzka, Obristan"""
    inspector.receive_bulletin(bulletin)
    guyovich = {'passport': 'ID#: 8B19F-R34DV\nNATION: Republia\nNAME: Muller, Maciej\nDOB: 1956.10.21\nSEX: M\nISS: Orvech Vonor\nEXP: 1986.10.25', 'certificate_of_vaccination': 'NAME: Muller, Maciej\nID#: 8B19F-R34DV\nVACCINES: tetanus, hepatitis B, cowpox, rubella', 'access_permit': 'NAME: Muller, Maciej\nNATION: Republia\nID#: 8B19F-R34DV\nPURPOSE: WORK\nDURATION: 1 MONTH\nHEIGHT: 153cm\nWEIGHT: 48kg\nEXP: 1989.08.17'}
    inspector.inspect(guyovich)
    print(inspector.documents)


if __name__ == '__main__':
    main()

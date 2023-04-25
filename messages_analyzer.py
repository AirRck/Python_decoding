#Jakub Kaminski
import re

class PhoneFinder:
    regex = re.compile("(\\d{9})|(\\d{3}-\\d{3}-\\d{3})")

    def find_all(self, text):
        res = []
        group_array = PhoneFinder.regex.findall(text);
        for groups in group_array:
            if groups[0] == "":
                res.append(groups[1])
            else:
                res.append(groups[0])
        return res

class DateFinder:
    regex = re.compile("(\\d{2}/\\d{2}/\\d{4})|(\\d{4}/\\d{2}/\\d{2})")

    def find_all(self, text):
        res = []
        group_array = DateFinder.regex.findall(text);
        for groups in group_array:
            if groups[0] == "":
                res.append(groups[1])
            else:
                res.append(groups[0])
        return res

class MessagesAnalyzer:
    cryptoRegex = re.compile('^\\([^)]+\\)')
    hourRegex = re.compile('\\d\\d:\\d\\d')
    messageNameContent = re.compile('^(\\S+ \\S+) (.+)$')
    capitalLetters = re.compile('[A-Z]+')
    replaceMap = re.compile('^(#[{[]([^ :,]+\\s*:\\s*[^ :}\\],]+\\s*(,\\s*)?)+[}\\]])\\s*(.+)$')
    WTODiffs = [(ord("T") - ord("W")) % 26, (ord("O") - ord("W")) % 26]

    phoneSearcher = PhoneFinder()
    dateFinder = DateFinder()

    def __init__(self, message):
        """
        :type message: str
        """
        self.msgs = {}
        for line in message.splitlines():
            self.__decodeLine(line)

    def __decodeLine(self, line):
        """
        :type line: str
        """

        match = MessagesAnalyzer.messageNameContent.match(line)
        name = match.groups()[0]
        content = match.groups()[1]

        if name not in self.msgs:
            self.msgs[name] = []

        self.msgs[name].append(self.__decode_content(content.strip()))
#   # QABC
    # QBB
    # Q -> C. QA -> D
    # A->BB B->CCC
    # BBBC
    def __decode_content(self, content):
        if content[0] == "#":
            dict_content_match = MessagesAnalyzer.replaceMap.match(content)
            dict_str = dict_content_match.groups()[0]
            content = dict_content_match.groups()[3].strip()
            dict_str = re.sub(r"\s", '', dict_str)
            dict_str = dict_str[2:(len(dict_str) - 1)]
            key_value_pairs = dict_str.split(",")
            replacements = []
            for keyValue in key_value_pairs:
                key_value_array = keyValue.split(":")
                replacements.append((key_value_array[0], key_value_array[1]))

            ms = content.split(" ")

            for i in range(0, len(ms)):
                for repl in replacements:
                    if ms[i] == repl[0]:
                        ms[i] = repl[1]
                        break

            return " ".join(ms)
        else:
            k = self.__findK(content)
            contentArray = list(content)
            for i in range(0, len(contentArray)):
                if ord("A") <= ord(contentArray[i]) <= ord("Z"):
                    contentArray[i] = chr((ord(contentArray[i]) - ord("A") - k + 26) % 26 + ord("A"))

                elif ord("0") <= ord(contentArray[i]) <= ord("9"):
                    contentArray[i] = chr((ord(contentArray[i]) - ord("0") - k + 10) % 10 + ord("0"))
            return "".join(contentArray)


    def __findK(self, content):
        for i in range(2, len(content)): # W   U
            if ((ord(content[i - 1]) - ord(content[i - 2])) % 26 == MessagesAnalyzer.WTODiffs[0]
                    and (ord(content[i]) - ord(content[i - 2])) % 26 == MessagesAnalyzer.WTODiffs[1]):
                return (ord(content[i - 2]) - ord("W") + 26) % 26
        print("nie znaleziono k")
        return -1

    def show_messages(self):
        for key in sorted(self.msgs.keys()):
            print(key + ":")
            for msg in self.msgs[key]:
                print(msg)

    def phone_numbers(self):
        res = []
        for key in sorted(self.msgs.keys()):
            for msg in self.msgs[key]:
                numbersFound = MessagesAnalyzer.phoneSearcher.find_all(msg)
                for number in numbersFound:
                    res.append((key, number))

        return res

    def hours(self):
        res = []
        for key in sorted(self.msgs.keys()):
            for msg in self.msgs[key]:
                hoursFound = self.hourRegex.findall(msg)
                for hour in hoursFound:
                    res.append((key, hour))

        return res

    def cryptonyms(self):
        res = []
        for key in sorted(self.msgs.keys()):
            for msg in self.msgs[key]:
                cryptosFound = self.cryptoRegex.findall(msg)
                for crypto in cryptosFound:
                    res.append((key, crypto))

        return res

    def dates(self):
        res = []
        for key in sorted(self.msgs.keys()):
            for msg in self.msgs[key]:
                dateFound = MessagesAnalyzer.dateFinder.find_all(msg)
                for date in dateFound:
                    res.append((key, date))

        return res

# "asdasd asdasdasdasda" => ["asdasd", "qweqweasd"]
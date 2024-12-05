import string

class HtmlTagAFD:
    def __init__(self):
        self.final_state = 35
        self.transitions = {
            (1, '<'): 2,
            (2, 's'): 3,
            (3, 'p'): 4,
            (4, 'a'): 5,
            (5, 'n'): 6,
            (6, ' '): 7,
            (7, 'd'): 8,
            (8, 'a'): 9,
            (9, 't'): 10,
            (10, 'a'): 11,
            (11, '-'): 12,
            (12, 'i'): 13,
            (13, 'd'): 14,
            (14, '='): 15,
            (15, '"'): 16,
            (23, '|'): 16,
            (23, '"'): 24,
            (24, '>'): 25,
            (26, '<'): 27,
            (27, '/'): 28,
            (28, 's'): 29,
            (29, 'p'): 30,
            (30, 'a'): 31,
            (31, 'n'): 32,
            (32, '>'): 33,
            (33, ':'): 34,
            (33, ','): 34,
            (33, 'l'): 34,
            (33, 'o'): 34,
            (33, 'a'): 34,
            (34, ':'): 34,
            (34, ','): 34,
            (34, 'l'): 34,
            (34, 'o'): 34,
            (34, 'a'): 34,
            (33, ' '): 1,
            (33, '\n'): 1,
            (33, '\t'): 1,
            (33, '.'): 35,
            (34, ' '): 1,
            (34, '\n'): 1,
            (34, '\t'): 1,
        }

        for char in string.ascii_letters + 'ñ' + string.digits:
            self.transitions[(16, char)] = 17
            self.transitions[(17, char)] = 18
            self.transitions[(18, char)] = 19
            self.transitions[(19, char)] = 20
            self.transitions[(20, char)] = 21
            self.transitions[(21, char)] = 22
            self.transitions[(22, char)] = 23

        for char in string.ascii_letters + 'ñ':
            self.transitions[(25, char)] = 26
            self.transitions[(26, char)] = 26

        self.saved_state = {26, 34, 35}

    def validate_text(self, text):
        current_state = 1
        definitions_found = []
        extracted_text = ""
        line, col = 1, 0
        positions = []

        for char in text:
            col += 1
            if char == '\n':
                line += 1
                col = 0

            transition = (current_state, char)
            if transition in self.transitions:
                current_state = self.transitions[transition]
                if current_state in self.saved_state:
                    extracted_text += char
                if current_state == 27:
                    extracted_text += ' '
                if current_state == 35:
                    extracted_text += ' '
            else:
                if char in [' ', '\n', '\t']:
                    current_state = 1
                else:
                    current_state = 1
                    extracted_text = ""

            if current_state == self.final_state:
                definitions_found.append(extracted_text)
                positions.append((line, col))
                extracted_text = ""
                current_state = 1

        if definitions_found:
            return True, definitions_found, positions
        return False, [], []
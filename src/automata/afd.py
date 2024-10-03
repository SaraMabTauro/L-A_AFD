transitions = {
    1: {'<': 2, ' ': 1, '\n': 1},
    2: {'s': 3},
    3: {'p': 4},
    4: {'a': 5},
    5: {'n': 6},
    6: {' ': 7},
    7: {'d': 8},
    8: {'a': 9},
    9: {'t': 10},
    10: {'a': 11},
    11: {'-': 12},
    12: {'i': 13},
    13: {'d': 14},
    14: {'=': 15},
    15: {'"': 16},
    16: {char: 17 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
    17: {char: 18 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
    18: {char: 19 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
    19: {char: 20 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
    20: {char: 21 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
    21: {char: 22 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
    22: {char: 23 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'},
    23: {'|': 16, '"': 24},
    24: {'>': 25},
    # Estado 25 a 26 permite capturar cualquier contenido dentro del <span>
    25: {char: 26 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,:;!?'},
    # Combinamos las transiciones en un solo estado 26
    26: {char: 26 for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,:;!?'},
}
transitions[26].update({'<': 27})  # Agregamos la transición con '<' para el estado 26

transitions.update({
    27: {'/': 28},
    28: {'s': 29},
    29: {'p': 30},
    30: {'a': 31},
    31: {'n': 32},
    32: {'>': 33},
    33: {':': 34, ' ': 1, '\n': 1, '.': 35},
    34: {' ': 1, '\n': 1},
    35: {}
})

# Función del autómata
def automata_validator(input_string):
    state = 1
    current_value = ""
    captured_values = []
    
    i = 0
    while i < len(input_string):
        char = input_string[i]
        
        # Verificar si la transición existe para el estado actual
        if char in transitions[state]:
            state = transitions[state][char]
            
            # Cuando llegamos al estado 25 empezamos a capturar el contenido del span
            if state == 25:
                current_value = ""
                
            # Cuando estamos en el estado 26, vamos capturando el contenido del span
            if state == 26:
                current_value += char
            
            # Si llegamos al final del span (estado 33), guardamos el valor capturado
            if state == 33:
                captured_values.append(current_value.strip())  # Elimina espacios al inicio y al final
                current_value = ""
            
        elif char in [' ', '\n']:  # Ignorar espacios en blanco y saltos de línea
            i += 1
            continue
        
        else:
            # Si no hay transición válida, el autómata falla
            print(f"Error: no hay transición válida para '{char}' en el estado {state}.")
            return False, []
        
        i += 1

    # Si llegamos al estado final (35), la cadena es aceptada
    if state == 35:
        return True, captured_values
    else:
        return False, captured_values

# Ejemplo de cadena a validar
input_string = """
<span data-id="BxLriBU|DgXmXNM">Dicho</span>
<span data-id="BtDkacL|Bt
FYznp">de</span>
<span data-id="b67JJSq|b6hEWeB|b6iKApr">una</span>
<span data-id="SjUIL8Z|SjwafWr">persona</span>:
<span data-id="Jwhmcap">Hacer</span>
<span data-id="ESraxkH|NWnohQu|NWofhZh">lo</span>
<span data-id="QKLjAgy">necesario</span>
<span data-id="Rp1CuT2|RsVKhBv|RwYmdsn|RxSczPr">para</span>
<span data-id="UkbUarn">que</span>
<span data-id="Qu8oSco">ocurra</span>
<span data-id="1nUry2t">algo</span>.
"""

# Ejecutar el autómata con la cadena de entrada
is_valid, captured_values = automata_validator(input_string)

if is_valid:
    print("Cadena válida. Valores capturados:")
    for value in captured_values:
        print(value)
else:
    print("Cadena inválida.")

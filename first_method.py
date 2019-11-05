import numpy as np
from sympy import *
import re


def validate_input(input_string) -> bool:
    """
    Function to validate input
    :param input_string: string to check
    :return: True if in string are allowed characters False if in string exist not allowed symbol

    >>> validate_input("C6H12O6 -> CH3CH2OH + CO2")
    True

    >>> validate_input("C6H12O6 = CH3CH2OH + CO2")
    False

    >>> validate_input("!? CH0CH23H + CO2")
    False

    """
    re_str = "[1-9A-Z->+]"
    re_compiled = re.compile(re_str)
    condition = re_compiled.sub('', input_string).strip()
    if len(condition) != 0:
        return False
    return True


def check_reaction_side(component):
    """
    Function to divide side of equation to components
    :param component: one side of equation
    :return: components list
    """
    if "+" in component:
        component = component.split("+")
    return component


def get_elements_number(part, dict_template):
    """
    Function to parse number of elements to coefficient dict by element
    :param part: one element from equation
    :param dict_template: dict with structure: {element_name: 0}, for unique elements from
             equation eg., for H20 {"H":0, "O": 0}
    :return: dict with coefficient for each element
    """
    elements_number = dict_template.copy()
    multiplexer = 1
    for index, item in enumerate(part):
        number = ""
        if index == 0 and item.isdigit():
            multiplexer = int(item)
        if item.isalpha():
            shifted_index = index
            while True:
                shifted_index = shifted_index + 1
                if shifted_index > len(part) - 1:
                    break
                if part[shifted_index].isalpha():
                    break
                number = number + part[shifted_index]

            if number == "":
                number = '1'
            if item not in elements_number.keys():
                elements_number[item] = multiplexer * int(number)
            else:
                elements_number[item] = elements_number[item] + (multiplexer * int(number))
    return elements_number


def get_coefficient(components, reaction):
    """
    Function to get coefficient of element from one side
    :param components: elements with number
    :param reaction: reaction equation
    :return: horizontal array of coefficients form one side of reaction
    """
    unique_elements = np.unique([x for x in reaction if x.isalpha()])
    dict_template = {k: 0 for k in unique_elements}
    if isinstance(components, list):
        coefficient_array = np.zeros((len(components), len(unique_elements)))
        for index, element in enumerate(components):
            temp_array = np.array(())
            temp_dict = get_elements_number(element.strip(), dict_template)
            for item in temp_dict.values():
                temp_array = np.append(temp_array, item)
            coefficient_array[index] = temp_array
    else:
        coefficient_array = np.array(())
        numbers_dict = get_elements_number(components.strip(), dict_template)
        for item in numbers_dict.values():
            coefficient_array = np.append(coefficient_array, item)

    return coefficient_array


def get_components(reaction, side_divider="->"):
    """
    Function to split reaction equation and get coefficients of elements
    :param reaction: string, reaction equation
    :param side_divider: string, side divider by default is arrow can be replaced by "=" in callback
    :return: array of coefficients of elements from both sides
    """
    left_side = reaction.split(side_divider)[0]
    rigth_side = reaction.split(side_divider)[-1]

    left_components = check_reaction_side(left_side)
    right_components = check_reaction_side(rigth_side)

    left_coefficient = get_coefficient(left_components, reaction)
    right_coefficient = get_coefficient(right_components, reaction)
    coefficient = np.vstack((left_coefficient, -1 * right_coefficient)).transpose()

    return coefficient


def get_balance(arrays, reaction):
    """
    Mathematical brain to balance reaction
    :param arrays: array of coefficient of elements
    :param reaction: string, reaction equation
    :return: string, balanced reaction
    """
    sym_symbols = list('abcdefghijklmnopqrstuvwxyz')
    equations = []
    used_symbols = {}
    for row in arrays:
        equation = ""
        for row_index, item in enumerate(row):
            if item != 0:
                used_symbols.update({sym_symbols[row_index]: Symbol(sym_symbols[row_index])})
                equation = sympify(f'{equation}{"" if item < 0 else "+"}{item}*{used_symbols[sym_symbols[row_index]]}')
            else:
                continue
        equations.append(equation)

    result = solve(equations, [x for x in used_symbols.values()], particular=True, rational=True)
    to_output = [result[used_symbols[x]] for x in sorted(list(used_symbols.keys()))]

    if not all(item % 1 == 0 for item in to_output):
        not_int_index = [index for index, value in enumerate(to_output) if value % 1 != 0]
        multiplier = []
        for item in not_int_index:
            multiplier.append(int(str(to_output[item]).split("/")[-1].replace(']', "")))

        if len(multiplier) == 1:
            to_output = [x * multiplier[0] for x in to_output]
        else:
            to_output = [x * max(multiplier) for x in to_output]

    output_string = ""
    index = 0
    latch = False
    for item in reaction:
        if item in [">", "+", "="]:
            latch = False
        if item.isalpha() and not latch:
            output_string = output_string + f"{'' if to_output[index] == 1 else int(to_output[index])}{item}"
            index = index + 1
            latch = True
            continue

        output_string = output_string + item

    return output_string


def main(reaction_to_balance):
    """
    Main Function to run balance algorithm
    :param reaction_to_balance: string with reaction to balance
    :return: string, balanced reaction
    """
    if not validate_input(reaction_to_balance):
        raise Exception('Wrong input - some character in string is not allowed')

    components = get_components(reaction_to_balance)
    output_string = get_balance(components, reaction_to_balance)
    return output_string


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    # out = main("C5H12 + O2 -> CO2 + H2O")
    # out = main("Z + HC -> ZC2 + H2")
    # out = main("C2H6 + O2 -> CO2 + H2O")

    out = main('C6H12O6 -> CH3CH2OH + CO2')
    print(out)

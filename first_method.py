import re
import numpy as np
from scipy.linalg import solve

def validate_input(input_string) -> bool:
    """
    :param input: string to check 
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
    if "+" in component:
        component = component.split("+")
    if "-" in component:
        component.split("-")

    return component


def get_elements_number(part, dict_template):
    elements_number = dict_template.copy()
    for index, item in enumerate(part):
        number = ""
        multiplexer = 1

        if index == 0 and item.isdigit():
            multiplexer = int(item)

        if item.isalpha():
            shifted_index = index
            while (True):
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

    unique_elements = np.unique([x for x in reaction if x.isalpha()])
    dict_template = {k: 0 for k in unique_elements}
    if isinstance(components, list):
        coefficient_array = np.zeros((len(components), len(unique_elements)))
        for index, element in enumerate(components):
            temp_array = np.array(())
            temp_dict = get_elements_number(element.strip() , dict_template)
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
    left_side = reaction.split(side_divider)[0]
    rigth_side = reaction.split(side_divider)[-1]

    left_components = check_reaction_side(left_side)
    right_components = check_reaction_side(rigth_side)

    left_coefficient = get_coefficient(left_components, reaction)
    right_coefficient = get_coefficient(right_components, reaction)
    results = np.zeros([left_coefficient.shape[-1], 1])
    coefficient = np.vstack((left_coefficient, -1 * right_coefficient)).transpose()

    return coefficient, left_coefficient, right_coefficient
    # return np.hstack((coefficient, results))


def get_balance(arrays, left_side, right_side):

    left_shape = left_side.shape
    right_shape = right_side.shape

    a = 0

def main(reaction_to_balance):
    if not validate_input(reaction_to_balance):
        print('Wrong input - some character in string is not allowed')

    z, x, y = get_components(reaction_to_balance)
    get_balance(z, x, y)

if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    expected_output = "C6H12O6 -> 2CH3CH2OH + 2CO2"
    main("C6H12O6 -> CH3CH2OH + CO2")

def Translator(cpp_code):
    source_lines, python_output, i = cpp_code.split('\n'), [], 0
    while i < len(source_lines):
        current_line = source_lines[i].strip()
        if not current_line or current_line.startswith('#include') or current_line.startswith('using'):
            i += 1
        elif current_line.startswith('//'):
            python_output.append('# ' + current_line[2:])
            i += 1
        elif current_line.startswith('struct'):
            python_output.extend(StructTrabslator(source_lines, i))
            i = endOfBlock(source_lines, i)
        elif '(' in current_line and ')' in current_line and not current_line.endswith(';'):
            python_output.extend(FunctionTranslator(source_lines, i))
            i = endOfBlock(source_lines, i)
        else:
            python_output.append(current_line)
            i += 1
    return '\n'.join(python_output)


def StructTrabslator(code_lines, i):
    class_lines, field_definitions = [], []
    struct_name = code_lines[i].split()[1]
    for j in range(i + 1, len(code_lines)):
        line_content = code_lines[j].strip()
        if line_content == '};':
            break
        field_type, field_name = line_content.rstrip(';').split()
        field_definitions.append((field_name, field_type))

    class_lines.append(f'class {struct_name}:')
    class_lines.append('    def __init__(self):')
    for field_name, field_type in field_definitions:
        if field_type == 'string':
            class_lines.append(f'        self.{field_name} = ""')
        elif field_type == 'int' or field_type == 'double':
            class_lines.append(f'        self.{field_name} = 0')
        else:
            class_lines.append(f'        self.{field_name} = None')
    class_lines.append('')
    return class_lines


def FunctionTranslator(code_lines, i):
    function_lines = []
    func_name, params_string = code_lines[i].strip().split('(')
    func_name = func_name.split()[1]
    params_string = params_string[:-3].split(',')
    python_params = ''
    for param_def in params_string:
        if param_def:
            python_params += param_def.split()[1] + ', '
    function_lines.append(f'def {func_name}({python_params[:-2]}):')
    i += 1

    start_index = i - 1
    while i < endOfBlock(code_lines, start_index) - 1:
        current_line = code_lines[i].strip()
        if not current_line:
            function_lines.append('')
        else:
            statement_lines, i = StatementTranslator(code_lines, i)
            if statement_lines:
                for j in range(0, len(statement_lines)):
                    function_lines.append('    ' + statement_lines[j])
        i += 1
    function_lines.append('')
    return function_lines


def endOfBlock(code_lines, i):
    brace_balance = 0
    while i < len(code_lines):
        current_line = code_lines[i]
        brace_balance += current_line.count('{')
        brace_balance -= current_line.count('}')
        if brace_balance == 0 and '}' in current_line:
            return i + 1
        i += 1


def StatementTranslator(code_lines, i):
    current_line = code_lines[i].strip().rstrip(';')
    if not current_line:
        return '', i
    elif current_line.startswith('if'):
        if_block = [f'if {code_lines[i].rstrip('{').strip()[4:-1]}:']
        last_index = i
        for j in range(i + 1, len(code_lines)):
            last_index = j
            inner_line = code_lines[j]
            if inner_line == '}':
                break
            elif inner_line == '    }':
                last_index -= 1
                break
            inner_line = inner_line.strip()
            if inner_line.startswith('else if'):
                if_block.append(f'elif {code_lines[j].rstrip('{').strip()[9:-1]}:')
            elif inner_line.startswith('else'):
                if_block.append(f'else:')
            else:
                inner_translated, j = StatementTranslator(code_lines, j)
                last_index = j
                for k in range(0, len(inner_translated)):
                    if_block.append('    ' + inner_translated[k])
        return if_block, last_index
    elif current_line.startswith('for'):
        loop_block = []
        loop_parts = current_line[5:-3].split(';')
        loop_block.append(f'for {loop_parts[0].split()[1]} in range({loop_parts[0].split()[3]}, {loop_parts[1].split()[2]}):')
        last_index, j = i, i + 1
        while j < len(code_lines):
            inner_line = code_lines[j].strip()
            if inner_line == '}':
                break
            inner_translated, j = StatementTranslator(code_lines, j)
            last_index = j
            for k in range(0, len(inner_translated)):
                loop_block.append('    ' + inner_translated[k])
            j += 1
        return loop_block, last_index + 1
    elif current_line.startswith('return'):
        return_value = current_line[7:].replace('true', 'True').replace('false', 'False')
        if return_value:
            return [f'return {return_value}'], i
        else:
            return ['return'], i
    else:
        if current_line == '}':
            return '', i
        current_line = current_line.replace('->', '.')
        current_line = current_line.replace('true', 'True').replace('false', 'False')
        current_line = current_line.replace('{', '[').replace('}', ']')
        if '=' in current_line:
            assignment_parts = current_line.split('=')
            if len(assignment_parts[0].split()) > 1:
                assignment_parts[0] = assignment_parts[0].split()[-1]
                assignment_parts[0] = assignment_parts[0].split('[')[0]
            return [f'{assignment_parts[0].strip()} = {assignment_parts[1].strip()}'], i
        current_line = current_line.replace('++', ' += 1').replace('--', ' -= 1')
        return [current_line], i


if __name__ == "__main__":
    with open('input.cpp') as cpp:
        with open('output.py', 'w') as python:
            python.write(Translator(cpp.read()))

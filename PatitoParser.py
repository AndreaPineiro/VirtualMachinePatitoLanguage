# ------------------------------------------------------------
# PatitoParser.py
#
# Parser for rules defined for Patito language
# ------------------------------------------------------------

import ply.yacc as yacc
from tabulate import tabulate
from PatitoLexer import PatitoLexer

class PatitoParser(object):

    def __init__(self):
        # Initialization of stacks, queues and tables
        self.symbol_table = {}
        self.quadruplos = []
        self.stack_operands = []
        self.stack_operators = []
        self.stack_types = []
        self.stack_jumps = []
        self.count_quads = 0
        self.symbol_factor = None
        
        # Get information from lexer
        self.tokens = PatitoLexer.tokens

        self.memory_directions = {
            'const_int': 0,
            'const_float': 500,
            'const_strings': 1000,
            'var_int': 1500,
            'var_float': 2000,
            'temp_int': 2500,
            'temp_float': 3000,
            'temp_bool': 3500,
        }

        # Semantic Cube
        self.cube = {
            ('int', 'int', '+'): 'int',
            ('int', 'int', '-'): 'int',
            ('int', 'int', '*'): 'int',
            ('int', 'int', '/'): 'float',
            ('int', 'int', '>'): 'bool',
            ('int', 'int', '<'): 'bool',
            ('int', 'int', '!='): 'bool',
            ('int', 'int', '='): 'int',
            ('int', 'float', '+'): 'float',
            ('int', 'float', '-'): 'float',
            ('int', 'float', '*'): 'float',
            ('int', 'float', '/'): 'float',
            ('int', 'float', '>'): 'bool',
            ('int', 'float', '<'): 'bool',
            ('int', 'float', '!='): 'bool',
            ('float', 'float', '+'): 'float',
            ('float', 'float', '-'): 'float',
            ('float', 'float', '*'): 'float',
            ('float', 'float', '/'): 'float',
            ('float', 'float', '>'): 'bool',
            ('float', 'float', '<'): 'bool',
            ('float', 'float', '!='): 'bool',
            ('float', 'float', '='): 'int',
            ('float', 'int', '+'): 'float',
            ('float', 'int', '-'): 'float',
            ('float', 'int', '*'): 'float',
            ('float', 'int', '/'): 'float',
            ('float', 'int', '>'): 'bool',
            ('float', 'int', '<'): 'bool',
            ('float', 'int', '!='): 'bool',
        }

    # Print information
    def print_res(self):
        if self.error == '':
            self.print_symbol_table()
            self.print_constant_table()
            self.print_memory_table()
            self.print_quad()

    # Print every quadruple
    def print_quad(self):
        print('QUADRUPLES')
        cnt = 0
        for i in self.quadruplos:
            print(cnt, i)
            cnt += 1

    # Print constant table
    def print_constant_table(self):
        if len(self.constants_table) > 0:
            print('CONSTANTS TABLE')
            # Convert the dictionary into nested lists
            tabla = [[clave] + list(valores.values()) for clave, valores in self.constants_table.items()]

            # Get keys as headers
            encabezados = [''] + list(next(iter(self.constants_table.values())).keys())

            # Print symbol table
            print(tabulate(tabla, headers=encabezados, tablefmt='grid'))
            print('\n')

    # Print memory table. Prints the tuples to see crearly dict and memory list
    def print_memory_table(self):
        if len(self.memory) > 0:
            print('MEMORY:', self.memory)
            print('\n')

    # Print symbol table
    def print_symbol_table(self):
        if len(self.symbol_table) > 0:
            print('SYMBOL TABLE')
            # Convert the dictionary into nested lists
            tabla = [[clave] + list(valores.values()) for clave, valores in self.symbol_table.items()]

            # Get keys as headers
            encabezados = [''] + list(next(iter(self.symbol_table.values())).keys())

            # Print symbol table
            print(tabulate(tabla, headers=encabezados, tablefmt='grid'))
            print('\n')

    def parse(self, data, print_flag = False):
        # Creation of parser and lexer
        try:
            parser = yacc.yacc(module=self, start='program')
            self.lexer = PatitoLexer().build()

            # Set errors and symbol table as empty
            self.error = ''
            self.symbol_table = {}
            self.quadruplos = []
            self.stack_operands = []
            self.stack_operators = []
            self.stack_types = []
            self.stack_jumps = []
            self.count_quads = 0
            self.symbol_factor = None

            self.count_memory = {
                'const_int': 0,
                'const_float': 0,
                'const_strings': 0,
                'var_int': 0,
                'var_float': 0,
                'temp_int': 0,
                'temp_float': 0,
                'temp_bool': 0
            }

            self.constants_table = {}
            self.memory = []

            # Parse the program and print the symbol table.
            parser.parse(data)

            if (self.error != ''):
                print('\nWRONG PROGRAM :(')
                print(self.error)
            else:
                if print_flag:
                    self.print_res()

            return self.quadruplos, self.constants_table, self.symbol_table, self.memory, self.count_memory, self.memory_directions, self.error

        # Stop parsing and show errors
        except yacc.YaccError as e:
            print('WRONG PROGRAM :(')
            print(self.error)

    # Test lexer
    def test(self, data):
        self.parse(data)

        if (self.error == ''):
            self.print_res()

    # Function wihich fills GoTo quads with jump
    def fill_quad(self, quad):
        quad1, quad2, quad3, quad4 = self.quadruplos[quad]
        self.quadruplos[quad] = (quad1, quad2, quad3, self.count_quads)

    # Function which receives 4 args, creates quad and add 1 to count_quads
    def aux_generate_quad(self, quad1, quad2, quad3, quad4):
        self.quadruplos.append((quad1, quad2, quad3, quad4))
        self.count_quads += 1
    
    # Function which creates a new memory space for temporal variable
    def add_count_memory(self, result_type, temp = False):
        new_dir = self.memory_directions[result_type] + self.count_memory[result_type]
        self.count_memory[result_type] += 1
        if temp:
            self.stack_operands.append(new_dir)
            if result_type == 'temp_int':
                    result_type = 'int'
            elif result_type == 'temp_float':
                result_type = 'float'
            elif result_type == 'temp_bool':
                result_type = 'bool'
            self.stack_types.append(result_type)
        return new_dir   
    
    def add_constant_to_memory(self, type_dir):
        new_dir = self.memory_directions[type_dir] + self.count_memory[type_dir]

        if type_dir == 'const_int':
            index = self.count_memory['const_int']
        elif type_dir == 'const_float':
            index = self.count_memory['const_int'] + self.count_memory['const_float']
        elif type_dir == 'const_strings':
            index = self.count_memory['const_int'] + self.count_memory['const_float'] + self.count_memory['const_strings']
        else:
            self.error += 'Error. Direction type does not exist'

        self.count_memory[type_dir] += 1
        
        self.memory.insert(index, None)
        return new_dir

    # Find constant in memory receiving a direction
    def find_cnst_in_memory(self, find_dir, type_dir):
        if type_dir == 'const_int':
            index = find_dir - self.memory_directions['const_int']
        elif type_dir == 'const_float':
            index = self.count_memory['const_int'] + (find_dir - self.memory_directions['const_float'])
        elif type_dir == 'const_strings':
            index = self.count_memory['const_int'] +  self.count_memory['const_float'] + (find_dir - self.memory_directions['const_strings'])
        
        return index
    
    # Fill memory direction with certail value
    def fill_memory(self, memory_dir, value, type_dir):
        index = self.find_cnst_in_memory(memory_dir, type_dir)
        self.memory[index] = value
    
    # Function which generates quad depending on the type of quad.
    # Valid type_quad = {operation, assign, change_symbol, GotoF, GoToV, GoTo, cout}
    def generate_quad(self, type_quad, line = None):
        # For operation and assign quads
        if type_quad == 'operation' or type_quad == 'assign':
            # Get operator, right and left operand and type
            right_operand = self.stack_operands.pop()
            right_type = self.stack_types.pop()
            left_operand = self.stack_operands.pop()
            left_type = self.stack_types.pop()
            operator = self.stack_operators.pop()

            # Check if the operator and operands match a valid semantic
            if (left_type, right_type, operator) in self.cube:
                # Get expected result
                result_type = self.cube[left_type, right_type, operator]
                
                # If the quad it's an operation create a new variable and generate quad
                if type_quad == 'operation':
                    if result_type == 'int':
                        result_type = 'temp_int'
                    elif result_type == 'float':
                        result_type = 'temp_float'
                    elif result_type == 'bool':
                        result_type = 'temp_bool'
                    else:
                        self.error += 'Error. Invalid variable type.\n'
                        raise yacc.YaccError("Direction type")
                    
                    result = self.add_count_memory(result_type, True)
                    self.aux_generate_quad(operator, left_operand, right_operand, result)

                # If the quad it's an assignment only generate quad
                elif type_quad == 'assign':
                    self.aux_generate_quad(operator, None, right_operand, left_operand)
            # Error if the type is invalid
            else:
                self.error += 'ERROR. Type mismatch.\n'
                raise yacc.YaccError("Type mismatch")
        
        # For change symbol type
        elif type_quad == 'change_symbol':
            right_operand = self.stack_operands.pop()
            right_type = self.stack_types.pop()
            left_operand = None
            operator = self.symbol_factor
            self.symbol_factor = None
            
            # Get expected result
            result_type = right_type
            result = self.add_temporal_memory(result_type)

            # Generate quad with None left_operand 
            self.aux_generate_quad(operator, left_operand, right_operand, result)

        # For GoToF and GoToV
        elif type_quad == 'GoToF' or type_quad == 'GoToV':
            exp_type = self.stack_types.pop()
            result = self.stack_operands.pop()

            if (exp_type != 'bool'):
                self.error += 'ERROR. Type mismatch in line ' + line +  '. Condition expects bool.\n'
                raise yacc.YaccError("Error de sintaxis")
            else:
                if type_quad == 'GoToF':
                    self.aux_generate_quad(type_quad, None, result, None)
                    self.stack_jumps.append(self.count_quads - 1)
                elif type_quad == 'GoToV':
                    jump = self.stack_jumps.pop()
                    self.aux_generate_quad(type_quad, None, result, jump)

        elif type_quad == 'GoTo':
            self.aux_generate_quad(type_quad, None, None, None)

        elif type_quad == 'cout':
            right_operand = self.stack_operands.pop()
            left_operand = self.stack_operands.pop()
            self.stack_types.pop()
            self.aux_generate_quad(type_quad, left_operand, right_operand, None)    

    # Definition of rules
    def p_empty(self, p):
        'empty :'
        pass

    # Program definition
    def p_program(self, p):
        'program : PROGRAM ID SEMICOLON r body END'
    
    def p_r(self, p):
        '''r : empty
                | vars'''
        
    # Vars definition
    def p_vars(self, p):
        'vars : VAR n'

    def p_n(self, p):
        'n : o COLON type SEMICOLON q'

    def p_o(self, p):
        'o : ID p'
        # Get variable name
        variable_name = p[1]

        # If the variable is already stored show error, if it is not in the dictionary add it.
        if variable_name in self.symbol_table:
            self.error += "ERROR. Duplicated variable: '" + variable_name + "' in line " + str(p.lineno(1)) + ".\n"
            raise yacc.YaccError("Error de semántica")
        else:
            self.symbol_table[variable_name] = {
                'type_var': None,
                'memory_dir': None
            }
    
    def p_p(self, p):
        '''p : COMMA o
                | empty'''
        
    def p_q(self, p):
        '''q : n
                | empty'''
        
    # Type definition
    def p_type(self, p):
        '''type : INT
                | FLOAT'''
        # Get data type
        variable_type = p[1]

        # For each variable that has variable type None add the type of variable obtained
        for key in self.symbol_table:
            if self.symbol_table[key]['type_var'] is None:
                self.symbol_table[key]['type_var'] = variable_type
                if variable_type == 'int':
                    self.symbol_table[key]['memory_dir'] = self.add_count_memory('var_int')
                elif variable_type == 'float':
                    self.symbol_table[key]['memory_dir'] = self.add_count_memory('var_float')
        
    # Body definition
    def p_body(self, p):
        'body : LEFT_BRACE m RIGHT_BRACE'

    def p_m(self, p):
        '''m : statement m
                | empty'''
        
    # Statement definition
    def p_statement(self, p):
        '''statement : assign
                        | condition
                        | cycle
                        | print'''
    
    # Assign definition
    def p_assign(self, p):
        'assign : id_assign equal_assign expresion SEMICOLON'
        self.generate_quad('assign')

    def p_id_assign(self, p):
        'id_assign : ID'
        # Get variable name
        variable = p[1]

        # If the variable is not found in the data dictionary, display error.
        if variable not in self.symbol_table:
            self.error += "ERROR. Variable not declared: '" + variable + "' in line " + str(p.lineno(1)) + ".\n"
            raise yacc.YaccError("Error de sintaxis")
        # If the variable is declared append variable to operands stack and it's type to types stack
        else:
            self.stack_operands.append(self.symbol_table[variable]['memory_dir'])
            self.stack_types.append(self.symbol_table[variable]['type_var'])

    def p_equal_assign(self, p):
        'equal_assign : EQUAL'
        # Append equal operator
        self.stack_operators.append(p[1])

    # Print definition
    def p_print(self, p):
        'print : COUT LEFT_PARENTHESIS j RIGHT_PARENTHESIS SEMICOLON'
        # If the print statement ends add line_break to operands and generate quad
        if 'line_break' not in self.constants_table:
            new_dir = self.add_constant_to_memory('const_strings')
            self.fill_memory(new_dir, 'line_break', 'const_strings')

            self.constants_table['line_break'] = {
                'type_var': 'string',
                'memory_dir': new_dir
        }

        memory_dir = self.constants_table['line_break']['memory_dir']
        self.stack_operands.append(memory_dir)
        self.generate_quad('cout')

    def p_j(self, p):
        'j : k l'
    
    def p_k(self, p):
        '''k : expresion
                | CTE_STRING'''
        # If it's a string add it to the constant table and to operands
        if p[1] is not None:
            if p[1] not in self.constants_table:
                new_dir = self.add_constant_to_memory('const_strings')
                self.fill_memory(new_dir, p[1], 'const_strings')

                self.constants_table[p[1]] = {
                    'type_var': 'string',
                    'memory_dir': new_dir
            }
            
            memory_dir = self.constants_table[p[1]]['memory_dir']
            self.stack_operands.append(memory_dir)
            self.stack_types.append('string')

    def p_l(self, p):
        '''l : comma j
                | empty'''
        
    def p_comma(self, p):
        'comma : COMMA'
        # If the print statement has a comma ad blank_space to operands and generate qiad
        if 'blank_space' not in self.constants_table:
            new_dir = self.add_constant_to_memory('const_strings')
            self.fill_memory(new_dir, 'blank_space', 'const_strings')

            self.constants_table['blank_space'] = {
                'type_var': 'string',
                'memory_dir': new_dir
        }

        memory_dir = self.constants_table['blank_space']['memory_dir']
        self.stack_operands.append(memory_dir)
        self.generate_quad('cout')
        
    # Cycle definition
    def p_cycle(self, p):
        'cycle : do body WHILE LEFT_PARENTHESIS expresion right_par_cycle SEMICOLON'

    def p_do(self, p):
        'do : DO'
        # Add current quad to jumps stack
        self.stack_jumps.append(self.count_quads)

    def p_right_par_cycle(self, p):
        'right_par_cycle : RIGHT_PARENTHESIS'
        # Generate quad to jump if the condition is true
        self.generate_quad('GoToV', str(p.lineno(1)))

    # Expresion definition
    def p_expresion(self, p):
        'expresion : exp h'

    def p_h(self, p):
        '''h : i exp
                | empty'''
        
    def p_i(self, p):
        '''i : GREATER_THAN
                | LESS_THAN
                | DIFFERENT_THAN '''
        # Add operator to stack
        self.stack_operators.append(p[1])

    # Condition definition
    def p_condition(self, p):
        'condition : IF u g SEMICOLON'
        # If condition ends fill quad with the last jump
        end_jump = self.stack_jumps.pop()
        self.fill_quad(end_jump)
        if self.stack_jumps:
            end_jump = self.stack_jumps[-1]
            quad1, quad2, quad3, quad4 = self.quadruplos[end_jump]
            if quad1 == 'GoTo':
                self.fill_quad(end_jump)
                end_jump = self.stack_jumps.pop()

    def p_u(self, p):
        'u : LEFT_PARENTHESIS expresion right_par_cond body'

    
    def p_right_par_cond(self, p):
        'right_par_cond : RIGHT_PARENTHESIS'
        # Generate a GoToF quad and send line number in case an error occurs
        self.generate_quad('GoToF', str(p.lineno(1)))

    def p_v(self, p):
        'v : else body'
        
    def p_g(self, p):
        '''g : elif u v
                | v
                | empty'''

    def p_elif(self, p):
        'elif : ELIF'
        # Generate a GoTo quad and fill GoToF quad
        self.generate_quad('GoTo')
        false_jump = self.stack_jumps.pop()
        self.stack_jumps.append(self.count_quads - 1)
        self.fill_quad(false_jump)
        
    def p_else(self, p):
        'else : ELSE'
        # Generate a GoTo quad and fill GoToF quad
        self.generate_quad('GoTo')
        false_jump = self.stack_jumps.pop()
        self.stack_jumps.append(self.count_quads - 1)
        self.fill_quad(false_jump)

    # Factor definition
    def p_factor(self, p):
        '''factor : left_par_fact expresion right_par_fact
                    | e f'''
        # If top of the stack operators is * or / generate quad
        if self.stack_operators and (self.stack_operators[-1] == '*' or self.stack_operators[-1] == '/'):
            self.generate_quad('operation')

    def p_left_par_fact(self, p):
        '''left_par_fact : LEFT_PARENTHESIS'''
        # Add ( to the stack
        self.stack_operators.append(p[1])

    def p_right_par_fact(self, p):
        '''right_par_fact : RIGHT_PARENTHESIS'''
        # Remove ( from the stack
        self.stack_operators.pop()

    
    def p_e(self, p):
        '''e : MINUS
                | PLUS
                | empty'''
        # Add - to symbol_factor variable to change the symbol of the variable.
        if p[1] == '-':
            self.symbol_factor = p[1]
            

        
    def p_f(self, p):
        '''f : ID
                | cte'''
        
        if p[1] is not None :
            # Get variable name
            variable = p[1]

            # Si la variable no se encuentra en el diccionario de datos, mostrar error.
            if variable not in self.symbol_table:
                self.error += "ERROR. Variable not declared: '" + variable + "' in line " + str(p.lineno(1)) + ".\n"
                raise yacc.YaccError("Error de sintaxis")
                
            self.stack_operands.append(self.symbol_table[variable]['memory_dir'])
            self.stack_types.append(self.symbol_table[variable]['type_var'])

            if self.symbol_factor is not None:
            # Add variable to operands stack and type to types stack
                self.generate_quad('change_symbol')
        
    # Exp definition
    def p_exp(self, p):
        'exp : term c'
        # If top of the stack operators is not null generate quad
        if self.stack_operators and (self.stack_operators[-1] == '>' or self.stack_operators[-1] == '<' or self.stack_operators[-1] == '!='):
            self.generate_quad('operation')

    def p_c(self, p):
        '''c : d exp
                | empty'''
        
    def p_d(self, p):
        '''d : PLUS
                | MINUS'''
        # Add + or - to operators stack
        self.stack_operators.append(p[1])

    # Term definition  
    def p_term(self, p):
        'term : factor a'
        # If top of the stack operators is + or - generate quad
        if self.stack_operators and (self.stack_operators[-1] == '-' or self.stack_operators[-1] == '+'):
            self.generate_quad('operation')
    
    def p_a(self, p):
        '''a : b term
                | empty'''
        
    def p_b(self, p):
        '''b : TIMES
                | DIVIDE'''
        # Add * or / to operators stack
        self.stack_operators.append(p[1])
        
    # CTE definition
    def p_cte(self, p):
        '''cte : CTE_INT
                | CTE_FLOAT'''
        cte = p[1]

        if cte not in self.constants_table:
            # Add it's type to the stack and add number to constant table
            if isinstance(cte, int):
                type_var = 'int'
                new_dir = self.add_constant_to_memory('const_int')
                self.fill_memory(new_dir, cte, 'const_int')

            elif isinstance(cte, float):
                type_var = 'float'
                new_dir = self.add_constant_to_memory('const_float')
                self.fill_memory(new_dir, cte, 'const_float')

            else:
                self.error += 'Constant ', cte, ' is not int or float.'
                raise yacc.YaccError('Constant ', cte, ' is not int or float.')
            
            self.constants_table[cte] = {
                    'type_var': type_var,
                    'memory_dir': new_dir
            }

        memory_dir = self.constants_table[cte]['memory_dir']
        type_var = self.constants_table[cte]['type_var']

        if self.symbol_factor is not None:
            # Add variable to operands stack and type to types stack
                self.generate_quad('change_symbol')

        # Add number to constant table and to operands stack
        self.stack_operands.append(memory_dir)
        self.stack_types.append(type_var)

    # Error rule for syntax errors
    def p_error(self, p):
        if p:
            # If there are other error, split them with a new line and print error. 
            if self.error != "":
                self.error += '\n'
            self.error += "Syntax error at token: " + str(p.type)
            self.error += "\nToken value: " + str(p.value) 
            self.error += "\nError at line: " + str(p.lineno)
            self.error += "\nError at position: " + str(p.lexpos) + "\n"
        else:
            print("Syntax error: Unexpected end of input")


# Function to read file
def read_file(file_path):
    file = open(file_path, "r")
    data = file.read()
    file.close()
    return data

# Build and test parser
if __name__ == '__main__':
    parser = PatitoParser()

    # Testcase with correct syntax and semantics
    print('\n')
    print('--------- CORRECT TESTCASE --------- ')
    data = read_file("testFibonacciFactorial.txt")
    parser.test(data)
    
    # Testcase with wrong syntax (error line 13, missing ;)
    print('\n\n')
    print('--------- INCORRECT SYNTAX TESTCASE --------- ')
    data = read_file("testSintaxisIncorrecta.txt")
    parser.test(data)

    # Testcase with wrong semantics (use duplicated variable)
    print('\n\n')
    print('--------- INCORRECT SEMANTICS TESTCASE --------- ')
    data = read_file("testSemanticaIncorrecta.txt")
    parser.test(data)

    # Testcase with operations 
    print('\n')
    print('--------- OPERATIONS TESTCASE --------- ')
    data = read_file("testOperations.txt")
    parser.test(data)

    # Testcase with condition 
    print('\n')
    print('--------- CONDITION TESTCASE --------- ')
    data = read_file("testCondition.txt")
    parser.test(data)

    # Testcase with while 
    print('\n')
    print('--------- WHILE TESTCASE --------- ')
    data = read_file("testWhile.txt")
    parser.test(data)

    # Testcase with print 
    print('\n')
    print('--------- PRINT TESTCASE --------- ')
    data = read_file("testPrint.txt")
    parser.test(data)

    # Testcase with correct syntax and semantics
    print('\n')
    print('--------- CORRECT TESTCASE --------- ')
    data = read_file("test.txt")
    parser.test(data)
    
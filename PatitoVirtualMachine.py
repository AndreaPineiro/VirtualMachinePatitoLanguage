# ------------------------------------------------------------
# PatitoVirtualMachine.py
#
# Virtual Machine to execute a program in Patito Language
# ------------------------------------------------------------


from PatitoParser import PatitoParser

class PatitoVirtualMachine(object):
    def test(self, program, print_flag = False):
        self.error = ''
        try:
            # Create parser
            parser = PatitoParser()
            # Get important information from the compiler
            self.quadruples, self.constants_table, self.symbol_table, self.memory_const, self.count_memory, self.memory_directions, self.error = parser.parse(program, print_flag)
            ## Print error
            if self.error != '':
                return
            
            try:
                # Create memory and run program
                self.memory = self.create_memory_vars()
                self.execute()
                # Print memory
                self.print_memory()
            except Exception as e:
                print('Error in Virtual Machine ', e)
        except Exception as e:
            print('Error in Compiler\n', self.error)

    # Print memory
    def print_memory(self):
        print("\nMEMORY")
        print(self.memory)
        print('\n')
        
    # Create memory (an array with the size of all the counters)
    def create_memory_vars(self):
        size = (self.count_memory['var_int'] + self.count_memory['var_float'] + self.count_memory['temp_int'] + self.count_memory['temp_float'] + self.count_memory['temp_bool'])
        self.memory = self.memory_const + [None for _ in range(size)]
        return self.memory

    # Find memory in the memory array
    def find_dir_in_memory(self, find_dir):
        if find_dir != None:
            count_memory_values = list(self.count_memory.values())
            if find_dir >= self.memory_directions['const_int'] and find_dir < self.memory_directions['const_float']:
                index = find_dir - self.memory_directions['const_int']
            elif find_dir >= self.memory_directions['const_float'] and find_dir < self.memory_directions['const_strings']:
                index = count_memory_values[0] + (find_dir - self.memory_directions['const_float'])
            elif find_dir >= self.memory_directions['const_strings'] and find_dir < self.memory_directions['var_int']:
                index = sum(count_memory_values[0:2]) + (find_dir - self.memory_directions['const_strings'])
            elif find_dir >= self.memory_directions['var_int'] and find_dir < self.memory_directions['var_float']:
                index = sum(count_memory_values[0:3]) + (find_dir - self.memory_directions['var_int'])
            elif find_dir >= self.memory_directions['var_float'] and find_dir < self.memory_directions['temp_int']:
                index = sum(count_memory_values[0:4]) + (find_dir - self.memory_directions['var_float'])
            elif find_dir >= self.memory_directions['temp_int'] and find_dir < self.memory_directions['temp_float']:
                index = sum(count_memory_values[0:5]) + (find_dir - self.memory_directions['temp_int'])
            elif find_dir >= self.memory_directions['temp_float'] and find_dir < self.memory_directions['temp_bool']:
                index = sum(count_memory_values[0:6]) + (find_dir - self.memory_directions['temp_float'])
            elif find_dir >= self.memory_directions['temp_bool'] and find_dir < self.memory_directions['temp_bool'] + 500:
                index = sum(count_memory_values[0:7]) + (find_dir - self.memory_directions['temp_bool'])
            return index
    
    # Funtion that executes the program
    def execute(self):
        # Counter to know which quad to check
        program_counter = 0

        # Execute every quad
        while program_counter < len(self.quadruples):
            # Get quad
            quad = self.quadruples[program_counter]
            operation, operand1, operand2, result = quad
            # Find indexes of the directions in memory
            index_operand1 = self.find_dir_in_memory(operand1)
            index_operand2 = self.find_dir_in_memory(operand2)
            index_result = self.find_dir_in_memory(result)

            # Switch for every tipe of operation
            if operation == '+':
                self.memory[index_result] = self.memory[index_operand1] + self.memory[index_operand2]
            if operation == '-':
                if self.memory[index_operand1] == None:
                    self.memory[index_result] = - self.memory[index_operand2]
                else:
                    self.memory[index_result] = self.memory[index_operand1] - self.memory[index_operand2]
            if operation == '*':
                self.memory[index_result] = self.memory[index_operand1] * self.memory[index_operand2]
            if operation == '/':
                self.memory[index_result] = self.memory[index_operand1] / self.memory[index_operand2]
            if operation == '>':
                self.memory[index_result] = self.memory[index_operand1] > self.memory[index_operand2]
            if operation == '<':
                self.memory[index_result] = self.memory[index_operand1] < self.memory[index_operand2]
            if operation == '!=':
                self.memory[index_result] = self.memory[index_operand1] != self.memory[index_operand2]
            if operation == '=':
                self.memory[index_result] = self.memory[index_operand2]
            if operation == 'cout':
                # Print different depending if it's a line break or a line space after
                if self.memory[index_operand2] == 'line_break':
                    print(self.memory[index_operand1])
                elif self.memory[index_operand2] == 'blank_space':
                    print(self.memory[index_operand1], end=" ")
            # GoTos move the program counter to the quad of the jump
            if operation == 'GoTo':
                program_counter = result - 1
            if operation == 'GoToV':
                if self.memory[index_operand2] == True:
                    program_counter = result - 1
            if operation == 'GoToF':
                if self.memory[index_operand2] == False:
                    program_counter = result - 1
            
            program_counter += 1

# Function to read file
def read_file(file_path):
    file = open(file_path, "r")
    data = file.read()
    file.close()
    return data


if __name__ == '__main__':
    patitoVM = PatitoVirtualMachine()

    # Testcase with correct syntax and semantics
    print('\n')
    print('--------- FIBONNACCI AND FACTORIAL --------- ')
    data = read_file("testFibonacciFactorial.txt")
    patitoVM.test(data)

    # Testcase with condition 
    print('\n')
    print('--------- CONDITION TESTCASE (ELIF) --------- ')
    data = read_file("testCondition.txt")
    patitoVM.test(data)
    
    # Testcase with wrong syntax (error line 13, missing ;)
    print('\n\n')
    print('--------- INCORRECT SYNTAX TESTCASE --------- ')
    data = read_file("testSintaxisIncorrecta.txt")
    patitoVM.test(data)

    # Testcase with wrong semantics (use duplicated variable)
    print('\n\n')
    print('--------- INCORRECT SEMANTICS TESTCASE --------- ')
    data = read_file("testSemanticaIncorrecta.txt")
    patitoVM.test(data)

    # Testcase with operations 
    print('\n')
    print('--------- OPERATIONS TESTCASE --------- ')
    data = read_file("testOperations.txt")
    patitoVM.test(data)

    # Testcase with while 
    print('\n')
    print('--------- WHILE TESTCASE --------- ')
    data = read_file("testWhile.txt")
    patitoVM.test(data)

    # Testcase with print 
    print('\n')
    print('--------- PRINT TESTCASE --------- ')
    data = read_file("testPrint.txt")
    patitoVM.test(data)

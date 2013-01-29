import sys

__author__ = 'Eirik Mildestveit Hammerstad'

class Interpreter:
    call_stack = []
    input = []  # Kept for ,
    output = [] # Used for .
    instruction_set = {}
    memory = [0]*32768
    source = []
    instruction_pointer = 0
    data_pointer = 0
    exit_loop = False

    def __init__(self, program_code):
        self.source = program_code

        self.instruction_set['+'] = self.__increase
        self.instruction_set['-'] = self.__decrease
        self.instruction_set['>'] = self.__right
        self.instruction_set['<'] = self.__left
        self.instruction_set['['] = self.__loop_start
        self.instruction_set[']'] = self.__loop_end
        self.instruction_set['.'] = self.__output
        self.instruction_set[','] = self.__input


    def run(self, max_instructions = 0):
        if max_instructions > 0:
            self.__run_limited(max_instructions)
        else:
            self.__run_unlimited()

    def __run_limited(self, max_instructions):
        count = 0
        while self.instruction_pointer < len(self.source):
            instruction = self.source[self.instruction_pointer]
            if instruction in self.instruction_set:
                action = self.instruction_set[instruction]
                action()

            self.instruction_pointer += 1
            count += 1
            if max_instructions > 0 and count > max_instructions:
                break

    def __run_unlimited(self):
        while self.instruction_pointer < len(self.source):
            instruction = self.source[self.instruction_pointer]
            if instruction in self.instruction_set:
                action = self.instruction_set[instruction]
                action()

            self.instruction_pointer += 1

    def __increase(self):
        if not self.exit_loop:
            self.memory[self.data_pointer]+=1

    def __decrease(self):
        if not self.exit_loop:
            self.memory[self.data_pointer]-=1

    def __right(self):
        if not self.exit_loop:
            self.data_pointer+=1

    def __left(self):
        if not self.exit_loop:
            self.data_pointer-=1

    def __loop_start(self):
        if not self.exit_loop:
            if self.memory[self.data_pointer] == 0:
                self.exit_loop = True
            else:
                self.call_stack.append(self.instruction_pointer)

    def __loop_end(self):
        if not self.exit_loop:
            temp = self.call_stack.pop() - 1
            self.instruction_pointer = temp if self.memory[self.data_pointer] != 0 else self.instruction_pointer
        else:
            self.exit_loop = False

    def __output(self):
        self.output.append(self.memory[self.data_pointer])

    def __input(self):
        self.memory[self.data_pointer] = self.input.pop()

    def print_output(self):
        print ([chr(value) for value in self.output])

#LETS TRY:
hello_world = sys.argv[1:]
if not hello_world:
    hello_world =  "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
x = Interpreter(program_code = hello_world )
x.run()
x.print_output()
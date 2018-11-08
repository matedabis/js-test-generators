#!/usr/bin/env python


# Copyright JS Foundation and other contributors, http://js.foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import argparse
import settings
import collections
path = os.path.join(settings.TEMPLATE_DIR)
sys.path.append(path)
import validate
import random
import math

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--op", help = "give the operators to be tested", nargs = '+',
    default = ["+", "-", "/", "*", "%"], choices = ["+", "-", "/", "*", "%"])
    parser.add_argument("--test-count", help = "give the number of tests to run", nargs = 1, default = [500],
    type = int)
    parser.add_argument("--output", help = "give the path to generate files into", nargs = 1, default = settings.NUMBER_DIR,
    type = str)
    parser.add_argument("--operand-count", help = "give the number of maximum operands in an expression",
    nargs = 1, default = [10], choices = range(2, 11), type = int)
    parser.add_argument("--seed", help = "give the random seed value", nargs = 1, default = [10000],
    type = int)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    script_args = parser.parse_args()

    # print(script_args)

    return script_args

filename = '''binary-ops-{NUMBER}.js'''
MAX = 9007199254740991
MIN = -9007199254740991
sys.maxint = 9007199254740991
sys.minint = -9007199254740991
# print(str(sys.maxint) + "  " + str(sys.minint))

class Integer:

    def __init__(self, integer, seed):
        self.integer = integer
        self.seed = seed

    def __add__(self, other):
        random.seed(self.seed)
        new = self.integer + other.integer
        while((new > MAX) or (new < MIN)):
            other.integer = random.randint(MIN, MAX)
            new = self.integer + other.integer
        return Integer(new, self.seed)

    def __sub__(self, other):
        random.seed(self.seed)
        new = self.integer - other.integer
        while(new > MAX or new < MIN):
            other.integer = random.randint(MIN, MAX)
            new = self.integer - other.integer
        return Integer(new, self.seed)

    def __mul__(self, other):
        random.seed(self.seed)
        new = self.integer * other.integer
        while(new > MAX or new < MIN):
            MAXNUM = min(math.fabs(math.floor(MAX / self.integer)), MAX)
            MINNUM = - MAXNUM
            other.integer = random.randint(MINNUM,MAXNUM)
            new = self.integer * other.integer
        return Integer(new, self.seed)

    def __truediv__(self, other):
        random.seed(self.seed)
        new = self.integer / other.integer
        while(new > MAX or new < MIN):
            other.integer = random.randint(MIN,MAX)
            new = self.integer / other.integer
        return Integer(new, self.seed)

    def __mod__(self, other):
        random.seed(self.seed)
        if (((self.integer < 0 and other.integer > 0) or (self.integer > 0 and other.integer < 0)) and (self.integer % other.integer != 0)):
            new = ((self.integer % other.integer) - other.integer)
        else:
            new = (self.integer % other.integer)
        while(new > MAX or new < MIN):
            other.integer = random.randint(MIN,MAX)
            if (((self.integer < 0 and other.integer > 0) or (self.integer > 0 and other.integer < 0)) and (self.integer % other.integer != 0)):
                new = ((self.integer % other.integer) - other.integer)
            else:
                new = (self.integer % other.integer)
        return Integer(new, self.seed)

def generate_binary_tests(options):

    SEED = options.seed[0]
    random.seed(SEED)
    opArgsNo = len(options.op)
    file_to_open = os.path.join(settings.NUMBER_DIR, filename.format(NUMBER = 1))
    with open(file_to_open, "w") as file:
        file.write(validate.validate)
        for i in range(options.test_count[0]):
            SEED += 1
            expression = ""
            executable_string = "intExpression = Integer(0, SEED)\n"
            generateInt = '''int{NUMBER} = Integer(random.randint(MIN,MAX), SEED)\n'''
            integers = '''int{NUMBER}'''
            operators = []
            for i in range(options.operand_count[0]):
                executable_string += "%s" % (generateInt.format(NUMBER = i))
            print(executable_string)

            executable_string += "intExpression = "
            for i in range(options.operand_count[0] - 1):
                N = random.randint(1, len(options.op)) % len(options.op)
                operators.append("%s" % (options.op[N]))
                executable_string += "%s %s" % (integers.format(NUMBER = i),  str(options.op[N]))
            executable_string += "%s" % (integers.format(NUMBER = options.operand_count[0] - 1))
            print(executable_string)
            exec(executable_string)
            print(intExpression.integer)

            for i in range(options.operand_count[0] - 1):
                exec("N = %s.integer" % (integers.format(NUMBER = i)))
                expression += "(%s) %s " % (N, operators[i])
            exec("N = %s.integer" % (integers.format(NUMBER =  (options.operand_count[0] - 1))))
            expression += "(%s)" % (N)
            expression += "\n"
            print(expression)
            expected_value = eval(expression)
            print(expected_value)
            print(intExpression.integer > MAX or intExpression.integer < MIN)
            N1 = random.randint(MIN,MAX)
            N2 = random.randint(MIN,MAX)
            N3 = random.randint(MIN,MAX)
            while(expected_value == N1 or expected_value == N2 or expected_value == N3):
                N1 = random.randint(MIN,MAX)
                N2 = random.randint(MIN,MAX)
                N3 = random.randint(MIN,MAX)
            false_values = "[(%s), (%s), (%s)]" % (str(N1), str(N2), str(N3))
            file.write("validate((%s), (%s), (%s));\n" % (expression, str(expected_value), false_values))

def main(options):
    generate_binary_tests(options)

if __name__ == "__main__":
    main(get_arguments())

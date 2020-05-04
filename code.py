the_expression = {'WHILE': 'while', 'IF': 'if', 'Do': 'do', 'ELSE': 'else', 'THEN': 'then', 'SKIP': 'skip',
 'Identifier': 'id', 'INT': 'int',
 'TRUE': 'true', 'FALSE': 'false', 'NOT': '¬',
 'addition': '+', 'subtraction': '-', 'multiplication': '*', 'division': '/',
  '∧': '^', '∨': 'v', '(': '(', ')': ')', ':=': ':=', '=': '=', '>': '>', '<': '<',
  '{': '{', '}': '}', 'Sim_Clone': ';', 'EOF': ''
}


WHILE, IF, DO, THEN, ELSE, SKIP, Identifier, INT, TRUE, FALSE, NOT, addition, subtraction, multiplication, division, AND, OR, Left_Parenthesis, Right_Parenthesis, Assigning, Equal_Sign, Greater_Than, Less_Than, Left_Brace, Right_Brace, Sim_Clone, EOF = (
    'WHILE', 'DO', 'IF', 'ELSE', 'THEN', 'SKIP', 'Identifier', 'INT', 'TRUE', 'FALSE', 'NOT', 'addition', 'subtraction', 'multiplication', 'division', '∧', '∨', '(', ')', ':=', '=', '>', '<', '{', '}', 'Sim_Clone', 'EOF'
)

ERROR = -999

class Interface():

    def __init__(self):
        pass

    def Touch(self, the_variable):
        raise ValueError("The Checking: ", type(self).__name__, ' it will be require to visit it')

    def configuration_define(self):
        pass


    def __str__(self):
        return 'node'

class Math_operations(Interface):

    def __init__(self, left, oper, right):
        self.left = left
        self.token = self.oper = oper
        self.right = right

    def Touch(self, the_variable, print_result):
        if self.oper.type == addition:
            return self.left.Touch(the_variable, print_result) + self.right.Touch(the_variable, print_result)
        elif self.oper.type == subtraction:
            return self.left.Touch(the_variable, print_result) - self.right.Touch(the_variable, print_result)
        elif self.oper.type == multiplication:
            return self.left.Touch(the_variable, print_result) * self.right.Touch(the_variable, print_result)
        elif self.oper.type == division:
            return self.left.Touch(the_variable, print_result) / self.right.Touch(the_variable, print_result)

    def __str__(self):
        return '(' + str(self.left) + self.oper.the_expression() + str(self.right) + ')'

class Boolean_exp(Interface):

    def __init__(self, left, oper, right):
        self.left = left
        self.token = self.oper = oper
        self.right = right

    def Touch(self, the_variable, print_result):
        if self.oper.type == Equal_Sign:
            return self.left.Touch(the_variable, print_result) == self.right.Touch(the_variable, print_result)
        elif self.oper.type == Less_Than:
            return self.left.Touch(the_variable, print_result) < self.right.Touch(the_variable, print_result)
        elif self.oper.type == Greater_Than:
            return self.left.Touch(the_variable, print_result) > self.right.Touch(the_variable, print_result)
        elif self.oper.type == AND:
            if self.left.Touch(the_variable, print_result) == False:
                return False
            else:
                return self.right.Touch(the_variable, print_result)
        elif self.oper.type == OR:
            if self.left.Touch(the_variable, print_result):
                return True
            else:
                return self.right.Touch(the_variable, print_result)
        elif self.oper.type == NOT:
            return not self.right.Touch(the_variable, print_result)

    def __str__(self):
        if self.left is None:
            return self.oper.the_expression() + str(self.right)
        else:
            return '(' + str(self.left) + self.oper.the_expression() + str(self.right) + ')'

class if_condition(Interface):

    def __init__(self, oper, the_status, right, wrong):
        self.left = the_status
        self.token = self.oper = oper
        self.right = right
        self.wrong = wrong

    def Touch(self, the_variable, print_result):
        actual_evaluation = self.left.Touch(the_variable, print_result)
        if actual_evaluation:
            return self.right
        else:
            return self.wrong

    def __str__(self):
        return 'if ' + str(self.left) + ' then { ' + str(self.right) + ' } else { ' + str(self.wrong) + " }"

class While_node_loop(Interface):

    def __init__(self, left, oper, right):
        self.left = left
        self.token = self.oper = oper
        self.right = right

    def Touch(self, the_variable, print_result):
        actual_evaluation = self.left.Touch(the_variable, print_result)

        if actual_evaluation:
            print_result(str(self.right), end=';')
            self.right.Touch(the_variable, print_result)
            self.right.configuration_define()
            print_result('skip', end=';')
            return self

        else:
            return None

    def configuration_define(self):
        pass


    def __str__(self):
        return 'while ' + str(self.left) + ' do { ' + str(self.right) + ' }'


class Complex_Node(Interface):

    def __init__(self, nodes):
        self.the_sblin = []
        for node in nodes:
            self.the_sblin.append(node)
        self.sbli = self.the_sblin.copy()
        self.sbling = 0

    def stringCheck(self):
        return '; '.join(str(node) for node in self.the_sblin)

    def Touch(self, the_variable, print_result):
        initialExperiment = True
        while self.the_sblin:
            n = 0
            if not initialExperiment:
                print_result(self.stringCheck(), end=';')
            initialExperiment = False
            node = self.the_sblin[n].Touch(the_variable, print_result)
            if node is None:
                self.the_sblin[n] = SkipingStep()
                if len(self.the_sblin) > 1:
                    print_result(self.stringCheck(), end=';')
                self.the_sblin.pop(n)
            else:
                self.the_sblin[0] = node
                if len(self.the_sblin) > 1:
                    print_result(self.stringCheck(), end=';')
        if len(self.the_sblin) > 0:
            return self

    def configuration_define(self):
        self.the_sblin = self.sbli.copy()
        self.sbling = 0

    def __str__(self):
        return '; '.join(str(node) for node in self.sbli)

class dynamic_nodes(Interface):

    def __init__(self, nodes):
        self.the_sblin = []
        for node in nodes:
            self.the_sblin.append(node)
        self.end = False

    def Touch(self, the_variable, print_result):
        node = self.the_sblin[0].Touch(the_variable, print_result)
        if self.end:
            return
        if node is None:
            self.the_sblin.pop(0)
            if len(self.the_sblin) == 0:
                print_result('skip', ',')
            else:
                print_result('skip', ';')
                print_result()
        else:
            self.the_sblin[0] = node
            print_result()
        if len(self.the_sblin) > 0:
            return self

    def __str__(self):
        return '; '.join(str(node) for node in self.the_sblin)
    
class TouchClass(Interface):

    def __init__(self, token):
        self.token = token
        self.value = token.value

    def Touch(self, the_variable, print_result):
        variables = self.value
        the_value = the_variable.get(variables)
        if the_value is None:
            return 0
        else:
            return the_value

    def __str__(self):
        return str(self.value)


class First_one(Interface):

    def __init__(self, token):
        self.token = token
        self.value = token.value

    def Touch(self, the_variable, print_result):
        return self.value

    def __str__(self):
        return str(self.value)


class SkipingStep(Interface):

    def __init__(self):
        pass

    def Touch(self, the_variable, print_result):
        pass

    def __str__(self):
        return 'skip'

class Boolean_Evaluation(Interface):

    def __init__(self, token):
        self.token = token

    def Touch(self, the_variable, print):
        if self.token.type == TRUE:
            return True
        else:
            return False
        
    def __str__(self):
        return self.token.the_expression()


class Assigning(Interface):

    def __init__(self, left, oper, right):
        self.left = left
        self.token = self.oper = oper
        self.right = right

    def Touch(self, the_variable, print_result):
        variables = self.left.value
        the_variable[variables] = self.right.Touch(the_variable, print_result)

    def __str__(self):
        return str(self.left) + ' := ' + str(self.right)


class TokenObject(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return the_expression[self.type]

    def the_expression(self):
        return the_expression[self.type]

    def __repr__(self):
        return self.__str__()


class LexerObject(object):

    def __init__(self, following_step):
        self.tokens = following_step.split(' ')
        self.tokens = [table for table in self.tokens if table != '']
        self.region = 0
        self.token = self.tokens[self.region]

    def migrate(self):
        self.region += 1
        if self.region > len(self.tokens) - 1:
            self.token = None
        else:
            self.token = self.tokens[self.region]

    def IsTokenInteger(self, token):
        try:
            rawnd = int(token)
            return True
        except:
            return False

    def getNextToken(self):

        while self.token is not None:
            if self.token == '':
                self.region += 1
                continue

            if self.token == 'while':
                self.migrate()
                return TokenObject(WHILE, 'while')
            if self.token == 'do':
                self.migrate()
                return TokenObject(DO, 'do')

            if self.token == 'if':
                self.migrate()
                return TokenObject(IF, 'if')
            if self.token == 'then':
                self.migrate()
                return TokenObject(THEN, 'then')
            if self.token == 'else':
                self.migrate()
                return TokenObject(ELSE, 'else')

            if self.token == 'skip':
                self.migrate()
                return TokenObject(SKIP, 'skip')

            if self.IsTokenInteger(self.token):
                getTokenVal = TokenObject(INT, int(self.token))
                self.migrate()
                return getTokenVal

            if self.token == '∧':
                self.migrate()
                return TokenObject(AND, '∧')

            if self.token == '+':
                self.migrate()
                return TokenObject(addition, '+')

            if self.token == '-':
                self.migrate()
                return TokenObject(subtraction, '-')

            if self.token == '*':
                self.migrate()
                return TokenObject(multiplication, '*')

            if self.token == '/':
                self.migrate()
                return TokenObject(division, '/')

            if self.token == '∨':
                self.migrate()
                return TokenObject(OR, '∨')

            if self.token == '(':
                self.migrate()
                return TokenObject(Left_Parenthesis, '(')

            if self.token == ')':
                self.migrate()
                return TokenObject(Right_Parenthesis, ')')

            if self.token == ';':
                self.migrate()
                return TokenObject(Sim_Clone, ';')

            if self.token == ':=':
                self.migrate()
                return TokenObject(Assigning, ':=')

            if self.token == '{':
                self.migrate()
                return TokenObject(Left_Brace, '{')

            if self.token == '}':
                self.migrate()
                return TokenObject(Right_Brace, '}')

            if self.token == '>':
                self.migrate()
                return TokenObject(Greater_Than, '>')

            if self.token == '<':
                self.migrate()
                return TokenObject(Less_Than, '<')

            if self.token == 'false':
                self.migrate()
                return TokenObject(FALSE, 'false')

            if self.token == '¬':
                self.migrate()
                return TokenObject(NOT, '¬')


            if self.token == '=':
                self.migrate()
                return TokenObject(Equal_Sign, '=')

            if self.token == 'true':
                self.migrate()
                return TokenObject(TRUE, 'true')


            if self.token.isidentifier():
                tk = TokenObject(Identifier, self.token)
                self.migrate()
                return tk


            raise Exception('Invalid character: "' + self.token + '"')

        return TokenObject(EOF, None)


class ParserObject(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = self.lexer.getNextToken()


    def tokenCheck(self, token_type):
        if self.token.type == token_type:
            self.token = self.lexer.getNextToken()
        else:
            raise Exception('syntax is not correct', token_type)

    def factory(self):
        token = self.token
        if token.type == INT:
            self.tokenCheck(INT)
            return First_one(token)
        elif token.type == Identifier:
            self.tokenCheck(Identifier)
            return TouchClass(token)
        elif token.type == Left_Parenthesis:
            self.tokenCheck(Left_Parenthesis)
            node = self.Expresssion()
            self.tokenCheck(Right_Parenthesis)
            return node
        else:
            return None

    def GetFunctionVariable(self):
        var_node = TouchClass(self.token)
        self.tokenCheck(Identifier)
        return var_node


    def FunctionTerm(self):
        node = self.factory()

        if node is None:
            return None

        while self.token.type in (multiplication, division):
            token = self.token
            if token.type == multiplication:
                self.tokenCheck(multiplication)
            elif token.type == division:
                self.tokenCheck(division)

            node = Math_operations(left=node, oper=token, right=self.factory())

        return node


    def FunctionSkip(self):
        self.tokenCheck(SKIP)
        return SkipingStep()


    def Expresssion(self):
        node = self.FunctionTerm()

        if node is None:
            return None

        while self.token.type in (addition, subtraction):
            token = self.token
            if token.type == addition:
                self.tokenCheck(addition)
            elif token.type == subtraction:
                self.tokenCheck(subtraction)

            node = Math_operations(left=node, oper=token, right=self.FunctionTerm())

        return node

    def Assignment(self):
        left = self.GetFunctionVariable()
        token = self.token
        self.tokenCheck(Assigning)
        right = self.Expresssion()
        node = Assigning(left, token, right)
        return node

    def ConditionExpression(self):
        node = self.Expresssion()
        if node is not None:
            return node, False
        else:
            node = self.BoolExpression()
            return node, True


    def BoolExpression(self):
        node = self.BoolExpressionTerm()
        while self.token.type == OR:
            token = self.token
            if token.type == OR:
                self.tokenCheck(OR)
            node = Boolean_exp(left=node, oper=token, right=self.BoolExpressionTerm())
        return node

    def BoolExpressionTerm(self):
        node = self.BoolExpressionFactor()
        while self.token.type in (AND):
            token = self.token
            if token.type == AND:
                self.tokenCheck(AND)

            node = Boolean_exp(left=node, oper=token, right=self.BoolExpressionFactor())
        return node

    def MatchComparison(self, left):
        token = self.token
        if token.type == Equal_Sign:
            self.tokenCheck(Equal_Sign)
        elif token.type == Less_Than:
            self.tokenCheck(Less_Than)
        elif token.type == Greater_Than:
            self.tokenCheck(Greater_Than)
        right = self.Expresssion()
        node = Boolean_exp(left, token, right)
        return node

    def BoolExpressionFactor(self):
        token = self.token
        if self.token.type == TRUE or \
           self.token.type == FALSE:
            node = Boolean_Evaluation(self.token)
            self.tokenCheck(self.token.type)
            return node
        elif token.type == NOT:
            self.tokenCheck(NOT)
            right = self.BoolExpressionFactor()
            node = Boolean_exp(None, token, right)
            return node
        elif token.type == Left_Parenthesis:
            self.tokenCheck(Left_Parenthesis)
            node, isBool = self.ConditionExpression()
            if self.token.type == Right_Parenthesis:
                self.tokenCheck(Right_Parenthesis)
                seen_end_paren = True
            else:
                seen_end_paren = False
            if not isBool:
                node = self.MatchComparison(node)
            while self.token.type == OR or \
                  self.token.type == AND:
                self.tokenCheck(self.token.type)
                node = Boolean_exp(left=node, oper=token, right = self.BoolExpressionTerm())
            if not seen_end_paren:
                self.tokenCheck(Right_Parenthesis)
            return node
        else:
            left = self.Expresssion()
            node = self.MatchComparison(left)
            return node

    def IfcondtionStatment(self):
        self.tokenCheck(IF)
        left = self.BoolExpression()
        token = self.token
        if self.token.type == TRUE:
            raise ValueError("it will not reach if there")
            self.tokenCheck(TRUE)
        elif self.token.type == FALSE:
            raise ValueError("this part is an error if")
            self.tokenCheck(FALSE)
        elif self.token.type == Left_Parenthesis:
            pass
        self.tokenCheck(THEN)
        right = self.singleStatement()
        self.tokenCheck(ELSE)
        wrong = self.singleStatement()
        node = if_condition(token, left, right, wrong)
        return node

    def WhileStatement(self):
        self.tokenCheck(WHILE)
        left = self.BoolExpression()

        token = self.token
        if self.token.type == TRUE:
            raise ValueError("while will not be reach")
            self.tokenCheck(TRUE)
        elif self.token.type == FALSE:
            raise ValueError("There is an error in while")
            self.tokenCheck(FALSE)
        self.tokenCheck(DO)
        if self.token.type == Left_Brace:
            self.tokenCheck(Left_Brace)
            right = self.StatementList()
            self.tokenCheck(Right_Brace)
        else:
            right = self.singleStatement()
        node = While_node_loop(left, token, right)
        return node


    def StatementList(self):
        node = self.singleStatement()

        results = [node]

        while self.token.type == Sim_Clone:
            self.tokenCheck(Sim_Clone)
            results.append(self.singleStatement())
        newr = []
        for node in results:
            if isinstance(node, Complex_Node):
                newr.extend(node.the_sblin)
            else:
                newr.append(node)

        results = newr

        if self.token.type == Identifier:
            raise Exception('Invalid syntax, unexpected Identifier', self.token)

        if len(results) > 1:
            node = Complex_Node(results)
            return node
        else:
            if isinstance(results[0], SkipingStep):
                return results[0]
            else:
                return Complex_Node(results)


    def ProgramStatement(self):
        node = self.singleStatement()

        results = [node]

        while self.token.type == Sim_Clone:
            self.tokenCheck(Sim_Clone)
            results.append(self.singleStatement())
        newr = []
        for node in results:
            if isinstance(node, Complex_Node):
                newr.extend(node.the_sblin)
            else:
                newr.append(node)

        results = newr

        if self.token.type == Identifier:
            raise Exception('Invalid syntax!', self.token)

        if len(results) > 1:
            node = dynamic_nodes(results)
            return node
        else:
            if isinstance(results[0], SkipingStep):
                return results[0]
            else:
                return dynamic_nodes(results)


    def singleStatement(self):
        if self.token.type == Identifier:
            node = self.Assignment()
        elif self.token.type == WHILE:
            node = self.WhileStatement()
        elif self.token.type == IF:
            node = self.IfcondtionStatment()
        elif self.token.type == SKIP:
            node = self.FunctionSkip()
        elif self.token.type == Left_Brace:
            self.tokenCheck(Left_Brace)
            node = self.StatementList()
            self.tokenCheck(Right_Brace)
        else:
            node = self.Expresssion()
        return node

    def parse(self):
        return self.ProgramStatement()



class InterpreterObject(object):

    def __init__(self, parser):
        self.The_TABLE = {}
        self.parser = parser
        self.tree = None
        self.stepCt = 0

    def start(self):
        self.stepCt = 0
        self.tree = self.parser.parse()
        while self.tree is not None:
            self.tree = self.tree.Touch(self.The_TABLE, self.printStep)
            
    def printTable(self):
        table_output = "{"
        for key, value in sorted(self.The_TABLE.items()):
            table_output = table_output + '{} → {}, '.format(key, value)
        if len(self.The_TABLE) >= 1:
            table_output = table_output.rstrip()[:-1] + "}"
        else:
            table_output = table_output.rstrip() + "}"
        print(table_output)
        
    def printStep(self, step='', end=','):
        self.stepCt += 1
        if self.tree is not None:
            if self.stepCt > 10000:
                self.tree.end = True
                self.tree.the_sblin = []
                self.tree = None
                return
            print('⇒ ', end='')
            if step:
                print(step, end=end + ' ')
            treestr = str(self.tree)
            if treestr:
                print(treestr, end=', ')
            self.printTable()


def main():
    while True:
        try:
            try:
                command_string = raw_input('')
            except NameError:
               command_string = input('')
        except EOFError:
            break
        if not command_string:
            continue
            
        command_string = command_string.replace('-', ' -')
        spaceCharacters = '()=,:;{}*+/<>¬∧∨'
        non_space = {':  =': ':='}

        for ch in spaceCharacters:
            command_string = command_string.replace(ch, ' ' + ch + ' ')

        for conspace, sinspace in non_space.items():
            command_string = command_string.replace(conspace, sinspace)

        lexerInstance = LexerObject(command_string)
        parserInstance = ParserObject(lexerInstance)
        interpreter = InterpreterObject(parserInstance)
        interpreter.start()



if __name__ == '__main__':
    main()

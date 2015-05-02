#Art Grichine
#Zeed Jarrah
#ArtGrichine@csu.fullerton.edu
#ZJarrah@csu.fullerton.edu
#Syntax Analyser (Assignment 2)
#Requires Python version > 2.5 because of use of ternary operations

import sys
import queue
import Lexer
from Lexer import Lex
from collections import deque

####################
##Global Variables##
####################
_printcmd = False            #toggles print to command terminal feature for the SA production
_printfile = True            #toggles print to filehandle feature for the SA production
toProcess = deque()
current = Lex()
peek_next = Lex()
_filename = None
outputFileHandle = None
_error = True
    
#reset global variables
def reset():
    global toProcess                    #initilize toProcess variable as global so we can change it
    global outputFileHandle
    global _filename
    global peek_next
    global current
    global _error
    
    toProcess = deque()
    outputFileHandle = None
    _filename = None
    peek_next = Lex()
    current = Lex()
    _error = True

#when an error is found, the expected variable is sent here and error is reported
def error(expected):
    global _error
        
    print('\nERROR line: {1}\nExpected: {0}'.format(expected, current.line))
    print('Current lexeme: {}'.format(current.lexeme))
    print('Current token: {}'.format(current.token))
    
    if _printfile:
        print('\nERROR line: {1}\nExpected: {0}'.format(expected, current.line), file = outputFileHandle)
        print('Current lexeme: {}'.format(current.lexeme), file = outputFileHandle)
        print('Current token: {}'.format(current.token), file = outputFileHandle)
    
    _error = False
   
#set outputFileHandle 
def setFileHandle():
    #tell python we willingly want to change the global variable outputFileHandle
    global outputFileHandle
    outputFileHandle = open(_filename + '.SA','w')
    
#set current to the next variable to process
def getNext():
    global current                          #access the current global variable

    if toProcess:                           #if not empty
        current = toProcess.popleft()
        printInfo()

#used to peek at the next variable in toProcess
def peek():
    global peek_next                        #access the peek_next global variable
    if toProcess:
        peek_next = toProcess[0]

#print information about the token and lexeme. Reports ERROR if current is empty
def printInfo():
    if current.token:
        if _printcmd:
            print('Token: {0:14} Lexeme: {1:14} Line: {2:1}'.format(current.token, current.lexeme, current.line))
        if _printfile:
            print('Token: {0:14} Lexeme: {1:14} Line: {2:1}'.format(current.token, current.lexeme, current.line), file = outputFileHandle)
    else:
        if _printcmd:
            print('ERROR: current is empty')
        if _printfile:
            print('ERROR: current is empty', file = outputFileHandle)

############################    
####  Production Rules  ####
############################
#<Rat15S>  ::=   <Opt Function Definitions>  @@  <Opt Declaration List> @@  <Statement List> 
def rat15S():
    #initial production
    if _printcmd:
        print('<Rat15S>  ::=   <Opt Function Definitions>  @@  <Opt Declaration List> @@  <Statement List> ')
    if _printfile:
        print('<Rat15S>  ::=   <Opt Function Definitions>  @@  <Opt Declaration List> @@  <Statement List> ', file = outputFileHandle)
    
    optFunctionDefinitions()
    
    if current.lexeme == '@@':
        getNext()
        optDeclarationList()
        
        if current.lexeme == '@@':
            getNext()
            #continue until EOF
            while True:
                statementList()
                if not toProcess:
                    break
        
        else:
            error('@@')
        
    else:
        error('@@')

#<Opt Function Definitions> ::= <Function Definitions> | <Empty>
def optFunctionDefinitions():
    if _printcmd:
        print('<Opt Function Definitions> ::= <Function Definitions> | <Empty>')
    if _printfile:
        print('<Opt Function Definitions> ::= <Function Definitions> | <Empty>', file = outputFileHandle) 
    
    if current.lexeme == 'function':
        functionDefinitions()
    elif current.token == 'unknown':
        error('<Function Definitions> | <Empty>')
    else:
        empty()   

#<Function Definitions>  ::= <Function> | <Function> <Function Definitions>   
def functionDefinitions():
    if _printcmd:
        print('<Function Definitions> ::= <Function> | <Function> <Function Definitions>')
    if _printfile:
        print('<Function Definitions> ::= <Function> | <Function> <Function Definitions>', file = outputFileHandle)
    
    #continue gathering function definitions until there are no more to report
    while True:
        function()
        if current.lexeme != 'function':
            break

#<Function> ::= function  <Identifier> [ <Opt Parameter List> ] <Opt Declaration List>  <Body>
def function():
    if _printcmd:
        print('<Function> ::= function  <Identifier> [ <Opt Parameter List> ] <Opt Declaration List>  <Body>')
    if _printfile:
        print('<Function> ::= function  <Identifier> [ <Opt Parameter List> ] <Opt Declaration List>  <Body>', file = outputFileHandle)
    
    #function
    if current.lexeme == 'function':
        getNext()
    
        #<Identifier>
        if current.token == 'identifier':
            getNext()
            
            # [
            if current.lexeme == '[':
                getNext()
                optParameterList()
                
                if current.lexeme == ']':
                    getNext()
                    optDeclarationList()
                    body()

                else:
                    error(']')
            
            else:
                error('[')
        
        else:
            error('<Identifier>')
    
    else:
        error('function')

# <Opt Parameter List> ::=  <Parameter List>   |  <Empty>
def optParameterList():
    if _printcmd:
        print('<Opt Parameter List> ::=  <Parameter List> | <Empty>')
    if _printfile:
        print('<Opt Parameter List> ::=  <Parameter List> | <Empty>', file = outputFileHandle)
    
    if current.token == 'identifier':
        parameterList()
    elif current.token == 'unknown':
        error('<Parameter List> | <Empty>')
    else:
        empty()

# <Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>
def parameterList():
    if _printcmd:
        print('<Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>')
    if _printfile:
        print('<Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>', file = outputFileHandle)
    
    parameter()
    
    if peek_next.lexeme == ',':
        getNext()
        parameterList()

# <Parameter> ::=  < IDs > : <Qualifier>
def parameter():
    if _printcmd:
        print('<Parameter> ::=  < IDs > : <Qualifier>')
    if _printfile:
        print('<Parameter> ::=  < IDs > : <Qualifier>', file = outputFileHandle)
    
    if current.token == 'identifier':
        getNext()
        
        if current.lexeme == ':':
            getNext()
            qualifier()
        
        else:
            error('<Qualifier>')
        
    else:
        error('< IDs >')


# <Qualifier> ::= int | boolean | real
def qualifier():
    if _printcmd:
        print('<Qualifier> ::= int | boolean | real')
    if _printfile:
        print('<Qualifier> ::= int | boolean | real', file = outputFileHandle)
    
    if current.lexeme == 'int' or current.lexeme == 'boolean' or current.lexeme == 'real':
        getNext()
    else:
        error('int | boolean | real')

# <Body>  ::=  {  < Statement List>  }
def body():
    if _printcmd:
        print('<Body>  ::=  {  < Statement List>  }')
    if _printfile:
        print('<Body>  ::=  {  < Statement List>  }', file = outputFileHandle)
    
    if current.lexeme == '{':
        getNext()
        statementList()
        
        getNext() if current.lexeme == '}' else error('}')
    
    else:
        error('{')

# <Opt Declaration List> ::= <Declaration List> | <Empty>
def optDeclarationList():
    if _printcmd:
        print('<Opt Declaration List> ::= <Declaration List> | <Empty>')
    if _printfile:
        print('<Opt Declaration List> ::= <Declaration List> | <Empty>', file = outputFileHandle)
    
    #check for qualifier
    if current.lexeme == 'int' or current.lexeme == 'boolean' or current.lexeme == 'real':
        declarationList()
    elif current.token == 'unknown':
        error('<<Declaration List> | <Empty>')
    else:
        empty()

# <Declaration List> := <Declaration> ; | <Declaration> ; <Declaration List>
def declarationList():
    if _printcmd:
        print('<Declaration List> := <Declaration> ; | <Declaration> ; <Declaration List>')
    if _printfile:
        print('<Declaration List> := <Declaration> ; | <Declaration> ; <Declaration List>', file = outputFileHandle)
    
    declaration()
    
    if current.lexeme == ';':
        getNext()
        #check if the next is a <Declaration List> by seeing if it's a qualifier --> int, boolean, real
        if current.lexeme == 'int' or current.lexeme == 'boolean' or current.lexeme == 'real':
            declarationList()
    else:
        error(';')

# <Declaration> ::=  <Qualifier > <IDs>
def declaration():
    if _printcmd:
        print('<Declaration> ::= <Qualifier> <IDs>')
    if _printfile:
        print('<Declaration> ::= <Qualifier> <IDs>', file = outputFileHandle)
    
    qualifier()
    ids()


# <IDs> ::=  <Identifier> | <Identifier>, <IDs>
def ids():
    if _printcmd:
        print('<IDs> ::=  <Identifier> | <Identifier>, <IDs>')
    if _printfile:
        print('<IDs> ::=  <Identifier> | <Identifier>, <IDs>', file = outputFileHandle)

    if current.token == 'identifier':
        getNext()
        
        #<Identifier>, <IDs>    break when no ',' after the identifier
        while True:
            if current.lexeme == ',':
                getNext()
                
                getNext() if current.token == 'identifier' else error('<Identifier>')
                    
            else:
                break
    else:
        error('<identifier>')

# <Statement List> ::= <Statement> | <Statement> <Statement List>
def statementList():
    if _printcmd:
        print('<Statement List> ::= <Statement> | <Statement> <Statement List>')
    if _printfile:
        print('<Statement List> ::= <Statement> | <Statement> <Statement List>', file = outputFileHandle)
    
    while True:
        statement()
        #must test to see if possible statement. Will test for compound, assign, if, return, write,
        #  read, while. If there is another statement then continue loop, otherwise break
        if current.lexeme != '{' and current.token != 'identifier' and current.lexeme != 'if' and current.lexeme != 'return' and current.lexeme != 'write' and current.lexeme != 'read' and current.lexeme != 'while':
            break

# <Statement> ::=  <Compound> | <Assign> | <If> |  <Return> | <Write> | <Read> | <While>
def statement():
    if _printcmd:
        print('<Statement> ::=  <Compound> | <Assign> | <If> |  <Return> | <Write> | <Read> | <While>')
    if _printfile:
        print('<Statement> ::=  <Compound> | <Assign> | <If> |  <Return> | <Write> | <Read> | <While>', file = outputFileHandle)
    
    #compound starts with '{' so we test for compound by looking for '{' lexeme in current
    if current.lexeme == '{':
        compound()
    #assign starts with an identifier, test for assign by checking if 'identifier' token in current
    elif current.token == 'identifier':
        assign()
    #if operations all start with 'if', check current lexeme for 'if'
    elif current.lexeme == 'if':
        _if()
    #return operators start with return, check current lexeme for 'return'
    elif current.lexeme == 'return':
        _return()
    #write begins with write, check current lexeme for 'write'
    elif current.lexeme == 'write':
        write()
    #read begins with read, check current lexeme for 'read'
    elif current.lexeme == 'read':
        read()
    #while begins with while, check current lexeme for 'while'
    elif current.lexeme == 'while':
        _while()
    else:
        error('<Compound> | <Assign> | <If> |  <Return> | <Write> | <Read> | <While>')

# <Compound> ::= {  <Statement List>  }
def compound():
    if _printcmd:
        print('<Compound> ::= {  <Statement List>  }')
    if _printfile:
        print('<Compound> ::= {  <Statement List>  }', file = outputFileHandle)
    
    if current.lexeme == '{':
        getNext()
        statementList()
        
        getNext() if current.lexeme == '}' else error('}')
        
        
    else:
        error('{')

# <Assign> ::=   <Identifier> := <Expression> ;
def assign():
    if _printcmd:
        print('<Assign> ::=   <Identifier> := <Expression> ;')
    if _printfile:
        print('<Assign> ::=   <Identifier> := <Expression> ;', file = outputFileHandle)
    
    if current.token == 'identifier':
        getNext()
    
        if current.lexeme == ':=':
            getNext()
            expression()
        
            getNext() if current.lexeme == ';' else error(';')
                
        else:
            error(':=')
    
    else:
        error('<Identifier>')

# <If> ::= if ( <Condition> ) <Statement> endif | if ( <Condition>  ) <Statement> else <Statement> endif
def _if():
    if _printcmd:
        print('<If> ::= if ( <Condition> ) <Statement > <ifPrime>')
    if _printfile:
        print('<If> ::= if ( <Condition> ) <Statement > <ifPrime>', file = outputFileHandle)
    
    if current.lexeme == 'if':
        getNext()
        
        if current.lexeme == '(':
            getNext()
            condition()
            
            if current.lexeme == ')':
                getNext()
                statement()
                ifPrime()
            else:
                error(')')
        
        else:
            error('(')
    
    else:
        error('if')

# <ifPrime> ::= endif | else <Statement> endif
def ifPrime():
    if _printcmd:
        print('<ifPrime> ::= endif | else <Statement> endif')
    if _printfile:
        print('<ifPrime> ::= endif | else <Statement> endif', file = outputFileHandle)
    
    if current.lexeme == 'endif':
        getNext()
    elif current.lexeme == 'else':
        getNext()
        statement()
        getNext() if current.lexeme == 'endif' else error('endif')
    else:
        error('endif | else')
        


# <Return> ::=  return ; |  return <Expression> ;
def _return():
    if _printcmd:
        print('<Return> ::=  return ; |  return <Expression> ;')
    if _printfile:
        print('<Return> ::=  return ; |  return <Expression> ;', file = outputFileHandle)
    
    peek()
    
    #condition 1:   return ;  
    if peek_next.lexeme == ';':
        
        if current.lexeme == 'return':
            getNext()   
        
            getNext() if current.lexeme == ';' else error(';')
        
        else:
            error('return')
    
    #condition 2:   return <Expression> ;
    else:
        if current.lexeme == 'return':
            getNext()
            # print('\nIM IN OF EXPRESSION()\n')
            expression()
            # print('\nIM OUT OF EXPRESSION()\n')
            getNext() if current.lexeme == ';' else error(';')
            
        else:
            error('return')
        

# <Write> ::=   write ( <Expression>);
def write():
    if _printcmd:
        print('<Write> ::=   write ( <Expression>);')
    if _printfile:
        print('<Write> ::=   write ( <Expression>);', file = outputFileHandle)
    
    if current.lexeme == 'write':
        getNext()
        
        if current.lexeme == '(':
            getNext()
            expression()
        
            if current.lexeme == ')':
                getNext()
                    
                getNext() if current.lexeme == ';' else error(';')
                
            else:
                error(')')
        
        else:
            error('<Expression>')
    
    else:
        error('write')

# <Read> ::= read ( <IDs> );
def read():
    if _printcmd:
        print('<Read> ::= read ( <IDs> );')
    if _printfile:
        print('<Read> ::= read ( <IDs> );', file = outputFileHandle)
    
    if current.lexeme == 'read':
        getNext()
        
        if current.lexeme == '(':
            getNext()
            ids()
            
            if current.lexeme == ')':
                getNext()
                
                getNext() if current.lexeme == ';' else error(';')
                
            else:
                error(')')
            
        else:
            error('(')
    
    else:
        error('read')

# <While> ::= while ( <Condition>  )  <Statement>
def _while():
    if _printcmd:
        print('<While> ::= while ( <Condition>  )  <Statement>')
    if _printfile:
        print('<While> ::= while ( <Condition>  )  <Statement>', file = outputFileHandle)
    
    if current.lexeme == 'while':
        getNext()
        
        if current.lexeme == '(':
            getNext()
            condition()
            
            if current.lexeme == ')':
                getNext()
                statement()
            else:
                error(')')
        
        else:
            error('(')
        
    else:
        error('while')

# <Condition> ::= <Expression> <Relop> <Expression>
def condition():
    if _printcmd:
        print('<Condition> ::= <Expression> <Relop> <Expression>')
    if _printfile:
        print('<Condition> ::= <Expression> <Relop> <Expression>', file = outputFileHandle)
    
    expression()
    relop()
    expression()

# <Relop> ::=   = |  !=  |   >   | <   |  =>   | <=
def relop():
    if _printcmd:
        print('<Relop> ::=   = |  !=  |   >   | <   |  =>   | <=')
    if _printfile:
        print('<Relop> ::=   = |  !=  |   >   | <   |  =>   | <=', file = outputFileHandle)
    
    if current.lexeme == '=' or current.lexeme == '!=' or current.lexeme == '>' or current.lexeme == '<' or current.lexeme == '=>' or current.lexeme == '<=':
        getNext()
    else:
        error('= |  !=  |   >   | <   |  =>   | <=') 

# <Expression> ::= <Term> <ExpressionPrime>
def expression():
    if _printcmd:
        print('<Expression> ::= <Term> <ExpressionPrime>')
    if _printfile:
        print('<Expression> ::= <Term> <ExpressionPrime>', file = outputFileHandle)
    
    term()
    expressionPrime()

# <ExpressionPrime> ::= + <Term> <ExpressionPrime> | - <Term> <ExpressionPrime> | <empty>
def expressionPrime():
    if _printcmd:
        print('<ExpressionPrime> ::= + <Term> <ExpressionPrime> | - <Term> <ExpressionPrime> | <empty>')
    if _printfile:
        print('<ExpressionPrime> ::= + <Term> <ExpressionPrime> | - <Term> <ExpressionPrime> | <empty>', file = outputFileHandle)
    
    if current.lexeme == '+' or current.lexeme == '-':
        getNext()
        term()
        expressionPrime()
    elif current.token == 'unknown':
        error('+, -, <empty>')    
    else:
        empty()


# <Term> ::= <Factor> <TermPrime>
def term():
    if _printcmd:
        print('<Term> ::= <Factor> <TermPrime>')
    if _printfile:
        print('<Term> ::= <Factor> <TermPrime>', file = outputFileHandle)
    
    factor()
    termPrime()

# <TermPrime> ::= * <Factor> <TermPrime> | / <Factor> <TermPrime> | <empty>
def termPrime():
    if _printcmd:
        print('<TermPrime> ::= * <Factor> <TermPrime> | / <Factor> <TermPrime> | <empty>')
    if _printfile:
        print('<TermPrime> ::= * <Factor> <TermPrime> | / <Factor> <TermPrime> | <empty>', file = outputFileHandle)
    
    if current.lexeme == '*' or current.lexeme == '/':
        getNext()
        factor()
        termPrime()
    elif current.token == 'unknown':
        error('*, /, <empty>')    
    else:
        empty()    



# <Factor> ::= - <Primary> | <Primary>
def factor():
    if _printcmd:
        print('<Factor> ::= - <Primary> | <Primary>')
    if _printfile:
        print('<Factor> ::= - <Primary> | <Primary>', file = outputFileHandle)
    
    if current == '-':
        getNext()
        primary()
    else:
        primary()
        
# <Primary> ::= <Identifier> | <Integer> | <Identifier> [<IDs>] | ( <Expression> ) | <Real> | true | false
def primary():
    if _printcmd:
        print('<Primary> ::= <Identifier> | <Integer> | <Identifier> [<IDs>] | ( <Expression> ) | <Real> | true | false')
    if _printfile:
        print('<Primary> ::= <Identifier> | <Integer> | <Identifier> [<IDs>] | ( <Expression> ) | <Real> | true | false', file = outputFileHandle)

    if current.token == 'identifier':
        getNext()
        #must test if <Identifier> [<IDs>], if no bracket then its just an identifier
        if current.lexeme == '[':
            getNext()
            ids()
            getNext() if current.lexeme == ']' else error(']')

    #    <Integer>
    elif current.token == 'integer':
        getNext()
        
    #    ( <Expression> ) 
    elif current.lexeme == '(':
        getNext()
        expression()
        getNext() if current.lexeme == ')' else error(')')

    #     <Real>        
    elif current.token == 'real':
        getNext()
    #     true
    elif current.lexeme == 'true':
        getNext()
    #     false
    elif current.lexeme == 'false':
        getNext()
    
    #else does not meet primary requirements
    else:
        error('<Identifier> | <Integer> | <Identifier> [<IDs>] | ( <Expression> ) |  <Real>  | true | false')
        

# <Empty> ::= ε
def empty():
    if _printcmd:
        print('<Empty> ::= epsilon')
    if _printfile:
        print('<Empty> ::= epsilon', file = outputFileHandle)


#purpose: Drive Syntax Analyser
def main():
    #initialize variables
    tokens = []
    lexemes = []
    
    #global init lets us change the global variable
    global toProcess                    
    global _filename

    #main loop will go until the user is finished
    while True:
        #reset global variables after loop
        reset()
        
        #call lexer
        #returned from Lexer.main() is deque containing lexers and filename of processed file
        toProcess, _filename = Lexer.main()             
        
        #if there is contents in toProcess (sent from Lexer.main()), proceed to Syntax Analyser
        if toProcess:   
            #set the output filehandle so that we can print to a file  
            setFileHandle()
            
            #Syntax Analyser
            print('\nSyntax Analyser running...')
            getNext()                                       #get input
            rat15S()                                        #call Syntax Analyser
            print('\n...Syntax Analyser finished!\n')
            
            #report to user if error or no error in syntax analysis
            print('There were no errors!') if _error else print('An error was found!')
            
            #report to user where the contents of the file have been saved
            print('Your syntactic analysis of {} has been saved as {} in the working directory.'.format(_filename,_filename + '.SA'))
        
        #ask user if they would like to run another file    
        _continue = input('\nWould you like to process another file? (yes/no): ')
        if _continue == 'no' or _continue == 'quit':
            print('Goodbye!')
            sys.exit()

if __name__ == '__main__':
    main()
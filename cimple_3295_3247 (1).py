#Amalia Naka, 3295, cse63295
#Athanasios Katsiliris, 3247, cse63247

import sys

f = sys.argv[1]

file = open(f,"r")


line = 1

digits = ['0','1','2','3','4','5','6','7','8','9','0']

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


commited_words = ["program","if","switchcase","not","function","input",
					"declare","else","forcase","and","procedure","print",
					"while","incase","or","call","case","return","default",
					"in","inout"]
                    

countList = []
countListA = []

gl_formal_list = []
gl_actual_list = []

temp_var_list = []

variable_list = []

prog_name = ""

scopesList = []

top_sc = []

ret_flag = 0

entity_list_toCheck = []

assembleNum = 0

flag = 0

arg_count = -1

r_true = []
b_true = []
q_true = []
r_false = []
b_false = []
q_false = []

subprogSign = False 
 
state0 = 0      # starting state
state1 = 1      # alpharithmetic state
state2 = 2      # numeric constant state
state3 = 3      # comparison: < state
state4 = 4      # comparison: > state
state5 = 5      # : state
state6 = 6      # comments state


state_err1 = -100
state_err2 = -200
state_err3 = -300
state_err4 = -400
state_err5 = -500

final_state_identifier = 100
final_state_numerical = 101
final_state_addition = 102
final_state_multiplication = 103
final_state_subtraction = 104
final_state_division = 105
final_state_lesser = 106
final_state_lesser_or_equal = 107
final_state_unequal = 108
final_state_greater = 109
final_state_greater_or_equal = 110
final_state_equality = 111
final_state_assignment = 112
final_state_comma = 113
final_state_semicolon = 114
final_state_LPar = 115
final_state_RPar = 116
final_state_L_bracket = 119
final_state_R_bracket = 120
final_state_L_bracket2 = 121
final_state_R_bracket2 = 122
final_state_full_stop = 123
final_state_EOF = 124


hashtag = 0
blank_char = 1
EOF = 2
let = 3
nums = 4
addition = 5
multiplication = 6
subtract = 7
division = 8
lesser = 9
greater = 10
equality = 11
colon = 12
question_mark = 13
comma = 14
RP = 15     # ')'
LP = 16
R_bracket = 17 # ']'
L_bracket = 18
R_bracket2 = 19 # '}'
L_bracket2 = 20
full_stop = 21
newline = 22
illegal_sym = 23


state_array = [
        [state6,state0,final_state_EOF,state1,state2,final_state_addition,final_state_multiplication,final_state_subtraction,
        final_state_division,state3,state4,final_state_equality,state5,final_state_semicolon,final_state_comma,final_state_RPar,
        final_state_LPar,final_state_R_bracket,final_state_L_bracket,final_state_R_bracket2,final_state_L_bracket2,final_state_full_stop,
        state0,state_err1],
        
        
        [final_state_identifier,final_state_identifier,final_state_identifier,state1,state1,final_state_identifier,final_state_identifier,
        final_state_identifier,final_state_identifier,final_state_identifier,final_state_identifier,final_state_identifier,final_state_identifier,
        final_state_identifier,final_state_identifier,final_state_identifier,final_state_identifier,final_state_identifier,final_state_identifier,
        final_state_identifier,final_state_identifier,final_state_identifier,final_state_identifier,state_err1],
        
        
        [final_state_numerical,final_state_numerical,final_state_numerical,state_err2,state2,final_state_numerical,final_state_numerical,
        final_state_numerical,final_state_numerical,final_state_numerical,final_state_numerical,final_state_numerical,final_state_numerical,
        final_state_numerical,final_state_numerical,final_state_numerical,final_state_numerical,final_state_numerical,final_state_numerical,
        final_state_numerical,final_state_numerical,final_state_numerical,final_state_numerical,state_err1],
        
        
        [final_state_lesser,final_state_lesser,final_state_lesser,final_state_lesser,final_state_lesser,final_state_lesser,final_state_lesser,
        final_state_lesser,final_state_lesser,final_state_lesser,final_state_unequal,final_state_lesser_or_equal,final_state_lesser,
        final_state_lesser,final_state_lesser,final_state_lesser,final_state_lesser,final_state_lesser,final_state_lesser,final_state_lesser,
        final_state_lesser,final_state_lesser,final_state_lesser,state_err1],
        
        
        [final_state_greater,final_state_greater,final_state_greater,final_state_greater,final_state_greater,final_state_greater,final_state_greater,
        final_state_greater,final_state_greater,final_state_greater,final_state_greater,final_state_greater_or_equal,final_state_greater,
        final_state_greater,final_state_greater,final_state_greater,final_state_greater,final_state_greater,final_state_greater,final_state_greater,
        final_state_greater,final_state_greater,final_state_greater,state_err1],
        
        
        [state_err1,state_err1,state_err1,state_err1,state_err1,state_err1,state_err1,
        state_err1,state_err1,state_err1,state_err1,final_state_assignment,state_err1,state_err1,
        state_err1,state_err1,state_err1,state_err1,state_err1,state_err1,state_err1,
        state_err1,state_err1,state_err1],
        
        
        [state0,state6,state_err5,state6,state6,state6,state6,state6,state6,state6,state6,state6,state6,state6,state6,state6,state6,state6,state6,
        state6,state6,state6,state6,state6]]
        


#lex start function        
def lex():

    what_is_token = ''
    Tid = ''
    global line
    cnt = line
    lexeme = []
    current_state = state0
    
    while(current_state >= 0 and current_state <= 6):
            
            cur_sym = file.read(1)
            
            if (cur_sym == '#'):
                sym_val = hashtag
            elif (cur_sym == " " or cur_sym == "\t"):
                sym_val = blank_char
            elif (cur_sym == ""):
                sym_val = EOF
            elif (cur_sym in letters):
                sym_val = let
            elif (cur_sym in digits):
                sym_val = nums
            elif (cur_sym == "+"):
                sym_val = addition
            elif (cur_sym == "*"):
                sym_val = multiplication
            elif (cur_sym == "-"):
                sym_val = subtract
            elif (cur_sym == "/"):
                sym_val = division
            elif (cur_sym == "<"):
                sym_val = lesser
            elif (cur_sym == ">"):
                sym_val = greater
            elif (cur_sym == "="):
                sym_val = equality
            elif (cur_sym == ":"):
                sym_val = colon
            elif (cur_sym == ";"):
                sym_val = question_mark
            elif (cur_sym == ","):
                sym_val = comma
            elif (cur_sym == ")"):
                sym_val = RP
            elif (cur_sym == "("):
                sym_val = LP
            elif (cur_sym == "]"):
                sym_val = R_bracket
            elif (cur_sym == "["):
                sym_val = L_bracket
            elif (cur_sym == "}"):
                sym_val = R_bracket2
            elif (cur_sym == "{"):
                sym_val = L_bracket2
            elif (cur_sym == "."):
                sym_val = full_stop
            elif (cur_sym == "\n"):
                cnt = cnt + 1
                sym_val = newline
            else:
                sym_val = illegal_sym
                
                
            current_state = state_array[current_state][sym_val]

            
            if(current_state == state_err1):
                
                print("Illegal character at line:" + str(cnt))
                print("--------------------------")
            
            if(current_state == state_err2):
                
                print("Letter after digit exception found at line:" + str(cnt))
                print("--------------------------")
                
            if(current_state == state_err5):
                
                print("Comment section is not closed at line:" + str(cnt))
                print("--------------------------")
            
            if(len(what_is_token) < 30):
            
                if (current_state != 0 and current_state != 6):
                
                    what_is_token += str(cur_sym)
            else:
            
                current_state = state_err3
                print("Identifier is longer than 30 characters at line:" + str(cnt))
                print("--------------------------")
                break
            
            if(current_state == final_state_numerical or current_state == final_state_identifier or current_state == final_state_greater or current_state == final_state_lesser ):
                
                if (cur_sym == '\n'):
                                
                        cnt -= 1
                cur_sym = file.seek(file.tell()-1,0)  

                what_is_token = what_is_token[:-1]       
            
           
            
    if(current_state == final_state_identifier):
        if what_is_token in commited_words:
        
            Tid = "Commited word" 
            
        else:
        
            Tid = "Identifier" 
            
    if(current_state == 101):
        
        Tid = "Constant"
        
    if(current_state >= 102 and current_state <= 105):
        
        Tid = "Arithmetic symbol"
        
    if(current_state >= 107  and current_state <= 111):
        
        Tid = "Comparison symbol"
        
    if(current_state >= 115 and current_state <= 122):

        Tid = "Grouping symbol"
        
    if(current_state == 113 or current_state == 114):

        Tid = "Delimeter symbol"
        
    if(current_state == 112):

        Tid = "Assignment symbol"
    
    if (current_state == 123):
    
        Tid = "Termination symbol"

    if (current_state == -100):
    
        Tid = "Illegal symbol"
    
    if(current_state == final_state_numerical):
    
        if (abs(int(what_is_token)) > 4294967295):   # 2^32 - 1 
        
            current_state = state_err4
            
            print("Numeric constant out of bounds at line:" + str(cnt))
            print("--------------------------")
            
    
    lexeme.append(cnt)
    
    lexeme.append(what_is_token)
    
    lexeme.append(Tid)
    
    line = cnt
    
    return lexeme

'''
while(1):
    result = lex()
    if (result[1] == ''):
    
        break
        
    print(result)
    print("\n")
'''


#syntax starting function   
def syn():
    global line
    global result
    global subprogSign
    
    result = lex()
    line = result[0]


    def program():
        global result
        global line 
        global prog_name
        global f4
        
        if(result[1] == "program"):
            result = lex()
            line = result[0]
            
            if(result[2] == "Identifier"):
                prog_name = result[1]
                result = lex()
                line = result[0]
                
                f4.write("L0:" + "\n")
                f4.write("j Lmain" + "\n")
                
                block(prog_name)
                
                if(result[1] == "."): 
                
                    result = lex()
                    line = result[0]
                    
                    genquad("halt",'_','_','_')
                    
                    genquad("end_block",prog_name,'_','_')
                    
                    closescope(prog_name)
                    
                    return
                    
                    
                else:
                
                    print("Syntax Error: missing full stop:" + str(line))
                    exit(-1)   
                    
            else:
            
                print("Syntax Error: program name is non existant at line" + str(line))
                exit(-1)
        
        
        else:
        
            print("Program name is non existant at the start at line" + str(line))
            exit(-1)
            
        
    def block(id):
        global prog_name,f5
        global argsList
        global countListA
        global flag
        
        scope(id)
        
        list = argumentsToScope()
        
        declarations()
    
        subprograms()
        
        n = nextquad()
        
        genquad('begin_block',id,'_','_')
        
        editScope(id,n)  
        
        statements()
        
        calc_framelength()
        
        
        
        for i in scopesList:
            list = i[2]
            f5.write(str(i[0]) + "\n" + " | NAME: " + str(i[1]) + "\n")
            print(str(i[0]) + "\n" + " | NAME: " + str(i[1]))
            f5.write(" | ENTITY LIST: \n")
            print(" | ENTITY LIST: ")
            for j in list:
                f5.write("\t|" + str(j) + "\n")
                print("\t|" + str(j))
            f5.write(" | NESTING LEVEL: " + str(i[3]) + "\n")
            print(" | NESTING LEVEL: " + str(i[3]))
            list = i[4]
            if (list !=[]):
                f5.write(" | ENCLOSING SCOPE: " + str(list[1]) + "\n")
                print(" | ENCLOSING SCOPE: " + str(list[1]))
            if (list == []):
                f5.write(" | ENCLOSING SCOPE: " + str(list) + "\n")
                print(" | ENCLOSING SCOPE: " + str(list))
            print("\n")
            f5.write("\n")
        f5.write("top scope:" + str(top_sc[1]) + "\n")    
        print("top scope:" + str(top_sc[1]) + "\n")     
        f5.write("--------------------------------------------------------------------------------------------------------------")
        print("--------------------------------------------------------------------------------------------------------------")
        f5.write("\n")
        print("\n")
        
        
        
        if (id != prog_name):
            genquad('end_block',id,'_','_')
        if (flag == 0):
            countListA = countList
        else:
            addTolist()
        assemble()
        flag = 1
        closescope(id)
    
    def declarations():
        global result
            
        while(result[1] == "declare"):
            result = lex()
            line = result[0]
            varlist()
                
                
            if(result[1] == ";"):
                
                result = lex()
                line = result[0]
                
            else:
                
                print("Syntax error: ; was not found at the end  of the line at line:" + str(line))
                exit(-1)
                
        return
            
            
    def varlist():
        global result
        global variable_list    
             

        
        if(result[2] == "Identifier"):
            var_name = result[1]    
            variable_list += [var_name]
            result = lex()
            line = result[0]
            
            variable_ent(var_name,calc_offset())
            #check_entities(var_name)
            
            while(result[1] == ","):
                    
                result = lex()
                line = result[0]
               
                    
                if(result[2] == "Identifier"):
                    var_name = result[1]
                    variable_list += [var_name]
                    
                    result = lex()
                    line = result[0]
                    
                    variable_ent(var_name,calc_offset())
                    check_entities(var_name)

                    
                else:
                        
                    print("Syntax error: missing comma at line:" + str(line))
                    exit(-1)
        return
            
        
    def subprograms():
        global result
        global subprogSign    
            
        while(result[1] == "function" or result[1] == "procedure"):
            subprogSign = True
            subprogram()
                
        return
                
                
    def subprogram():
        global result
        global func_name
        global ret_flag

        
        ls = []

        if(result[1] == "function"):
            result = lex()
            line = result[0]

            
            if(result[2] == "Identifier"):
                func_name = result[1]
                result = lex()
                line = result[0]
                    
                    
                if(result[1] == "("):
                    result = lex()
                    line = result[0]
                        
                        
                    ls = formalparlist()
                    
                   
                    if(result[1] == ")"):
                        result = lex()
                        line = result[0]
                        
                       
                        function_ent(func_name,"function","-",ls,"-")

                        this_name = func_name
                        
                        check_entities(func_name)
                        
                        block(func_name)
                        
                        if(ret_flag == 0):
                        
                            print("Function needs at least one return statement\nFunction is:" + str(this_name))
                            exit()
                            
                        ret_flag = 0
                        
                        return
                            
                    else:
                           
                        print("Syntax error: ) is missing at line:" + str(line))
                        exit(-1)
                    
                else:
                    
                    print("Syntax error: ( is missing at line:" + str(line))
                    exit(-1)
            else:
                
                print("Syntax error: Identifier is missing at line:" + str(line))
                exit(-1)
            
            
        elif(result[1] == "procedure"):
            result = lex()
            line = result[0]
            func_name = result[1]
            
                
            if(result[2] == "Identifier"):
                func_name = result[1]
                result = lex()
                line = result[0]
                    
                    
                if(result[1] == "("):
                    result = lex()
                    line = result[0]
                        
                    ls = formalparlist()
      
                    
                    if(result[1] == ")"):
                        result = lex()
                        line = result[0]
                       
                        function_ent(func_name,"procedure","-",ls,"-")
                        
                        check_entities(func_name)
                        
                        block(func_name)
                        
                        if(ret_flag == 1):
                            print("Return statement at procedures is not permitted")
                            
                        ret_flag = 0
                        
                    else:

                        print("Syntax error: Brackets are not closed at line:" + str(line))
                        exit(-1)
                    
                else:
                        
                    print("Syntax error: Brackets are missing at line:" + str(line))
                    exit(-1)
                        
            else:

                print("Syntax error: Identifier expected at line:" + str (line))
                exit(-1)
                    
    def formalparlist():
            global result          
            
            ls = []
            
            ls.append(formalparitem())
            
            while(result[1] == ","):
                result = lex()
                line = result[0]
                
                ls.append(formalparitem())
                
            return ls


    def formalparitem():
            global line
            global result
            
            arg = []
            
            if(result[1] == "inout"):
                result = lex()
                line = result[0]


                
                if(result[2] == "Identifier"):
                    name = result[1]
                    result = lex()
                    line = result[0]
                    
                    arg = argument(name,"inout")

                    
                else:
                    
                    print("Syntax error: identifier expected after inout at line:" + str(line))
                    exit(-1)
                
            elif(result[1] == "in"):
                
                result = lex()
                line = result[0]


                
                if(result[2] == "Identifier"):
                    name = result[1]
                    result = lex()
                    line = result[0]
                    
                    arg = argument(name,"in")

                    
                else:
                    
                    print("Syntax error: identifier expected after in at line:" + str(line))
                    exit(-1)
                    
            return arg
           
        
    def statements():
        global line
        global result
        
        
        if(result[1] == "{"):
            result = lex()
            line = result[0]
                
            statement()
     
            while(result[1] == ";"):
                result = lex()
                line = result[0]
                    
                statement()    
                
            if(result[1] == "}"):
                result = lex()
                line = result[0]
                        
                return
                        
            else:
                    
                print("Syntax error: Block is not closed at line:" + str(line))
                exit(-1)
            
        else:
                
            statement()
            
            
            if(result[1] == ";"):
                result = lex()
                line = result[0]
                    
                return
                    
            else:
                print("Syntax error: missing ; at line:" + str(line))
                exit(-1)
                    
                    
    def statement():
        global result
            
            
        if(result[2] == "Identifier"):
            assignStat()
        elif(result[1] == "input"):
            inputStat()
        elif(result[1] == "return"):
            returnStat()
        elif(result[1] == "if"):
            ifStat()
        elif(result[1] == "while"):
            whileStat()
        elif(result[1] == "incase"):
            incaseStat()
        elif(result[1] == "switchcase"):
            switchcaseStat()
        elif(result[1] == "forcase"):
            forcaseStat()
        elif(result[1] == "call"):
            callStat()
        elif(result[1] == "print"):
            printStat()
            
        return
            
            
    def assignStat():
            global result


            if(result[2] == "Identifier"):
                loc_id = result[1] 
                
                result = lex()
                line = result[0]
                
                
                if(result[1] == ":="):
                    result = lex()
                    line = result[0]
                    
                    
                    exp_pl = expression()
                    
                    genquad(":=",exp_pl,"_",loc_id)
                    
                    return
                    
                else:

                    print("Syntax error: assignment symbol missing at line:" + str(line))
                    exit(-1)
                    
            else:
                    
                print("Syntax error: Identifier non existant at line:" + str(line))
                exit(-1)
                    
            
    def inputStat():
            global line
            global result
            global f4
           
           
            if(result[1] == "input"):
                result = lex()
                line = result[0]

                
                if(result[1] == "("):
                    result = lex()
                    line = result[0]
                    local_id = result[1]
                    genquad("inp", local_id,'_','_')
                    
                    if(result[2] == "Identifier"):
                        result = lex()
                        line = result[0]

                        
                        if(result[1] == ")"):
                            result = lex()
                            line = result[0]
                            
                            return
                            
                        else:
                            
                            print("Syntax error: brackets not closed at line:" + str(line))
                            exit(-1)
                         
                    else:
                    
                        print("Syntax error: Identifier is missing at line:" + str(line))
                        exit(-1)
                        
                else:
                    
                    print("Syntax error: brackets are missing at line:" + str(line))
                    exit(-1)
                    
            else:
                
                print("Syntax error: commited word input is missing at line:" + str(line))
                exit(-1)
                
        
    def returnStat():
            global line
            global result
            global func_name
            global ret_flag

            
            if(result[1] == "return"):
                result = lex()
                line = result[0]
                
                
                if(result[1] == "("):
                    result = lex()
                    line = result[0]
                    
                    
                    if(result[1] == func_name):
                        
                        genquad("call",func_name,'_','_')
                        
                    exp_pl = expression()
                    
                    genquad("retv",exp_pl,'_','_')
                    
                    ret_flag = 1
                    
                    if (result[1] == ")"):
                        result = lex()
                        line = result[0]
                        
                        return 
                    
                    else:
                    
                        print("Syntax error: Brackets not closed at line:" + str(line))
                        exit(-1)
                
                else:
                
                    print("Syntax error: brackets missing at line:" + str(line))
                    exit(-1)
                    
                    
        
    def ifStat():
            global line
            global result
            global b_false,b_true
            
            if(result[1] == "if"):
                result = lex()
                line = result[0]
                
                
                if(result[1] == "("):
                    result = lex()
                    line = result[0]
                    
                    
                    condition()
                    
                    loc_b_false = b_false
                    
                    
                    if(result[1] == ")"):
                        result = lex()
                        line = result[0]
                        
                        backpatch(b_true,nextquad())
                        
                        statements()
                        
                        ifList = makelist(nextquad())
                        
                        genquad("jump","_","_","_")
                        
                        backpatch(loc_b_false,nextquad())
                        
                        elseStat()
                        
                        backpatch(ifList,nextquad())
                        
                        return
                        
                    else:
                         
                        print("Syntax error: Brackets not closed at line:" + str(line))
                        exit(-1)
                        
                else:
                    
                    print("Syntax error: brackets are missing at line:" + str(line))
                    exit(-1)
             
            else:
            
                print("Syntax error: error with commited word id at line:" + str(line))
                exit(-1)
           
           
    def  elseStat():
            global line
            global result
            
            
            if(result[1] == "else"):
                result = lex()
                line = result[0]
                
                statements()
                
            return


    def whileStat():
            global line
            global result
            global b_false, b_true
            
            if(result[1] == "while"):
                result = lex()
                line = result[0]
                
                
                if(result[1] == "("):
                    result = lex()
                    line = result[0]
                    
                    bquad = nextquad()
                    
                    condition()
                    
                    loc_b_false = b_false
                    
                    if(result[1] == ")"):
                        backpatch(b_true,nextquad())
                    
                        result = lex()
                        line = result[0]
                    
                        
                        statements()
                        
                        genquad("jump","_","_",bquad)
                        
                        backpatch(loc_b_false,nextquad())
                        
                        return
                        
                    else:
                    
                        print("Syntax error: Brackets are not closed at line:" + str(line))
                        exit(-1)
                
                else:

                    print("Syntax error: Brackets are missing at line:" + str(line))
                    exit(-1)
                    
            else:

                print("Syntax error: while is missing at line:" + str(line)) 
                exit(-1)
            
            
    def incaseStat():
            global line
            global result
            global b_false,b_true
            
            if(result[1] == "incase"):
                result = lex()
                line = result[0]
                
                
                w = newtemp()
                
                p1Quad = nextquad()                
                
                genquad(":=",1,"_",w) 
                

                while(result[1] == "case"):
                    result = lex()
                    line = result[0]
                    
                    
                    if(result[1] == "("):
                        result = lex()
                        line = result[0] 
                        
                        
                        condition()
                        
                        backpatch(b_true,nextquad())
                        
                        if(result[1] == ")"):
                            result = lex()
                            line = result[0]
                            
                            statements()
                            
                            genquad(":=",0,"_",w)
                          
                            backpatch(b_false,nextquad())    
                           
                        else:
                            
                            print("Syntax error: Brackets are not closed at line:" + str(line))
                            exit(-1)
                            
                    else:

                        print("Syntax error: Brackets are missing at line:" + str(line))
                        exit(-1)
                
                genquad("=",w,0,p1Quad)
                
            else:
                
                print("Syntax error: error within incase at line:" + str(line))
                exit(-1)
                
          
    def switchcaseStat():
            global line
            global result
            global b_false,b_true
            
            if(result[1] == "switchcase"):
                result = lex()
                line = result[0]
                
                exitlist = emptylist()
                
                while(result[1] == "case"):
                    result = lex()
                    line = result[0]

                    
                    if(result[1] == "("):
                        result = lex()
                        line = result[0]
                        
                        
                        condition()
                        
                        backpatch(b_true,nextquad())
                        
                        
                        
                        if(result[1] == ")"):
                            result = lex()
                            line = result[0]
                            
                            
                            statements()
                            
                            e = makelist(nextquad())
                            
                            genquad("jump","_","_","_")
                            
                            exitlist = merge(exitlist,e)
                            
                            backpatch(b_false,nextquad())
                            
                        else:
                            
                            print("Syntax error: Brackets are not closed at line:" + str(line))
                            exit(-1)
                            
                    
                    else:
                        
                        print("Syntax error: Brackets are missing at line:" + str(line))
                        exit(-1)
                   
                   
                if(result[1] == "default"):
                    result = lex()
                    line = result[0]
                            
                    
                    statements()
                    
                    backpatch(exitlist,nextquad())
                        
                else:
                    
                    print("Syntax error: error within commited word default at line:" + str(line))
                    exit(-1)
                    
            else:
                
                print("syntax error: error within switchcase at line:" + str(line))
                exit(-1)
                
                
    def forcaseStat():
            global line
            global result
            global b_false,b_true
            
            if(result[1] == "forcase"):
                result = lex()
                line = result[0]
            
                p1Quad = nextquad()
                
                while(result[1] == "case"):
                    result = lex()
                    line = result[0]
                    
                    
                    if(result[1] == "("):
                        result = lex()
                        line = result[0]
                        
                        
                        condition()
                        
                        backpatch(b_true,nextquad())
                        
                        if(result[1] == ")"):
                            result = lex()
                            line = result[0]
                            
                            
                            statements()
                            
                            genquad("jump","_","_",p1Quad)
                            
                            backpatch(b_false,nextquad())
                            
                        else:
                            
                            print("Syntax error: Brackets are not closed at line:" + str(line))
                            exit(-1)
                            
                    else:
                    
                        print("Syntax error: Brackets are missing at line:" + str(line))
                        exit(-1)
                        
                        
                if(result[1] == "default"):
                    result = lex()
                    line = result[0]
                    
                    
                    statements()
                    
                    
                else:
                    
                    print("Syntax error: error within default at line:" + str(line))
                    exit(-1)
                    
            else:
                
                print("Syntax error: error within forcase at line:" + str(line))
                exit(-1)
                
                
    def callStat():
            global line
            global result
            
            
            if(result[1] == "call"):
                result = lex()
                line = result[0]
                local_proc_name = result[1]

                if(result[2] == "Identifier"):
                    result = lex()
                    line = result[0]

                    
                    if(result[1] == "("):
                        result = lex()
                        line = result[0]
                        
                        
                        list = actualparlist()
                        gl_actual_list.append([local_proc_name,list])
                        print(gl_actual_list)
                        genquad("call",local_proc_name,'_','_')
                        
                        
                        if(result[1] == ")"):
                            result = lex()
                            line = result[0]
                            
                            return
                            
                            
                        else:

                            print("Syntax error: Brackets are not closed at line:" + str(line))
                            exit(-1)
                            
                    else:
                        
                        print("Syntax error: Brackets are missing at line:" + str(line))
                        exit(-1)
                           
                else:
                    
                    print("Syntax error: Identifier missing at line:" + str(line))
                    exit(-1)
                    
            else:

                print("Syntax error: error within call at line:" + str(line))
                exit(-1)
                
            return
            
            
    def printStat():
            global line
            global result
            
            
            if(result[1] == "print"):
                result = lex()
                line = result[0]
                
                
                if(result[1] == "("):
                    result = lex()
                    line = result[0]
                    
                    
                    exp_pl = expression()
                    
                    genquad("out",exp_pl,'_','_')
                    
                    if(result[1] == ")"):
                        result = lex()
                        line = result[0]
                        
                    else:

                        print("Syntax error: Brackets are not closed in line:" + str(line))
                        exit(-1)
                        
                else:

                    print("Syntax error: Brackets are missing in line:" + str(line))
                    exit(-1)
                    
            else:
            
                print("Syntax error: error within print in line:" + str(line))
                exit(-1)
                
            return    
            
            
    def actualparlist():
            global line
            global result
            
            actual_list = []
            
            actual_list.append(actualparitem())
            
            while(result[1] == ","):
                result = lex()
                line = result[0]
                
                actual_list.append(actualparitem())
                
                
            return actual_list


    def actualparitem():
            global line
            global result
            
            act_arg = []
            
            if(result[1] == "inout"):
                result = lex()
                line = result[0]
                tmp = result[1]
                m = "REF"
                
                if(result[2] == "Identifier"):
                    result = lex()
                    line = result[0]
                    
                    genquad("par",tmp,m,"_")
                    act_arg = [tmp,m]
                   
                else:

                    print("Syntax error: Identifier expected at line:" + str(line))
                    exit(-1)
                    
            elif(result[1] == "in"):
                tmp = result[1]
                result = lex()
                line = result[0]
                m = "CV"
                
                exp_pl = expression()
                
                genquad("par",exp_pl,m,"_")
                act_arg = [exp_pl,m]
                
            return act_arg
        

    def condition():
            global line
            global result
            global con_f,con_t,q_false,q_true,b_false,b_true
            
            boolterm()
            
            b_true = q_true
            
            b_false = q_false
            
            while(result[1] == "or"):
                backpatch(b_false,nextquad())
                
                result = lex()
                line = result[0]

                
                boolterm()
                
                b_true = merge(b_true,q_true)
                
                b_false = q_false
                
            con_f = b_false
            con_t = b_true
            
            return
         

    def boolterm():
            global line
            global result
            global r_false,r_true,q_false,q_true
            
            boolfactor()
            
            q_true = r_true
            
            q_false = r_false
            
            while(result[1] == "and"):
                backpatch(q_true,nextquad())
            
                result = lex()
                line = result[0]
                
                
                boolfactor()
                
                q_false = merge(q_false,r_false)
                
                q_true = r_true
                
            return    
            
            
    def boolfactor():
            global line
            global result
            global r_false,r_true,b_false,b_true
            
            
            if(result[1] == "not"):
                result = lex()
                line = result[0]
                
                
                if(result[1] =="["):
                    result = lex()
                    line = result[0]
                    
                    
                    condition()
                    
                    
                    if(result[1] == "]"):
                        result = lex()
                        line = result[0]
                        
                        r_true = b_false
                        
                        r_false = b_true
                        
                    else:

                        print("Syntax error: Brackets [] are not closed at line:" + str(line))
                        exit(-1)
                        
                else:

                    print("Syntax error: Brackets [] are missing at line:" + str(line))
                    exit(-1)
                 
                    
            elif(result[1] == "["):
                result = lex()
                line = result[0]
                
                
                condition()
                
                
                if(result[1] == "]"):
                    result = lex()
                    line = result[0]
                    
                    r_true = b_true
                    
                    r_false = b_false
                    
                else:

                    print("Syntax error: Brackets [] are not closed at line:" + str(line))
                    exit(-1)
                    
            
            else:

                e1_pl = expression()

                rop = relational_oper()

                e2_pl = expression()
                
                r_true = makelist(nextquad())
                
                genquad(rop,e1_pl,e2_pl,'_')
                
                r_false = makelist(nextquad())
                
                genquad("jump",'_','_','_')
                
            return    
            
            
    def expression():
            global line
            global result
            
            
            ops = optional_sign()
            
            
            t1_pl = term()
            
            if (ops == "-"):
                t1_pl = "-" + t1_pl
            
            while(result[1] == "+" or result[1] == "-"):
                

                op = add_oper()
                
                t2_pl = term()
                
                Tmp = newtemp()
                
                genquad(op,t1_pl,t2_pl,Tmp)
                
                t1_pl = Tmp
                
            exp_pl = t1_pl
            
            return exp_pl


    def optional_sign():
            global line
            global result
            ops = ""
            
            if(result[1] == "+" or result[1] == "-"):
                
                ops = add_oper()
                
            return ops


    def term():
            global line
            global result
            
            
            f1_pl = factor()
            
            
            while(result[1] == "*" or result[1] == "/"):
                
                op = mul_oper()
                
                f2_pl = factor()
                
                Tmp = newtemp()

                genquad(op,f1_pl,f2_pl,Tmp)

                f1_pl = Tmp
                
            
            term_pl =  f1_pl
            
            return term_pl   
            
            
    def factor():
            global line
            global result
            
            
            if(result[2] == "Constant"):
                f = result[1]
                result = lex()
                line = result[0]
                
                
            elif(result[1] == "("):
                result = lex()
                line = result[0]
                
                
                exp_pl = expression() 
                
                f = exp_pl
                
                if(result[1] == ")"):
                    result = lex()
                    line = result[0]
                    
                    
                else:

                    print("Syntax error: ')' is missing at line:" + str(line))
                    exit(-1)
                    
            elif(result[2] == "Identifier"):
                fid = result[1]
                result = lex()
                line = result[0]
               
                
                f = idtail(fid)
                
                
            else:

                print("Syntax error: Identifier or constant expected at line:" + str(line))
                exit(-1)
                
            return f

         
    def idtail(arg):
            global line
            global result
            
            
            if(result[1] == "("):
                result = lex()
                line = result[0]
                
                
                list = actualparlist()

                temp = newtemp()
                
                genquad("par",temp,"RET","_")
                
                genquad("call",arg,"_","_")
                
                if(result[1] == ")"):
                    result = lex()
                    line = result[0]
                    
                    return temp
                    
            
            return arg           


    def relational_oper():
            global line
            global result
            
            
            if(result[1] == ">"):
            
                rop = result[1]
                result = lex()
                line = result[0]
                
            elif(result[1] == "<"):
            
                rop = result[1]
                result = lex()
                line = result[0]
                
            elif(result[1] == ">="):
            
                rop = result[1]
                result = lex()
                line = result[0]
                
            elif(result[1] == "<="):
            
                rop = result[1]
                result = lex()
                line = result[0]
                
            elif(result[1] == "<>"):
            
                rop = result[1]
                result = lex()
                line = result[0]
                
            elif(result[1] == "="):
            
                rop = result[1]
                result = lex()
                line = result[0]
                
            else:
                
                print("Syntax error: relational operation missing at line:" + str(line))
                exit(-1)

            return rop

        
    def add_oper():
            global line
            global result
            
            
            if(result[1] == "+"):
                
                op = result[1]
                result = lex()
                line = result[0]
                
            elif(result[1] == "-"):
                
                op = result[1]
                result = lex()
                line = result[0]
                
                
            return op


    def mul_oper():
            global line
            global result

            
            if(result[1] == "*"):
                
                op = result[1]
                result = lex()
                line = result[0]
                
            elif(result[1] == "/"):
                
                op = result[1]
                result = lex()
                line = result[0]
                
                
            return op   
            
    program()     
    return    


def nextquad():
    global countList
    return len(countList)
    
    
def genquad(op,x,y,z):
    global countList,label
    label = nextquad()
    countList.append([label,op,x,y,z])


def newtemp():
    global temp_var_list
    newT = "T_" + str(len(temp_var_list) + 1)
    temp_var_list.append(newT)
    temp_var_ent(newT,calc_offset())
    
    return newT
    
def emptylist():

    labelList = []
    
    return labelList
    
    
def makelist(x):
    
    return [x]


def merge(list1, list2):

    mergedList = list1 + list2 
    return mergedList
    

def backpatch(list,z):
    global countList
    for i in range(len(list)):
        for j in range(len(countList)):
            if (list[i] == countList[j][0] and countList[j][4] == '_'):
                countList[j][4] = z
                break;
                
    return

def addTolist():
    global countList,countListA
    global assembleNum
    
    for i in countList:
        if(i[0] >= assembleNum):
            countListA.append(i)

#scopes     // [scope:,name,entity_list,nestingLevel,enclosingScope]
def scope(name):
    global scopesList
    global top_sc

    entityList = []
    
    if (top_sc == []):
        nestingLevel = 0
    else:
        nestingLevel = top_sc[3] + 1
    
    enclosingScope = top_sc
    if (enclosingScope != []):
        en_name = enclosingScope[1]
    else: 
        en_name = []
    sc = ["Scope",name,entityList,nestingLevel,enclosingScope]
    scopesList.append(sc)
    
    top_sc = sc


def addToScope(arg):
    global scopesList
    global top_sc
    
    for i in scopesList:
        if (top_sc[1] == i[1]):
            i[2].append(arg)
            
            
def argumentsToScope():
    global top_sc
   
    enscope = top_sc[4]
    if(enscope != []):
        for i in enscope[2]:
            if(i != [] and i[0] == "SUBPROGRAM" and i[1] == top_sc[1]):
                arlist = i[4]
                for j in arlist:
                    if(j != []):
                        argument_ent(j[0],j[1],calc_offset())

                    

    
   
def editScope(name,id):
    global scopesList
    global countList
    
    for i in scopesList:
        list = i[2]
        for j in list:
            list2 = j
            editEntity(name,list2,id)
    return list2

    
def editEntity(name,list,id):
    global countList
    for i in countList:
        list2 = i
        if (list[0] == "SUBPROGRAM" and list[1] == name and list2[2] == name and list2[0] == id):
            list[3] = id
   
   
def calc_framelength():
    global top_sc
    
    enclosing = top_sc[4]
    if (enclosing != []):
        entities = enclosing[2]
        if (entities != []):
            for i in entities:
                if(i[0] == "SUBPROGRAM" and i[1] == top_sc[1]):
                    i[5] = calc_offset()
            
    
    return
    
def closescope(name):
    global top_sc
    global scopesList
    
    tmp = top_sc
    for i in scopesList:
        if(i[1] == name):
            top_sc = i[4]
            scopesList.remove(i)


#entities
def variable_ent(name,offset):
    global scopesList
    global top_sc
    
    ve = ["VARIABLE",name,offset]
    
    addToScope(ve)

def function_ent(name,type,startQuad,argument_list,framelength):
    global scopesList
    
    fe = ["SUBPROGRAM",name,type,startQuad,argument_list,framelength]
    
    addToScope(fe)


def argument_ent(name,parMode,offset):
    global scopesList
    
    ae = ["ARGUMENT",name,parMode,offset]
    
    addToScope(ae)
    
    
    
def temp_var_ent(name,offset):
    global scopesList
    
    te = ["TEMP_VARIABLES",name,offset]
    
    addToScope(te)


def calc_offset():
    global top_sc
    
    count = 0
    list = top_sc[2]

    if (list is not []):
        for i in list:
            ent_list = i
            if (ent_list[0] == "VARIABLE" or ent_list[0] == "ARGUMENT" or ent_list[0] == "TEMP_VARIABLES"):
                count += 1
    offset = 12 + (count*4)
    
    return offset
    

#arguments
def argument(name,parMode):
    
    arg = [name,parMode]
    
    return arg


def find_ent(name):
    global top_sc
    
    temp = top_sc
    while temp != []:
        for ent in temp[2]:
            if(ent[1] == name):
                return (temp[1],temp[3],ent)
        temp = temp[4]
        
    print("Entity was not found. Name given: " + str(name))
    exit()

def check_entities(id):
    global top_sc,entity_list_toCheck
    
    list = find_ent(id)
    ent_list = list[2]
    if(ent_list[0] == "VARIABLE"):
        entity_list_toCheck.append([list[0],list[1],ent_list[1]])
    elif(ent_list[0] =="SUBPROGRAM"):
        entity_list_toCheck.append([list[0],list[1]+1,ent_list[1]])
    #print(entity_list_toCheck)
    for i in entity_list_toCheck:
        for j in entity_list_toCheck:
            if(i[1] == j[1] and i[2] == j[2] and i!=j):
                print("Duplicate entity with name:" + str(i[2]) + "\n")
                exit()
    
    
    

def check_arguments(id,arg):
    

    return
    

#Assembly

f4 = open(f.split(".")[0] + ".asm","w")

def gnvlcode(ent_name):
    global f4,top_sc
    
    f4.write("lw $t0,-4($sp)\n")
    
    asm_ent = find_ent(ent_name)
    
    loop = top_sc[3] - asm_ent[1]
    loop = loop - 1

    for i in range(0,loop):
        f4.write("lw $t0,-4($t0)\n")
        
    ent_list = asm_ent[2]
    if(ent_list[0] == "ARGUMENT"):
        off = ent_list[3]
    if(ent_list[0] == "VARIABLE"):
        off = ent_list[2]
    
    f4.write("addi $t0,$t0,-" + str(off) + "\n")
    
def loadvr(v,r):
    global f4,top_sc
   
    
    if(v.isdigit()):
        f4.write("li $t" + str(r) + "," + str(v) + "\n") 
        
    else:
        asm_ent = find_ent(v)
        ent_list = asm_ent[2]
        
        if (asm_ent[1] == 0 and [ent_list[0] == "VARIABLE" or ent_list[0] == "TEMP_VARIABLES"]):
            off = ent_list[2]
            f4.write("lw $t" + str(r) + ",-" + str(off) + "($s0)\n")
            
            
        elif(asm_ent[1] == top_sc[3]):
        
            if(ent_list[0] == "VARIABLE" or ent_list[0] == "TEMP_VARIABLES"):
                off = ent_list[2]
                f4.write("lw $t" + str(r) + ",-" + str(off) + "($sp)\n")
                
                
            elif(ent_list[0] == "ARGUMENT" and ent_list[2] == "in"):
                    off = ent_list[3]
                    f4.write("lw $t" + str(r) + ",-" + str(off) + "($sp)\n")
                
                
            elif(ent_list[0] == "ARGUMENT" and ent_list[2] == "inout"):
                    off = ent_list[3]
                    f4.write("lw $t0,-" + str(off) + "($sp)\n")
                    f4.write("lw $t" + str(r) + ",($t0)\n")
                
                
        elif(asm_ent[1] < top_sc[3]):
                if(ent_list[0] == "VARIABLE"):
                    gnvlcode(v)
                    f4.write("lw $t" + str(r) + ",($t0)\n")
                
                
                elif(ent_list[0] == "ARGUMENT" and ent_list[2] == "in"):
                    gnvlcode(v)
                    f4.write("lw $t" + str(r) + ",($t0)\n")
                
                elif(ent_list[0] == "ARGUMENT" and ent_list[2] == "inout"):
                    gnvlcode(v)
                    f4.write("lw $t0,($t0)\n")
                    f4.write("lw $t" + str(r) + ",($t0)\n")

def storerv(r,v):
    global f4,top_sc
    
    asm_ent = find_ent(v)
    ent_list = asm_ent[2]
    
    if(asm_ent[1] == 0 and ent_list[0] == "VARIABLE"):
        off = ent_list[2]
        f4.write("sw $t" + str(r) + ",-" + str(off) + "($s0)\n")
    
    elif(asm_ent[1] == top_sc[3]):
        if(ent_list[0] == "VARIABLE" or ent_list[0] == "TEMP_VARIABLES"):
            off = ent_list[2]
            f4.write("sw $t" + str(r) + ",-" +str(off) + "($sp)\n")
         
        elif(ent_list[0] == "ARGUMENT" and ent_list[2] == "in"):
            off = ent_list[3]
            f4.write("sw $t" + str(r) + ",-" + str(off) + "($sp)\n")
            
        elif(ent_list[0] == "ARGUMENT" and ent_list[2] == "inout"):
            off = ent_list[3]
            f4.write("lw $t0,-" + str(off) + "($sp)\n")
            f4.write("sw $t" + str(r) + ",($t0)\n")
            
    elif(asm_ent[1] < top_sc[3]):
        if(ent_list[0] == "VARIABLE"):
            gnvlcode(v)
            f4.write("sw $t" + str(r) + ",($t0)\n")
            
        elif(ent_list[0] == "ARGUMENT" and ent_list[2] == "in"):
            gnvlcode(v)
            f4.write("sw $t" + str(r) + ",($t0)\n")
            
        elif(ent_list[0] == "ARGUMENT" and ent_list[2] == "inout"):
            gnvlcode(v)
            f4.write("lw $t0,($t0)\n")
            f4.write("sw $t" + str(r) + ",($t0)\n")
            

            
def assemble():
    global f4,top_sc,countListA,arg_count,assembleNum,prog_name
   
    
    for i in range(len(countListA)):
        
        if(countListA[i][1] == "begin_block" and countListA[i][2] == prog_name):
            f4.write("Lmain:" + "\n")
            f4.write("L" + str((countListA[i][0]) + 1) + ": \n")
        else:    
            f4.write("L" + str((countListA[i][0] + 1)) + ": \n")
                
        if(countListA[i][1] == "jump"):
            f4.write("j L" + str(countListA[i][4] + 1) + "\n")
            
        elif(countListA[i][1] == ">"):
            loadvr(countListA[i][2],1)
            loadvr(countListA[i][3],2)
            f4.write("bgt,$t1,$t2,L" + str(countListA[i][4] + 1) + "\n")
            
        elif(countListA[i][1] == "<"):   
            loadvr(countListA[i][2],1)
            loadvr(countListA[i][3],2)
            f4.write("blt,$t1,$t2,L" + str(countListA[i][4] + 1) + "\n")
            
        elif(countListA[i][1] == ">="):
            loadvr(countListA[i][2],1)
            loadvr(countListA[i][3],2)
            f4.write("bge,$t1,$t2,L" + str(countListA[i][4] + 1) + "\n")
            
        elif(countListA[i][1] == "<="):
            loadvr(countListA[i][2],1)
            loadvr(countListA[i][3],2)
            f4.write("ble,$t1,$t2,L" + str(countListA[i][4] + 1) + "\n")    
            
        elif(countListA[i][1] == "<>"):
            loadvr(countListA[i][2],1)
            loadvr(countListA[i][3],2)
            f4.write("bne,$t1,$t2,L" + str(countListA[i][4] + 1) + "\n")
        
        elif(countListA[i][1] == "="):
            loadvr(countListA[i][2],1)
            loadvr(countListA[i][3],2)
            f4.write("beq,$t1,$t2,L" + str(countListA[i][4] + 1) + "\n")

        elif(countListA[i][1] == ":="):
            loadvr(countListA[i][2],1)
            storerv(1,countListA[i][4])
            
        elif(countListA[i][1] == "+" or countListA[i][1] == "-" or countListA[i][1] == "*" or countListA[i][1] == "/"):
            loadvr(countListA[i][2],1)
            loadvr(countListA[i][3],2)
            if(countListA[i][1] == "+"):
                f4.write("add,$t1,$t1,$t2" + "\n")
            elif(countListA[i][1] == "-"):
                f4.write("sub,$t1,$t1,$t2" + "\n")
            elif(countListA[i][1] == "*"):
                f4.write("mul,$t1,$t1,$t2" + "\n")
            elif(countListA[i][1] == "/"):    
                f4.write("div,$t1,$t1,$t2" + "\n")
            storerv(1,countListA[i][4])
        
        elif(countListA[i][1] == "out"):
            f4.write("li $v0,1" + "\n")
            loadvr(countListA[i][2],1)
            f4.write("move $a0,$t1" + "\n")
            f4.write("syscall" + "\n")
            
        elif(countListA[i][1] == "inp"):
            f4.write("li $v0,5" + "\n")
            f4.write("syscall" + "\n")
            f4.write("move $t1,$v0" + "\n")
            storerv(1,countListA[i][2])
            
        elif(countListA[i][1] == "retv"):
            loadvr(countListA[i][2],1)
            f4.write("lw $t0,-8($sp)" + "\n")
            f4.write("sw $t1,($t0)" + "\n")
        
        elif(countListA[i][1] == "par"):
            
            if(arg_count == -1):
               
                for j in range(len(countListA)):
                    if(countListA[j][1] == "call"):
                        subprogName = countListA[j][2]
                        
                searched_subp = find_ent(subprogName)        
                ent_list = searched_subp[2]
                fl = ent_list[5]
                f4.write("addi $fp,$sp," + str(fl) + "\n")
                arg_count = 0
            
                

            if(countListA[i][3] == "CV"):
                loadvr(countListA[i][2],0)
                f4.write("sw $t0,-" + str(12+4*arg_count) + "($fp)\n")
                arg_count = arg_count + 1
                
            elif(countListA[i][3] == "RET"):
                search_par = find_ent(countListA[i][2])
                ent_list = search_par[2]
                off = ent_list[2]
                f4.write("addi $t0,$sp,-" + str(off) + "\n")
                f4.write("sw $t0,-8($fp)\n")
                
            elif(countListA[i][3] == "REF"):
                search_par = find_ent(countListA[i][2])
                ent_list = search_par[2]
                
                if(search_par[1] == top_sc[3]):
                    if(ent_list[0] == "VARIABLE"):
                        off = ent_list[2]
                        f4.write("addi $t0,$sp,-" + str(off) + "\n")
                        f4.write("sw $t0,-" + str(12+4*arg_count) + "($fp)\n")
                    elif(ent_list[0] == "ARGUMENT" and ent_list[2] == "in"):
                        off = ent_list[3]
                        f4.write("addi $t0,$sp,-" + str(off) +  "\n")
                        f4.write("sw $t0,-" + str(12+4*arg_count) + "($fp)\n")
                    elif(ent_list[0] == "ARGUMENT" and ent_list[2] == "inout"):
                        off = ent_list[3]
                        f4.write("lw $t0,-" + str(off) + "($sp)\n")
                        f4.write("sw $t0, -" + str(12+4*arg_count) + "($fp)\n")
                elif(search_par[1] < top_sc[3]):
                    gnvlcode(countListA[i][2])
                    if(ent_list[0] == "ARGUMENT" and ent_list[2] == "inout"):
                        f4.write("lw $t0,($t0)" + "\n")
                        f4.write("sw $t0, -" + str(12+4*arg_count) + "($fp)\n")
                    else:
                        f4.write("sw $t0, -" + str(12+4*arg_count) + "($fp)\n")
                        
                arg_count = arg_count + 1    
                
        elif(countListA[i][1] == "call"):
            arg_count = -1
            searched_subp = find_ent(countListA[i][2])
            ent_list = searched_subp[2]
            if(top_sc[3] == searched_subp[1]+1):
                f4.write("lw $t0,-4($sp)" + "\n")
                f4.write("sw $t0,-4($fp)" + "\n")
            
            elif(top_sc[3] < searched_subp[1]+1):
                f4.write("sw $sp ,-4($fp)" + "\n")
            
            fl = ent_list[5]
            sq = ent_list[3]
            f4.write("addi $sp,$sp," + str(fl) + "\n")
            f4.write("jal L" + str(sq + 1) + "\n")
            f4.write("addi $sp,$sp,-" + str(fl) + "\n")
            
            
            
        elif(countListA[i][1] == "begin_block" and top_sc[3] !=0):
            f4.write("sw $ra,($sp)" + "\n")
        
        elif(countListA[i][1] == "begin_block" and top_sc[3] == 0):
            
            f4.write("addi $sp,$sp," + str(calc_offset()) + "\n")
            f4.write("move $s0,$sp\n")
            
        elif(countListA[i][1] == "end_block" and top_sc[3] !=0):
            f4.write("lw $ra,($sp)" + "\n")
            f4.write("jr $ra" + "\n")
    
    assembleNum = nextquad()

    countListA = []


f5 = open(f.split(".")[0] + ".txt","w")
 
syn()



for i in countList:
    print(i)
    
'''
f2 = open(f.split(".")[0] + ".int","w")

for j in countList:
    f2.write(str(j))
    f2.write("\n\n")

print("* File with quads is written\n")   

if(subprogSign == False):

    f3 = open(f.split(".")[0] + ".c","w")

    f3.write("int main()\n")

    f3.write("{\n\t")

    f3.write("int ")

    for i in range(len(variable_list)):
      
        f3.write(variable_list[i])

        if((len(variable_list)) == i + 1 and len(temp_var_list) == 0):

            f3.write(";\n\t")

        else:

            f3.write(",")


    for j in range(len(temp_var_list)):

        f3.write(temp_var_list[j])

        if(len(temp_var_list) == j + 1):

            f3.write(";\n\t")

        else:

            f3.write(",")

            
    for k in range(len(countList)):
        
        if(countList[k][1] == "begin_block"):
        
            f3.write("L_" + str(countList[k][0] + 1) + ":\n\t")
            
        elif(countList[k][1] == "+" or countList[k][1] == "-" or countList[k][1] == "*" or countList[k][1] == "/"):

            f3.write("L_" + str(countList[k][0] + 1) + ": " + countList[k][4] + " = " + countList[k][2] + " " + countList[k][1] + " " + countList[k][3] + "; // [ " + str(countList[k][0]) + ", " + countList[k][1] + ", " + countList[k][2] + ", " + countList[k][3] + ", " + countList[k][4] + " ]\n\t")
        
        elif(countList[k][1] == "jump"):
        
            f3.write("L_" + str(countList[k][0] + 1) + ": " + "goto L_" + str(countList[k][4] + 1) + "; // [ " + str(countList[k][0])+ ", " + "jump" + ", " + "_" + ", " + "_" + str(countList[k][4]) + " ]\n\t")
            
        elif(countList[k][1] == "<" or countList[k][1] == ">" or countList[k][1] == "<>" or countList[k][1] == "<=" or countList[k][1] == ">=" or countList[k][1] == "="):
            
            if(countList[k][1] == "<>"):
            
                f3.write("L_" + str(countList[k][0] + 1) + ": " + "if (" + countList[k][2] + " != " + countList[k][3] + ") goto L_" + str(countList[k][4] + 1) + "; // [ " + str(countList[k][0]) + ", " + countList[k][1] + ", " + countList[k][2] + ", " + countList[k][3] + ", " + str(countList[k][4]) + " ]\n\t")
            
            elif(countList[k][1] == "="): 
            
                f3.write("L_" + str(countList[k][0] + 1) + ": " + "if (" + str(countList[k][2]) + " == " + str(countList[k][3]) + ") goto L_" + str(countList[k][4] + 1) + "; // [ " + str(countList[k][0]) + ", " + str(countList[k][1]) + ", " + str(countList[k][2]) + ", " + str(countList[k][3]) + ", " + str(countList[k][4]) + " ]\n\t")
            
            else:
            
                f3.write("L_" + str(countList[k][0] + 1) + ": " + "if (" + countList[k][2] + " " + countList[k][1] + " " + countList[k][3] + ") goto L_" + str(countList[k][4] + 1) + "; // [ " + str(countList[k][0]) + ", " + countList[k][1] + ", " + countList[k][2] + ", " + countList[k][3] + ", " + str(countList[k][4]) + " ]\n\t")
        
        elif(countList[k][1] == ":="):
        
            f3.write("L_" + str(countList[k][0] + 1) + ": " + countList[k][4] + " = " + str(countList[k][2]) + "; // [ " + str(countList[k][0]) + ", " + countList[k][1] + ", " + str(countList[k][2]) + ", " + countList[k][3] + ", " + countList[k][4] + " ]\n\t")
        
        elif(countList[k][1] == "inp"):
        
            f3.write("L_" + str(countList[k][0] + 1) + ": scanf(" + '"' + "%d" + '"' + ", &" + countList[k][2] + "); // [ " + str(countList[k][0]) + ", " + countList[k][1] + ", " + countList[k][2] + ", " + countList[k][3] + ", " + countList[k][4] + " ]\n\t")
        
        elif(countList[k][1] == "out"):
        
            f3.write("L_" + str(countList[k][0] + 1) + ': printf(' + '"' + countList[k][2] + ' =%d' + '"' + "," + countList[k][2] + "); // [ " + str(countList[k][0]) + ", " + countList[k][1] + ", " + countList[k][2] + ", " + countList[k][3] + ", " + countList[k][4] + " ]\n\t")
        
        elif(countList[k][1] == "halt"):

            f3.write("L_" + str(countList[k][0] + 1) + ": " + "{}\n")
            
    f3.write("}") 
    
    print("* C code file written")


'''
print("\n")    
print("Lexical and syntax analysis completed")

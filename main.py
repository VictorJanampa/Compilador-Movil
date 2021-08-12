# initialization
from flask import jsonify, request
import ply.lex as lex
import ply.yacc as yacc
import sys
import json
import flask
#from app import app
from flask_cors import CORS, cross_origin
from flask import Flask
app = Flask(__name__)
#PROPAGATE_EXCEPTIONS = False
@app.route('/getcompilador', methods=['POST'])

def getCompilador():
        global data
        tokens = [

            'INT',
            'FLOAT',
            'NAME',
            'PLUS',
            'MINUS',
            'DIVIDE',
            'MULTIPLY',
            'EQUALS'

        ]

        t_PLUS = r'\+'
        t_MINUS = r'\-'
        t_MULTIPLY = r'\*'
        t_DIVIDE = r'\/'
        t_EQUALS = r'\='


        t_ignore = r' '

        def t_FLOAT(t):
            r'\d+\.\d+'
            t.value = float(t.value)
            return t

        def t_INT(t):
            r'\d+'
            t.value = int(t.value)
            return t

        def t_NAME(t):
            r'[a-zA-Z_][a-zA-Z_0-9]*'
            t.type = 'NAME'
            return t

        def t_error(t):
            print("Illegal characters!")
            t.lexer.skip(1)

        lexer = lex.lex()

        precedence = (

            ('left', 'PLUS', 'MINUS'),
            ('left', 'MULTIPLY', 'DIVIDE')

        )

        def p_calc(p):
            #global result
            '''
            calc : expression
                | var_assign
                | empty
            '''
            data=run(p[1])
            dic={"resultado": str(data)}
            #print ("dic: " ,dic)
            json_object = json.dumps(dic, indent = 2)
            #print ("json_object: " ,json_object)
            with open("ejemplo.json", "w") as outfile:
                outfile.write(json_object)
            
            

        def p_var_assign(p):
            '''
            var_assign : NAME EQUALS expression
            '''
            p[0] = ('=', p[1], p[3])

        def p_expression(p):
            '''
            expression : expression MULTIPLY expression
                    | expression DIVIDE expression
                    | expression PLUS expression
                    | expression MINUS expression
            '''
            p[0] = (p[2], p[1], p[3])

        def p_expression_int_float(p):
            '''
            expression : INT
                    | FLOAT
            '''
            p[0] = p[1]

        def p_expression_var(p):
            '''
            expression : NAME
            '''
            p[0] = ('var', p[1])

        def p_error(p):
            print("Syntax error found!")

        def p_empty(p):
            '''
            empty :
            '''
            p[0] = None

        parser = yacc.yacc()

        env = {}

        def run(p):
            global env
            if type(p) == tuple:
                if p[0] == '+':
                    return run(p[1]) + run(p[2])
                elif p[0] == '-':
                    return run(p[1]) - run(p[2])
                elif p[0] == '*':
                    return run(p[1]) * run(p[2])
                elif p[0] == '/':
                    return run(p[1]) / run(p[2])
                elif p[0] == '=':
                    env[p[1]] = run(p[2])
                    return ''
                elif p[0] == 'var':
                    if p[1] not in env:
                        return 'Undeclared variable found!'
                    else:
                        return env[p[1]]
            else:
                return p

    
        response = request.json
        dni = response['resultado']
        parser.parse(dni)
        leer = json.loads(open('ejemplo.json').read())
        cambiar = leer["resultado"]
        response = jsonify(resultado=cambiar)
        
        
        return response
if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0')
   

# werp.py :: toy programming language, lispish and concise.

tokenize = lambda chars: chars.replace('(', ' ( ').replace(')', ' ) ').split()

def read_from_tokens(tokens):
		if len(tokens) == 0:
			raise SyntaxError('Unexpected EOF')
		token = tokens.pop(0)
		if token == "(":
			L = []
			while tokens[0] != ')': L.append(read_from_tokens(tokens))
			tokens.pop(0) # final ) pop
			return L
		elif token == ')': raise SyntaxError('unexpected `)`')
		else: return atom(token)

def atom(token):
	try: return int(token)
	except ValueError:
		try: return float(token)
		except ValueError:
			return Symbol(token)

parse = lambda program: read_from_tokens(tokenize(program))

Symbol 	= str
List 	= list
Number 	= (int, float)

class Env(dict):
	def __init__(self, params=(), args=(), outer=None):
		self.update(zip(params, args))
		self.outer = outer
	def find(self, var):
		if (var in self):
			return self
		else: 
			try: return self.outer.find(var)
			except StandardError, e:
				print "ERROR, undefined:", var
				sys.exit()

def standard_env():
	import math, operator as op
	import importlib
	env = Env()
	env.update(vars(math)) # sin, cos, etc.
	env.update({
		'+':op.add, '-':op.sub, '*':op.mul, '/':op.div,
		'>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '==':op.eq,
		'abs':		abs, 
		'append':	op.add,
		'apply': 	apply,
		'>>': 		lambda *x : x[-1],
		'car': 		lambda x: x[0],
		'cdr': 		lambda x: x[1:],
		'cons': 	lambda x,y: [x] + y,
		'eq?': 		op.is_,
		'equal?':	op.eq,
		'length': 	len,
		'list': 	lambda *x: list(x),
		'list?': 	lambda x: isinstance(x, list),
		'map': 		map,
		'max': 		max,
		'min': 		min,
		'not': 		op.not_,
		'null?':	lambda x: x==[],
		'number?': 	lambda x: isinstance(x, Number),
		'procedure?':callable,
		'space':	' ',
		'round':	round,
		'import':	lambda x: importlib.import_module,
		'symbol?': 	lambda x: isinstance(x, Symbol)
		})
	return env

global_env = standard_env()

class Procedure(object):
	def __init__(self, params, body, env):
		self.params, self.body, self.env = params, body, env
	def __call__(self, *args):
		return eval(self.body, Env(self.params, args, self.env))

def eval(x, env = global_env):
	if isinstance(x, Symbol):
		return env.find(x)[x]
	elif not isinstance(x, List):
		return x
	elif x[0] == '`' or x[0] == 'string':
		(_, exp) = x
		return exp
	elif x[0] == 'if':
		(_, test, _then, _else) = x
		exp = (_then if eval(test, env) else _else)
		return eval(exp, env)
	elif x[0] == 'var':
		(_, _var, exp) = x
		env[_var] = eval(exp, env)
	elif x[0] == 'fun':
		(_, params, body) = x
		return Procedure(params, body, env)
	else:
		proc = eval(x[0], env)
		args = [eval(exp, env) for exp in x[1:]]
		return proc(*args)

run = lambda prg: eval(parse(prg))

import sys

def tryReadFile():
	if len(sys.argv) == 2:
		script, filename = sys.argv

		try: fh = open(filename, "r")
		except IOError:
			print "invalid filename"
			sys.exit()

		contents = fh.read()
		fh.close()
		print run(contents)
		sys.exit()	

tryReadFile()

print run("(>> (var r 10) (* pi (* r r)))") # 314.159265359
print run("(if (> (* 11 11) 120) (* 7 6) (` oops))") # 42
print run("(>> (var h (` hello)) (var w (` world)) (+ h (+ space w)))") # hello world
print run("""
	(>> 
		(var h (` hello)) 
		(var w (` world)) 
		(+ h (+ space w))
	)
	""") # hello world

print run("""
	(>>
		(var p 1)
		(if (== p 1) (string yes) (string no))
	)
	""") # yes

print run("""

	(>> 
		(var twice (fun (x) (* x 2)))
		(twice 21)
	)

	""")

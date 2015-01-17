toy programming language, lispish and concise

for fun, based off http://norvig.com/lispy.html

the name comes from the ease of typing `werp`

```scheme
(>> 
	(var h (` Hello)) 
	(var w (` World)) 
	(+ h (+ space w))
)
```
`Hello World`

---

- [x] function declaration
- [x] run code from .wrp file
- [ ] handle argv -x `(>> hello)`
- [ ] std lib python imports
- [ ] string handling `"bla"` instead of `(` bla)`
- [ ] comments handing `-- line comment`

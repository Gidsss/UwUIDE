# UwU++

Automata Project for 3rd Year

# Table of Contents
- [Get Started](#get-started)
- [UwU Console Script Package](#uwu-console-script-package)
- [Unit Testing](#unit-testing)
- [Language Tour](#language-tour)
    - [Hello World](#hello-world)
    - [IO](#io)
    - [Declaration and Assignment](#declaration-and-assignment)
    - [Function Declaration and Calling](#function-declaration-and-calling)
    - [Type System](#type-system)
    - [Constants](#constants)
    - [Classes](#classes)
    - [Control Flow](#control-flow)
        - [If-Else](#if-else)
        - [Loops](#loops)
            - [While Loop](#while-loop)
            - [For Loop](#for-loop)

# Get Started

1. Create a virtual environment `python -m venv .env`
2. Activate environment For CMD `.env\scripts\activate` For bash `source .env/bin/activate`
3. Install UwU Console Script Package (below)

# UwU Console Script Package

1. Install the UwU Console Script Package `python -m pip install ./packages/uwu`

2. To install | uninstall packages from `requirements.txt`

```bash
uwu install
uwu uninstall
```

3. To install | uninstall individual packages

```bash
uwu install < package name >
uwu uninstall < package name >
```

4. To run all tests `uwu test`
5. To run a specific test

```bash
uwu test test_*
uwu test *_test
```

6. To build UwU IDE `uwu build`

7. To run lexer package `uwu lexer`. Lexed text is in `./files/package-lexer.uwu`

8. To run parser package `uwu parser`. Parsed text is in `./files/package-parser.uwu`

9. To run analyzer package `uwu analyzer`. Analyzed text is in `./files/package-analyzer.uwu`

10. To run the compiler package `uwu compile`. Compiled text is in `./files/packages-compile.uwu`


# Unit Testing

1. For unit testing, we'll be using `pytest`
2. To create a test file, simply follow these file formats: `test_*.py` or `*_test.py`
3. For more information, please refer to the official [Pytest documentation](https://docs.pytest.org/en/7.1.x/getting-started.html#)

---

# Language Tour
## Hello World
All programs must have a mainuwu function
- must have no arguments
- must return nothing (aka return type `san`)
```kotlin
>.< this is a comment

fwunc mainuwu-san() [[
    pwint("hello", "world")~
]]
```
output: `hello world`

## IO
Printing to console can be done using the builtin `pwint` function.
- takes a variable amount of arguments of any type.
- arguments are separated by space when printed

Taking input from user can be done using the builtin `inpwt` function.
- takes one argument only (any type)
- arg will be printed to the console as the prompt
- will read user input until the user presses enter.
- user input will be implicitly converted to the type declared if `inpwt()` is
the right hand side of a declaration/assignment
- `inpwt()` can also be a standalone statement, not needing to be on the right hand side of a declaration/assignment

```kotlin
>.< this is a comment

fwunc mainuwu-san() [[
    >.< inpwt is implicitly converted to senpai
    name-senpai = inpwt("what is your first name?: ")~
    pwint("hello", name, "\n")~

    age-chan = 0~
    >.< inpwt is implicitly converted even in assignments
    >.< here, age is still a chan
    age = inpwt("what is your age?: ")~
    pwint(age, "was my age a few weeks ago!\n")~

    >.< inpwt as a standalone statement
    inpwt("Press Enter to exit...")~
]]
```
output:
```
what is your name?: uwu
hello uwu

what is your last name?: 1000
1000 was my age a few weeks ago!

Press Enter to exit...
```
## Declaration and Assignment
1. Variable declarations are in the format: `name-type = value~`
2. Assignments are done in the format:`name = value~`.

```kotlin
global-chan = 99~ 

fwunc mainuwu-san() [[
    >.< this is constant
    num-chan = 1~ 

    >.< reassigning global variable
    global = 0~
    pwint(global, num, global2)~
]]

global2-chan = 2~
```
output: `0 1 2`

## Function Declaration and Calling
Function declarations are in the format:<br>
`fwunc name-type(param-type, param2-type) [[ ... ]]`<br>
```kotlin
>.< this is a comment

fun main-san() [[
    pwint(sum(2,3))~
]]

>.< args: two chan
>.< returns: chan
fun sum-chan(left-chan, right-chan) [[
    wetuwn(left + right)~
]]
```
output: `5`

## Type System
1. `chan`: integer<br>
    declaration: `aqua-chan = 1~`<br>
<br>

2. `kun`: float<br>
    declaration: `shion-kun = 1.0~`<br>
<br>

3. `senpai`: string<br>
    declaration: `ojou-senpai = "hi"~`<br>
    `senpai` literals are enclosed in `"`<br>
    - indexing into a `senpai` value returns another `senpai` value
    ```kotlin
    aqua-senpai = "hello"~
    peko-senpai = aqua[1]~
    ```
<br>

4. `sama`: boolean<br>
    declaration: `lap-sama = fax~` (True)<br>
    declaration: `lap-sama = cap~` (False)<br>
<br>

5. `san`: null
    - used for functions that never return anything
    - identifiers that have this type can only have the value `nuww` (null)<br>
    function declaration: `fwunc mainuwu-san() [[ ... ]]`<br>
    declaration: `aqua-san = nuww~`<br>
<br>

## Constants

declare a constant by adding `-dono` after the type declaration:
- `aqua-chan-dono = 1~ >.< constant int`<br>
- `shion-senpai-dono = "hwats!?" >.< constant string~`<br>

## Classes
1. Classes are user defined types with properties and methods
2. Format:
```kotlin
cwass CwassName() [[
    property1-chan~
    
    fwunc method1-senpai() [[
        wetuwn("woah")~
    ]]
]]
```
3. Declare a variable with a `cwass` type in this format:<br>
`name-CwassName = CwassName()~`
4. Add constructor parameters to a class by:
```kotlin
cwass CwassName(constructorParam1-chan, constructorParam2-senpai) [[
    property1-chan~
]]

fwunc mainuwu-san() [[
    >.< all constructors must be initialized
    var-CwassName = CwassName(1, "hello")~
]]
```
5. Access properties and methods from a variable using `.`
```kotlin
cwass CwassName(constructorParam1-chan, constructorParam2-senpai) [[
    property1-chan~
    fwunc method-senpai() [[
        wetuwn("hello method")~
    ]]
]]

fwunc mainuwu-san() [[
    var-CwassName = CwassName(1, "hello")~
    pwint(
        var.property1,
        var.constructorParam1,
        var.constructorParam2,
        var.method()
    )~
]]
```
6. Inside a class, you do not need `self` or `this` to access properties
and constructor params. Just use it as normal like so:
```kotlin
cwass CwassName(constructorParam1-chan) [[
    property1-chan~
    
    fwunc method1-chan() [[
        wetuwn(property1 + constructorParam1)~
    ]]
]]
```
## Control Flow
### If-Else

Use `iwf`, `ewse`, and `ewif` for branching. Enclose condition in parentheses
```kotlin
fwunc mainuwu-san() [[
    aqua-chan = inpwt("input a number: ")~
    iwf (aqua > 1) [[
        pwint(aqua, "is less than 1")
    ]] ewse iwf (aqua == 1) [[
        pwint("one")
    ]] ewse [[
        pwint(aqua, "is more than 1")
    ]]
]]
```
output:
```
input a number: 3
3 is more than 1
```
### Loops
#### While Loop
Execute block of code as long as condition stays true. Format:
```kotlin
fwunc mainuwu-san() [[
    aqua-chan = 0~
    whiwe (aqua < 18) [[
        aqua = inpwt("How old are you?: ")~
    ]]
    pwint("ok")~
]]
```
output:
```
How old are you?: 10
How old are you?: -1000
How old are you?: 18
ok
```
#### For Loop
Format is:<br>
`fow (init~ condition~ update) [[ ... ]]`<br>
where:
- `init` is the initial value declaration
- `condition` is the stop condition of the for loop
- `update` is the update assigned to the initial value on each iteration
```kotlin
>.< this is a comment

fwunc mainuwu-san() [[
    >.< print 1 to 3
    fow (i-chan = 1~ i <= 3~ i+1) [[
        pwint(i)~
    ]]
    pwint()~

    >.< keep prompting the user until they type "uwu"
    fow (
        a-senpai = ""~
        a == "uwu"~
        a = inpwt("input owo: ")
    ) [[
        pwint(a)~
    ]]
    pwint("\ndone")~
]]
```
output:
```
1
2
3

'  '
input owo: no
'no'
input owo: NO!
'NO!'
input owo: owo
'uwu'

done!
```

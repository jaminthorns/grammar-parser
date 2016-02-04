# Grammar Parser

This is a recursive top-down parser that I wrote as a project for a course in
college.

To run the parser, give the filename of a file containing a grammar:

    python Derive.py Examples/Date_Format.txt


I used Backus-Naur Form for the grammar syntax, using
[this](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_Form) Wikipedia article
as an example:

    ; Grammar defining proper format for a date according to ISO 8601
    <S> ::= <Y> "-" <M> "-" <T>

    ; Year
    <Y> ::= <D> <D> <D> <D>

    ; Month
    <M> ::= "0" <D> | "1" <A>
    <A> ::= "0" | "1" | "2"

    ; Date
    <T> ::= "0" <D> | "1" <D> | "2" <D> | "3" <B>
    <B> ::= "0" | "1"

    ; Digits
    <D> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"


On start, the parser will display the grammar from the file in a compact,
readable form:

    S -> Y-M-T
    Y -> DDDD
    M -> 0D | 1A
    A -> 0 | 1 | 2
    T -> 0D | 1D | 2D | 3B
    B -> 0 | 1
    D -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9


Then, it will ask you for a string to derive from the grammar, as well as a
separator for the terminals (if needed):

    String to be derived (type "_" for lambda or press Enter to quit): 2016-12-25
    Separator that divides terminals (press Enter for none):


After inputting the string, the list of derivations from the starting character
to the final string of terminals is displayed:

    S => Y-M-T => DDDD-M-T => 2DDD-M-T => 20DD-M-T => 201D-M-T => 2016-M-T => 2016-1A-T => 2016-12-T => 2016-12-2D => 2016-12-25

I've also included the paper I wrote for the course, which explains the general
concept behind the implementation.

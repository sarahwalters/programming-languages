## Homework 6

1. For loops
    - Syntax: for loops use fairly standard C-style syntax: `for (var i = 0; (lt? i 3); i <- (+ i 1)) { print i; }`
    - Examples: see `test_for` in [./homework6_test.py](./homework6_test.py)

2. String operations
    - Syntax: standard C-style syntax with a \ as an escape character
    - Examples: see `test_string` in [./homework6_test.py](./homework6_test.py)
    - Transcript of Operations:
    ```
          imp> var x = "\"hello\"";
            x defined
          imp> print x;
            "hello"
          imp> print (length x);
            7
          imp> print (substring x 0 2);
            "h
          imp> print (concat x " riccardo");
            "hello" riccardo
          imp> print (startswith x "\"");
            true
          imp> print (endswith x "\"");
            true
          imp> print (lower "HELLO");
            hello
          imp> print (upper x);
            "HELLO"
    ```

3. Procedures
    - Implementation: Procedures are instantiated with the expression `procedure name ( args ) stmt` where name is the name of the procedure, args is the arguments expected of the procedure, and stmt is the statement that will be run when the procedure is called. The procedure declaration syntax parses to a EProcedure which evaluates to an VProcedure. When parsed by the shell this VProcedure is associated with the corresponding name of the procedure in the environment. A procedure is called using the syntax `name( args )`. This is parses to an ECall expression which will grab the associated stmt body out of the environment and evaluate the statement body with the appropriate arguements.
    - Transcript:
    ```
          imp> procedure print_plus_one (x) {x <- (+ x 1); print x;}
            print_plus_one defined
          imp> print_plus_one(1);
            2
    ```
    
4. Arrays
    - Implementation: Arrays are instantiated with the expression `(new-array e)`, where `e` is the length of the array which is created. The `new-array` syntax parses to` EArray`, which evaluates to `VArray`. Array methods are defined on `VArray` in the style of the `initial_env_imp` primitive operation declarations.
    - Examples: see `test_array` in [./homework6_test.py](./homework6_test.py)
    - Quicksort:
        - The quicksort procedure:
            ```
            procedure quicksort(arr, start, stop) {
                if (gt? (- stop start) 1) {
                    var pivot = (with arr (index (- stop 1)));
                    var q = start;

                    for (var i = start; (lt? i (- stop 1)); i <- (+ i 1)) {
                    if (lte? (with arr (index i)) pivot) {
                        do (with arr (swap i q));
                        q <- (+ q 1);
                    }
                }

                do (with arr (swap q (- stop 1)));

                quicksort(arr, start, q);
                quicksort(arr, (+ q 1), stop);
            }
            ```

        - A procedure which generates an array of length `len`, fills it with random integers between `0` and `len * 10` (inclusive), quicksorts it, and prints it
            ```
            procedure test_quicksort(len) {
                var test = (new-array len);
                var max = (* len 10);

                for (var i = 0; (lt? i len); i <- (+ i 1)) {
                    test[i] <- (random max);
                }

                quicksort(test, 0, len);

                print test;
            }
            ```

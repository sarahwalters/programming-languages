## Homework 6

1. For loops
    - Syntax: for loops use fairly standard C-style syntax: `for (var i = 0; (lt? i 3); i <- (+ i 1)) { print i; }`
    - Examples: see `test_for` in [./homework6_test.py](./homework6_test.py)

2. String operations


3. Procedures


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

Foreign Function Interface Generator
------------------------------------

`genffi` generates an interface file in an easy-to-parse s-expression
format with all the information needed to call library functions
through a C API.  It derives function signatures, struct/union layouts,
offsets, and sizes, enum and constant values.  It also unwinds typedefs
and follows simple macro renames.

It was written for
the [Irken language](https://github.com/samrushing/irken-compiler),
which needs to be able to call functions in dynamic link libraries
through libffi and llvm.

Note: `genffi` is a part of the Irken distribution, and is written in
Irken.  This repo is an experiment in redistributing pre-compiled
applications.  You can find the original sources in `ffi/gen/genffi.scm`
in the Irken distribution.

Input Format
------------

Sample input file for `stdio`:

    ;; -*- Mode: lisp -*-
    
    (brotli
      (includes "brotli/encode.h" "brotli/decode.h")
      (cflags "")
      (lflags "-lbrotlienc -lbrotlidec")
      (enums BrotliEncoderMode BrotliEncoderOperation BrotliEncoderParameter
             BrotliDecoderResult BrotliDecoderParameter)
      (constants
       BROTLI_MAX_WINDOW_BITS
       BROTLI_LARGE_MAX_WINDOW_BITS
       BROTLI_MIN_INPUT_BLOCK_BITS
       BROTLI_MAX_INPUT_BLOCK_BITS
       BROTLI_MIN_QUALITY
       BROTLI_MAX_QUALITY)
      (sigs
       BrotliEncoderSetParameter
       BrotliEncoderCreateInstance
       BrotliEncoderDestroyInstance
       BrotliEncoderMaxCompressedSize
       BrotliEncoderCompress
       BrotliEncoderCompressStream
       BrotliEncoderIsFinished
       BrotliEncoderHasMoreOutput
       BrotliEncoderTakeOutput
       BrotliEncoderVersion
       )
      )


The first symbol gives a name to the interface, in this case `brotli`. Then:

  * `includes` lists the C API `.h` file[s].
  * `cflags`, `lflags`: compile and link flags for `CC`.
  * `structs` lists the structures you need to know about. [you need not list opaque types here]
  * `constants` integer values you need (usually from `#define`).
  * `sigs` functions whose signatures you need.

Building
--------

    $ make

Running
-------

    $ ./genffi -gen brotli.ffi

There are other options, see the [Irken documentation](https://github.com/samrushing/irken-compiler/blob/master/ffi/gen/README.md) for more information.

What do I do with the output?
-----------------------------

S-expressions are very simple to parse.  I've included a simple reader
capable of reading both the inputs and outputs of this program, in the
file `lisp.py`.  You might be tempted to convert it to json, but you
shouldn't.

types
-----

Types are presented (mostly) in a prefix notation.  Numeric types are collapsed
into a single symbol, so `unsigned long long` becomes `ulonglong`.

Pointers are of the form `(* int)`, meaning `int *` in C.
`(* (* int))` would mean `int **`.

    (* (fun (* void) uint -> (* int))

Is a pointer to a function that takes two arguments, `void*` and `unsigned int`, and returning `int *`.

`struct` definitions
--------------------

Here's a sample `struct` definition:

    (struct sockaddr 16
      (0 sa_len uchar)
      (1 sa_family uchar)
      (2 sa_data (array 14 char))
     )

`sizeof (struct sockaddr)` is 16 bytes.  The first slot is an `unsigned char`, at
offset 0.  The second slot is also `unsigned char`, at offset 1.  The
third slot, `sa_data`, is at offset 2 and is an array of 14
`char`. [i.e., `char sa_data[14]`]

`con` definitions
-----------------

    (con SOME_NAME 34)

This simply says that the constant `SOME_NAME` has the integer value 34.

`sig` definitions
-----------------

    (sig recv (int (* void) ulong int -> long))

This declares `recv` as a function taking four arguments:

  1. `int`
  2. `void*`
  3. `unsigned long`
  4. `int`

And returning a `long`.

    (sig some_integer int)

This indicates that the symbol `some_integer` points to an integer rather than a function.

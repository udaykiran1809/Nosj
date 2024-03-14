# SUMMARY
The nosj data format is the latest and greatest way to serialize data such that it can be shared across arbitrary channels, languages, and applications.
Although formats like JSON, XML, and protocol-buffers already exist, they do
not subscribe to nosj's philosophy of "No one ever needs more than three
data-types!". nosj was created for the purpose of allowing even the most
complex data structures to be represented in an ascii-only format useful for
all known situations usage.

A nosj object consists of a root-level map containing zero or more key-value
pairs (see map data-type). One of the core design-goals of nosj is to all the
unmarshalled data types to be handled by almost any languages' built-in data
types and using only the languages built-in libraries for example
(non-inclusive possibilities listed):
	- Java
		- nosj num == double or int
		- nosj simple-string == java.lang.String OR byte[]
		- nosj complex-string == java.lang.String OR byte[]
		- nosj map == java.util.HashMap<String, Object>
	- Python
		- nosj num == float or int
		- nosj simple-string == str OR bytes
		- nosj complex-string == str OR bytes
		- nosj map == dict
	- golang
		- nosj num == float64 or int
		- nosj simple-string == string OR byte[]
		- nosj complex-string == string OR byte[]
		- nosj map == map[string]{}interface

# DATA-TYPES

The nosj format consists of three data-types: maps, nums, and strings. Each is
described in-depth below.

# Data-Type: num
A nosj num represents a numerical value between positive-infinity and
negative-infinity. A marshalled num consists of the ascii-character "f", an
optional ascii-dash representing a negative-sign ("-"), one or more
ascii-digits ("0" through "9"), a decimal point, one or more ascii-digits ("0"
through "9"), and the ascii-character "f".

Examples:
    Marshalled nosj num: f12.32f
    Numerical value: 12.32

    Marshalled nosj num: f-5678.0f
    Numerical value: -5678

# Data-Type: string
A nosj string is a sequence of ascii bytes which can be used to represent
arbitrary internal data such as ascii, unicode, or raw-binary. There are two
distinct representations of a nosj string data-type as described below.

### Representation #1: Simple-Strings
In the simple representation, the string is restricted to a set of
commonly-used ascii characters which (according to our extensive market survey)
are the most-liked among humans (i.e. all ascii letters and numbers, spaces ("
" / 0x20), and tabs ("\t", 0x09)). Simple-strings are followed by a trailing
"s" which is NOT part of the data being encoded.

Examples:
    Marshalled nosj simple-string: abcds
    String value: "abcd"

    Marshalled nosj simple-string: ef ghs
    String value: "ef gh"

### Representation #2: Complex-Strings
In the complex representation, the string is percent-encoded in order to reuse
pre-existing and well-tested libraries such as those used for encoding/decoding
URLs. Where as simple-string may only contain a restricted set of bytes,
complex-strings can encode arbitrary bytes but the marshalled-form MUST include
at least one (1) percent-encoded byte (sometimes called "URL-encoding").

Examples:
    Marshalled nosj complex-string: ab%2Ccd
    String value: "ab,cd"

    Marshalled nosj complex-string: ef%00gh
    String value: "ef<null-byte>gh"

# Data-Type: map
A nosj map is a sequence of zero or more key-value pairs that take the form of
"<key-1:value-1,key-2:value-2,...>" similar to the conceptual hash-map data
structure. A nosj map MUST start with a two left angle-bracket ("<<") and end
with two right angle-bracket (">>") and map keys MUST be an ascii-string
consisting of one or more lowercase letters ("a" through "z") only. Map values
may be any of the three canonical nosj data-types (map, string or num) and
there is no specification-bound on how many maps may be nested within each
other. Though map values are not required to be unique, map keys MUST be unique
within the current map (though they may be duplicated in maps at other levels
of "nesting").

Examples:
    Marshalled nosj map: <<x:abcds>>
    Key-1: "x"
    Value-1: "abcd" (string)

    Marshalled nosj map: <<x:abcds,y:f1.23f>>
    Key-1: "x"
    Value-1: "abcd" (string)
    Key-2: "y"
    Value-2: 1.23 (num)

    Marshalled nosj map: <<x:<<y:f1.23f>>>>
    Key-1: "x"
    Value-1: (map)
        Key-1-1: "y"
        Value-1-1: 1.23 (num)

A properly formatted nosj map containst NO WHITESPACE characters unless it is
as part of one of the below special-cases:
	- Whitespace is part of a simple-string which is part of that string.
		- Valid: "<<a:b s>"
	- Whitespace is before or after the start/end of the map which should be
	  ignored.
		- Valid: "      <<a:bs>>"
		- Valid: "<<a:bs>>     "

Examples of invalid whitespace:
		- "<<a :bs>>"
		- "<< a:bs>>"
		- "<<a:bs >>"

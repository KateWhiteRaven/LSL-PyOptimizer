[ llXorBase64Strings("𒍅", "")
, llXorBase64Strings("", "")
, llXorBase64Strings("Hello, World", "")
, llXorBase64Strings("AAAAA==AAAAA=", "_X")
, llXorBase64Strings("AAAAAA......AAAAAAA", "BCDEFG=====")
, llXorBase64Strings("AAAAA===AAAAAAAAAAA", "BCDEF")
, llXorBase64Strings("Hello, World!", "A")
, llXorBase64Strings("Hello, World!", "A=")
, llXorBase64Strings("Hello, World!", "A?")
, llXorBase64Strings("Hello, World!", "A?A")
, llXorBase64Strings("Hello, World!", "+")
, llXorBase64Strings("Hello, World!", "++")
, llXorBase64Strings("Hello, World!", "=")
, llXorBase64Strings("Hello, World!", "+=")
, llXorBase64Strings("Hello, World!", "+?")
, llXorBase64Strings("Hello, World!", "+??")
, llXorBase64Strings("Hello, World!", "+???")
, llXorBase64Strings("Hello, World!", "+????")
, llXorBase64Strings("Hello, World!", "+?????")
, llXorBase64Strings("Hello, World!", "+???????")
, llXorBase64Strings("Hello, World!", "/")
, llXorBase64Strings("Hello, World!", "//")
, llXorBase64Strings("Hello, World!", "^")
, llXorBase64Strings("Hello, World!", ".")
, llXorBase64Strings("Hello, World!", "_")
, llXorBase64Strings("Hello, World!", "_XX")
, llXorBase64Strings("Hello, World!", "XYZ")
, llXorBase64Strings("Hello, World!", "XYZ?")
, llXorBase64Strings("Hello, World!", "XYZXYZ")
, llXorBase64Strings("Hello, World!", "XYZXYZ==")
, llXorBase64Strings("AAAAA===AAAAAAAAAAA", "BCDEF")
, llXorBase64Strings("AAAAA===AAAAAAAAAAA", "BCDEF=")
, llXorBase64Strings("AAAAA===AAAAAAAAAAA", "BCDEF==")
, llXorBase64Strings("AAAAA===AAAAAAAAAAA", "BCDEF===")
, llXorBase64Strings("AA_AAA______AAAAAAAAAAAAA", "BC=EFG==")
, llXorBase64Strings("AA_AAA______AAAAAA=AAAAAA", "BC=EFG==")
, llXorBase64Strings("AAAAA==AAAAA", "_XXXXXXX")
, llXorBase64Strings("ABCDABCDABCDABCDABCDABCDABCD", "ABCD")
, llXorBase64Strings("BCDABCDABCDABCDABCDABCDABCDA", "BCDA")
, llXorBase64Strings("AA_AAA______AAAAAAAAAAAAA", "=5gbbW==oWVbj=")
, llXorBase64Strings("ABCDABCDABCD", "ABC=")
, llXorBase64Strings("AQCDAQCD", "AQC=")
]
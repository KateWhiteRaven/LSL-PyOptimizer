[ llXorBase64StringsCorrect("𒍅", "")
, llXorBase64StringsCorrect("", "ABCD")
, llXorBase64StringsCorrect("", "?")
, llXorBase64StringsCorrect("AB", "?")
, llXorBase64StringsCorrect("AABA", "1234")
, llXorBase64StringsCorrect("1234", "AABA")
, llXorBase64StringsCorrect("BAAA", "1234")
, llXorBase64StringsCorrect("1234", "BAAA")
, llXorBase64StringsCorrect("AABA", "AABA")
, llXorBase64StringsCorrect("AABA", "AABC")
, llXorBase64StringsCorrect("AABC", "AABA")
, llXorBase64StringsCorrect("Hello, World!", "XYZXYZ")
, llXorBase64StringsCorrect("QG8y", "XYZXYZ")
, llXorBase64StringsCorrect("ABCDABCDABCDABCDABCDABCDABCD", "ABCD")
, llXorBase64StringsCorrect("BCDABCDABCDABCDABCDABCDABCDA", "BCDA")
, llXorBase64StringsCorrect("ABCD", "ABCD")
, llXorBase64StringsCorrect("ABCDABCDABCD", "ABCD")
, llXorBase64StringsCorrect("AACD", "AACD")
, llXorBase64StringsCorrect("AQCD", "AQCD")
, llXorBase64StringsCorrect("AQCDAQCD", "AQC=")
, llXorBase64StringsCorrect("AQCDAQCD", "AQCD")
, llXorBase64StringsCorrect("ACCD", "AC==")
, llXorBase64StringsCorrect("ABCD", "AB==")
, llXorBase64StringsCorrect("ABCD", "ABC=")
, llXorBase64StringsCorrect("APCD", "APC=")
, llXorBase64StringsCorrect("AQCD", "AQC=")
, llXorBase64StringsCorrect("ACCD", "ABC=")
, llXorBase64StringsCorrect("ARCD", "ARC=")
, llXorBase64StringsCorrect("ABCDABCDABCDABCDABCDABCDABCD", "AB==")
, llXorBase64StringsCorrect("ABCDABCDABCDABCDABCDABCDABCD", "AQ==")
, llXorBase64StringsCorrect("ABCDABCDABCDABCDABCDABCDABCD", "ABCDAP//")
, llXorBase64StringsCorrect("ABCDABCDABCD", "ABC=")
, llXorBase64StringsCorrect("AQCDAQCD", "AQC=")
]

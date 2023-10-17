DICTIONARY = {
  "BFPV": "1",
  "CGJKQSXZ": "2",
  "DT": "3",
  "L": "4", "MN": "5", "R": "6",
  "AEIOUHWY": "."
}
 
def soundex_generate(token, size=7):
  token = token.replace(' ','').upper()
  soundex = token[0]

  for char in token[1:]:
    for key in DICTIONARY.keys():
      if char in key:
        code = DICTIONARY[key]
        if code != '.':
          if code != soundex[-1]:
            soundex += code
  
  soundex = soundex[:size].ljust(size,"0")
  return soundex

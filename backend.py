import pandas as pd
import sys
import os
import re, math
from collections import Counter
from nltk.tokenize import regexp_tokenize
import string

WORD = re.compile(r'\w+')

# Convert text to lower-case and strip punctuation/symbols from words
def normalize_text(text):
    norm_text = text.lower()

    # Replace breaks with spaces
    norm_text = norm_text.replace('<br />', ' ')

    norm_text = [word.strip(string.punctuation) for word in norm_text.split(" ")]
    # Pad punctuation with spaces on both sides
    #for char in ['.', ',', '(', ')', '!', '?', ';', ':']:
    #    norm_text = norm_text.replace(char, ' ' + char + ' ')

    # norm_text = preprocess_string(norm_text)
    # norm_text = regexp_tokenize(norm_text, pattern='\w+|\$[\d\.]+|\S+')

    return norm_text
  
def get_cosine(vec1, vec2):
  '''  
  Example of how to use this function
  text1 = 'This is a foo bar sentence .'
  text2 = 'This sentence is similar to a foo bar sentence .'

  vector1 = text_to_vector(text1)
  vector2 = text_to_vector(text2)

  cosine = get_cosine(vector1, vector2)
  
  print cosine:
  0.861640436855
  '''
  
  intersection = set(vec1.keys()) & set(vec2.keys())
  numerator = sum([vec1[x] * vec2[x] for x in intersection])

  sum1 = sum([vec1[x]**2 for x in vec1.keys()])
  sum2 = sum([vec2[x]**2 for x in vec2.keys()])
  denominator = math.sqrt(sum1) * math.sqrt(sum2)

  if not denominator:
    return 0.0
  else:
    return float(numerator) / denominator

def text_to_vector(text):
#   words = WORD.findall(text)
  words = normalize_text(text)
  return Counter(words)

if __name__ == "__main__":
  print sys.argv
  if len(sys.argv) < 2:
    input_file = 'songs.csv'
    cols = ['col1', 'col2', 'col3']
    rows = [0, -1]
    sheet = ['Sheet1']
  else:
    input_file = sys.argv[2]
    cols = [sys.argv[3], sys.argv[4], sys.argv[5]]
    rows = [sys.argv[6], sys.argv[7]]
    sheet = sys.argv[8]
    
  if os.path.isfile(input_file):
    if 'csv' in input_file: 
      data = pd.read_csv(input_file, skiprows=rows[0], usecols=cols)
    elif 'xlsx' in input_file:
      data = pd.read_excel(input_file, skiprows=rows[0], usecols=cols, sheetname=sheet)  
  
  # Drop the Null's?
  data.dropna(inplace=True)
  
  # Do a groupby over column 1, then 2: sum column 3
  X = data.groupby([cols[1], cols[0]]).agg({cols[2]: sum})
  
  songs = data[[cols[1]]].drop_duplicates()
  songs.columns = ['songs']
  songs['vec'] = songs['songs'].apply(text_to_vector)
  
  
  
  

  
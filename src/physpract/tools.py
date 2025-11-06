import os
import re

ersetzungen = {
  '0': 'null',
  '1': 'eins',
  '2': 'zwei',
  '3': 'drei',
  '4': 'vier',
  '5': 'fuenf',
  '6': 'sechs',
  '7': 'sieben',
  '8': 'acht',
  '9': 'neun'
}

class DataSave:
  def __init__(self, path: str):
    self.path = path
    os.makedirs(os.path.dirname(path), exist_ok=True)

  def save(self, name: str, value: str):
    data: dict[str, str] = {}

    # read existing file
    if os.path.exists(self.path):
      with open(self.path, 'r', encoding='utf-8') as f:
        for line in f:
          line = line.strip()
          if not line:
            continue
          m = re.match(r'^\\newcommand\{\\daten(?P<key>[A-Za-z]+?)\}\{(?P<value>.*)\}$', line)
          if m:
            data[m.group('key')] = m.group('value')

    # update
    data[name] = value

    # write back
    with open(self.path, 'w', encoding='utf-8') as f:
      for k, v in data.items():
        kk = k
        for num, word in ersetzungen.items():
          kk = re.sub(num, word, kk)
        kk = re.sub(r'[^A-Za-z]', '', kk)
        f.write(f'\\newcommand{{\\daten{kk}}}{{{v}}}\n')

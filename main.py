from cfg import crops
import json
import random

defaultdata = {
"name": "", 
"money": 10.0, 
"multiplier": 1.0, 
"xp": 0, 
"farmslots": 1, 
"farms": {"apple": 0, "mango": 0}, 
"crops": {}
}

autosell = 'true' #work on this later

pdata = None
try:
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  print("Welcome back,", pdata['name'])
except FileNotFoundError:
    pdata = defaultdata
    pdata['name'] = input("Welcome to antfarm\nInput Name\n> ")
    with open('pdata.json', 'w') as f:
      json.dump(pdata, f)
  
def help(args):
  print(f'''
  h - Shows this menu
  x - Exit game
  p - Shows your profile
  f - Harvest crops
  b - Buy farms (b [crop] [amount])
  m - Opens shop menu (WIP)
  ~n - Change your name
  ~r - Reset game
  ''')

def quit(args):
  print("Goodbye")
  exit()
  
def stats(args):
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  print(f'''Name: {pdata['name']}
Money: {pdata['money']}
Multiplier: {pdata['multiplier']}x
Farm Slots: {pdata['farmslots']}''')

def namechange(args):
  newn = input("New Name: (Leave blank for no change)\n~")
  if newn != '':
    pdata['name'] = newn
    with open('pdata.json', 'w') as f:
      json.dump(pdata, f)
  else:
    print('Name not changed')
  
def reset(args):
  ans = input("Are you sure you want to reset? (y/N)\n~ ")
  if ans.lower() == "y":
    pdata = defaultdata
    pdata['name'] = input("Welcome to antfarm\nInput Name\n> ")
    with open('pdata.json', 'w') as f:
      json.dump(pdata, f)
  else:
    print("Reset cancelled")

def buy(args):
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  if args == []:
    print('Type "s" for shop')
  elif args[0] in pdata['farms']:
    try:
      amt = int(args[1])
      print(amt)
    except:
      amt = 1
    if pdata['money'] >= crops[args[0]]['buy-price'] * amt:
      if pdata['farmslots'] > sum(pdata['farms'].values()):
        pdata['farms'][args[0]] += 1
        pdata['money'] -= crops[args[0]]['buy-price']
        with open('pdata.json', 'w') as f:
          json.dump(pdata, f)
        print("+1", args[0], "farm")
      else:
        print('No available farm slots.')
    else:
      print(f'''Not enough money, you need ${crops[args[0]]['buy-price']*amt - pdata['money']} more.''')
  else:
    print('Type "s" for shop')

def shop(args):
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  print("to do: market")

def harvest(args):
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  if sum(pdata['farms'].values()) == 0:
    print("You have no farms. Buy some from the market")
  else:
    totals = {}
    sellamt = 0
    print("Your ants harvested:")
    for farm, count in pdata['farms'].items():
      totals[farm] = int(round(count * crops[farm]['yield'] * random.uniform(1,2.5),0))
      try:
        pdata['crops'][farm] += totals[farm]
      except:
        pdata['crops'] = pdata['crops'] | totals
      with open('pdata.json', 'w') as f:
        json.dump(pdata, f)
      if totals[farm] > 0:
        print(f'''{totals[farm]} {farm}''')
      if autosell == 'true':
        for crop, count in pdata["crops"].items():
          sellamt += count * crops[crop]['sell-price']
          pdata['crops'][crop] -= count
          pdata['money'] += sellamt
    print(f'''Sold all for ${sellamt}''')
    
def invalid_command(args):
  print('Type "h" for help')

commands = {
  'h': help,
  'x': quit,
  'p': stats,
  'f': harvest,
  'b': buy,
  'm': shop,
  '~n': namechange,
  '~r': reset,
}

while True:
  inp = input('> ').split(' ')
  commands.get(inp[0], invalid_command)(inp[1:])
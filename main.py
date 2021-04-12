from cfg import crops
import json
import random

defaultdata = {
"name": "", 
"money": 10.0, 
"multiplier": 1.0, 
"xp": 0, 
"farmslots": 1, 
"autosell": "true", 
"farms": {"apple": 0, "mango": 0}, 
"crops": {}
}

pdata = None
try:
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  print(f'''
Welcome back {pdata['name']}
  ''')
except FileNotFoundError:
    pdata = defaultdata
    pdata['name'] = input("Welcome to antfrm\n Input Name\n> ")
    with open('pdata.json', 'w') as f:
      json.dump(pdata, f)
  
def help(args):
  print(f'''Commands:
| h - Shows this menu
| x - Exit game
| p - Shows your profile
| f - Harvest crops
| b - Buy farms (b [crop] [amount])
| m - Opens shop menu (WIP)

Options:
|~n - Change your name
|~a - Toggle Autosell
|~r - Reset game
  ''')

def quit(args):
  print("Goodbye\n")
  exit()
  
def stats(args):
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  print(f'''{pdata['name']}'s Profile:
| Money: {pdata['money']}
| Multiplier: {pdata['multiplier']}x
| Farm Slots: {pdata['farmslots']}
''')

def namechange(args):
  newn = input("New Name: (Leave blank for no change)\n~")
  if newn != '':
    pdata['name'] = newn
    with open('pdata.json', 'w') as f:
      json.dump(pdata, f)
  else:
    print('Name not changed\n')
  
def reset(args):
  ans = input("Are you sure you want to reset? (y/N)\n~ ")
  if ans.lower() == "y":
    pdata = defaultdata
    pdata['name'] = input("Welcome to antfrm\n Input Name\n> ")
    with open('pdata.json', 'w') as f:
      json.dump(pdata, f)
  else:
    print("Reset cancelled\n")

def buy(args):
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  try:
    clist = list(pdata['crops'].keys()).remove(args[0])
  except ValueError:
    clist = list(pdata['crops'].keys())
  if clist == None:
    clist = 0
  else:
    clist = len(clist)
  if args == []:
    print('Type "s" for shop\n')
  elif args[0] in pdata['farms']:
    try:
      amt = int(args[1])
    except:
      amt = 1
    if pdata['money'] >= crops[args[0]]['buy-price'] * amt:
      if pdata['farmslots'] > clist:
        pdata['farms'][args[0]] += 1
        pdata['money'] -= crops[args[0]]['buy-price']
        with open('pdata.json', 'w') as f:
          json.dump(pdata, f)
        print(f'''Bought {amt}x {args[0]} farm (-${crops[args[0]]['buy-price'] * amt})
        ''')
      else:
        print('No available farm slots.\n')
    else:
      print(f'''Not enough money, you need ${crops[args[0]]['buy-price']*amt - pdata['money']} more.
      ''')
  else:
    print('Type "s" for shop\n')

def shop(args):
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  print("to do: market\n")

def harvest(args):
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  if sum(pdata['farms'].values()) == 0:
    print("You have no farms. Buy some from the market\n")
  else:
    totals = {}
    sellamt = 0
    print("Your ants collected:")
    for farm, count in pdata['farms'].items():
      totals[farm] = int(round(count * crops[farm]['yield'] * random.uniform(1,2.5),0))
      try:
        pdata['crops'][farm] += totals[farm]
      except:
        pdata['crops'] = pdata['crops'] | totals
      with open('pdata.json', 'w') as f:
        json.dump(pdata, f)
      if totals[farm] > 0:
        print(f'''| + {totals[farm]} {farm}''')
      if pdata['autosell'] == "true":
        for crop, count in pdata["crops"].items():
          sellamt += count * crops[crop]['sell-price']
          pdata['crops'][crop] -= count
          pdata['money'] += sellamt
    if sellamt != 0:
      print(f'''| Sold all for ${sellamt}
      ''')
    else:
      print("")
    
def togglesell(args):
  with open('pdata.json','r') as f:
    pdata = json.load(f)
  if pdata['autosell'] == "true":
    pdata['autosell'] = "false"
    print("| Autosell toggled off\n")
    with open('pdata.json', 'w') as f:
      json.dump(pdata, f)
  elif pdata['autosell'] == "false":
    pdata['autosell'] = "true"
    print("| Autosell toggled on\n")
    with open('pdata.json', 'w') as f:
      json.dump(pdata, f)
    
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
  '~a': togglesell,
}

while True:
  inp = input('> ').split(' ')
  commands.get(inp[0], invalid_command)(inp[1:])
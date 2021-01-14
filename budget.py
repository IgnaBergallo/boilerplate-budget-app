from math import floor

class Category:

  def __init__(self, name):
    self.name = name
    self.ledger = list()
    self.balance = 0.0

  def __str__(self):    
    
    #title
    summary = "{:*^30s}\n".format(self.name)
    #budget summary
    for i in self.ledger:
      summary += "{0:<23s}{1:>7.2f}\n".format(i['description'][0:23], i['amount'])
      
    #Net income
    summary += "Total:{0:>7.2f}".format(self.balance)

    return summary
  
  def deposit(self, amount, description = str()):
    """This method receive:
    amount: a number, amount deposit.
    description: Is the description for deposit. Is an str"""
    
    self.ledger.append({"amount": amount, "description": description})
    self.balance += amount

    return

  def withdraw(self, amount, description = str()):

    '''This method should return True if the withdrawal took place, and False otherwise.
    This method receive a number 'amount' to withdraw and a description'''
    
    if self.check_funds(amount) == False:
      print('Not enough funds to withdraw that amount of money')
      return False
    
    self.ledger.append({"amount": -amount, "description": description})
    self.balance -= amount
    return True

  def get_balance(self):
    '''returns the current balance of the budget category based on the deposits and withdrawals that have occurred.''' 
    return self.balance

  def transfer(self, amount, destination):
    '''A transfer method that accepts an amount and another budget category as arguments. 
      The method add a withdrawal with the amount and the description "Transfer to [Destination Budget Category]". 
      The method then add a deposit to the other budget category with the amount and the description "Transfer from [Source Budget Category]". 
      If there are not enough funds, nothing will be added to either ledgers. This method returns True if the transfer took place, and False otherwise.'''

    if self.check_funds(amount) == False:
      return False
    
    self.withdraw(amount, 'Transfer to ' + destination.name)
    destination.deposit(amount, 'Transfer from ' + self.name)
    return True

  def check_funds(self, amount):
    '''check_funds method accepts an amount as an argument. 
    It returns False if the amount is greater than the balance of the budget category and returns True otherwise.'''

    if amount > self.balance:
      return False
    else:
      return True
  


def create_spend_chart(categories):
  '''It return a string that is a bar chart. The chart shows the percentage spent in each category passed in to the function.'''
  
  def chart_line(line, percentages):
    category_chart = '  '.join(['o' if percentage >= line else ' ' for percentage in percentages])
    return f'{str(line).rjust(3)}| {category_chart}  '

  def name_line(cat_names, k):
    name_line = '  '.join([cat_name.name[k] if k < len(cat_name.name) else ' ' for cat_name in cat_names])
    begin = ' '*5
    return f'{begin}{name_line}  '

  spendByCat ={k.name : sum(d['amount'] for d in k.ledger if d['amount']<0) for k in categories}
  totalSpend = sum(spendByCat.values())
  spendPercentage = {k : floor(10*(v/totalSpend))*10 for k,v in spendByCat.items()}
  linesPercentages = [i for i in range(100, -10, -10)] #100, 90, 90, etc.

  chartLines = '\n'.join([chart_line(line, spendPercentage.values()) for line in linesPercentages])
  title = "Percentage spent by category"
  dotLine = ' '*4 + '-'*3*len(categories) + '-'

  #chart name
  max_length = 0
  for i in categories:
    if max_length < len(i.name):
      max_length = len(i.name)

  name_lines = [name_line(categories, k) for k in range(max_length)]
  name_chart = '\n'.join(name_lines)

  return '\n'.join([title, chartLines, dotLine, name_chart])
class Stack:
  def __init__(self):
    self.items = []
    self.auxTokens = []

  def isEmpty(self):
    return self.items == []

  def Free(self):
    self.items = []

  def push(self, item):
    self.items.append(item)

  def pop(self,posicao=None):
    if posicao == None:
      return self.items.pop()
    else:
      return self.items.pop(posicao)

  def peek(self):
    return self.items[len(self.items)-1]

  def size(self):
    return len(self.items)

  def updateDesvio(self, item, pos):
    self.items[pos] = item
def find(iterable, predicate):
  """Find an element in a collection.

  :param iterable: Collection to iter in
  :type iterable: iter
  :param predicate: Predicate to use
  :type predicate: lambda

  """
  
  eles = list(filter(predicate, iterable))[:1]

  if eles:
    return eles[0]
  else:
    return None
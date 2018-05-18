import uuid, hashlib

def generate_checksum(data):
  """Generates a checksum from a raw string.

  :param data: Data for which you want an hex string
  :type data: str
  :rtype: str

  """

  return hashlib.sha256(data.encode('utf-8')).hexdigest()

def generate_hash():
  """Generates a random hash.

  :rtype: str

  """

  return uuid.uuid4().hex

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
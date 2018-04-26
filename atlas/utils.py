import uuid, hashlib

def generate_checksum(data):
  """Generates a checksum from a raw string.

  :param data: Data for which you want an hex string
  :type data: str
  :rtype: str

  """

  return hashlib.sha256(data.encode('utf-8')).hexdigest()

def resolve_parametric_intent_name(name, slots):
  """Format the intent name with slots dict to handle parametric intent name.

  With this feature, you can create generic intent and output a single intent name
  based on slots values.

  :param name: Name of the intent, may contain placeholders such as {slotName}
  :type name: str
  :param slots: Dictionary of slots values
  :type slots: dict

  """

  # TODO what to do if a slot value is an array?

  try:
    return name.format(**slots)
  except KeyError:
    return name

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
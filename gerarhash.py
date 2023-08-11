import hashlib

input = 'usuario'
hash = hashlib.sha512(str(input).encode("utf-8")).hexdigest()
print(hash)
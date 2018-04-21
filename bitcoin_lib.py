from bitcoin import *

pk1 = random_key()
pb1 = privtopub(pk1)
ad1 = privtoaddr(pk1)

pk2 = random_key()
pb2 = privtopub(pk2)
ad2 = privtoaddr(pk2)

pk3 = random_key()
pb3 = privtopub(pk3)
ad2 = privtoaddr(pk2)

multisig_script = mk_multisig_script(pb1, pb2, pb3, 2, 3)

multisig_script_address = scriptaddr(multisig_script)

address_history = history("3BMEXNscmUMXNh8QQ4M33GaMW7NuuhWzTX")

for i in address_history:
    print(i)

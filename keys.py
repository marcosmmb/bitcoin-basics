import os
import ecdsa # has to install
import hashlib
import base58 # has to install

def generate_private_key():
    # generates a random 32 bytes string that serves as private key
    return os.urandom(32).encode("hex")

def return_signing_key(private_key):
    # the signing key is obtained using the ecdsa SECP256k1
    # signature = sk.sign(msg)
    return ecdsa.SigningKey.from_string(private_key.decode("hex"), curve=ecdsa.SECP256k1)

def return_verifying_key(signing_key):
    # vk.verify(signature, msg)
    return signing_key.verifying_key

def generate_public_key(private_key):
    # the public key is the concatenation of a 0x04 byte with the verification key
    sk = return_signing_key(private_key)
    vk = return_verifying_key(sk)
    return ('\04' + vk.to_string()).encode("hex")

def return_bitcoin_address(public_key):
    # creates a new hashlib object called ripemd160
    ripemd160 = hashlib.new("ripemd160")
    # updates the object with the digest of the sha256(public_key)
    ripemd160.update(hashlib.sha256(public_key.decode("hex")).digest())
    # concatenates 0x00 with the digest of the ripemd160
    middle = '\00' + ripemd160.digest()
    # the checksum is the four first bytes of a double sha256 hashing of the middle variable
    checksum = (hashlib.sha256( hashlib.sha256(middle).digest() ).digest())[:4]
    # the binary address is the concatenation of the middle with the checksum
    bin_addr = middle + checksum
    # the bitcoin address is the base58 encoding of the 256 bytes string binary address
    address = base58.b58encode(bin_addr)
    return address

import random
from umbral import (
    SecretKey, Signer, CapsuleFrag,
    encrypt, generate_kfrags, reencrypt, decrypt_original, decrypt_reencrypted, Capsule)

# Generate an Umbral key pair
# ---------------------------
# First, Let's generate two asymmetric key pairs for Alice:
# A delegating key pair and a Signing key pair.

alices_secret_key = SecretKey.random()
alices_public_key = alices_secret_key.public_key()

alices_signing_key = SecretKey.random()
alices_verifying_key = alices_signing_key.public_key()
alices_signer = Signer(alices_signing_key)

# Encrypt some data for Alice
# ---------------------------
# Now let's encrypt data with Alice's public key.
# Invocation of `pre.encrypt` returns both the `ciphertext`,
# and a `capsule`. Anyone with Alice's public key can perform
# this operation.

plaintext = b'Proxy Re-encryption is cool!'
capsule, ciphertext = encrypt(alices_public_key, plaintext)
# print("capsule",dir(capsule))
# print("capsule get something",capsule.__bytes__().hex())
capsule = Capsule._from_exact_bytes(capsule.__bytes__())

# capsule,test = Capsule.from_public_key(alices_signing_key.public_key())
# newcaplsule.
# print(capsule.__bytes__().hex())

# print("ciphertext:",ciphertext.hex())

# Decrypt data for Alice
# ----------------------
# Since data was encrypted with Alice's public key,
# Alice can open the capsule and decrypt the ciphertext with her private key.

cleartext = decrypt_original(alices_secret_key, capsule, ciphertext)
# print("cleartext:",cleartext)

# Bob Exists
# -----------

bobs_secret_key = SecretKey.random()
bobs_public_key = bobs_secret_key.public_key()

# Bob receives a capsule through a side channel (s3, ipfs, Google cloud, etc)
bob_capsule = capsule

# Attempt Bob's decryption (fail)
try:
    fail_decrypted_data = decrypt_original(bobs_secret_key, bob_capsule, ciphertext)
except ValueError:
    print("Decryption failed! Bob doesn't has access granted yet.")

# Alice grants access to Bob by generating kfrags
# -----------------------------------------------
# When Alice wants to grant Bob access to open her encrypted messages,
# she creates *threshold split re-encryption keys*, or *"kfrags"*,
# which are next sent to N proxies or *Ursulas*.
# She uses her private key, and Bob's public key, and she sets a minimum
# threshold of 10, for 20 total shares

kfrags = generate_kfrags(delegating_sk=alices_secret_key,
                         receiving_pk=bobs_public_key,
                         signer=alices_signer,
                         threshold=1,
                         shares=20)

# Ursulas perform re-encryption
# ------------------------------
# Bob asks several Ursulas to re-encrypt the capsule so he can open it.
# Each Ursula performs re-encryption on the capsule using the `kfrag`
# provided by Alice, obtaining this way a "capsule fragment", or `cfrag`.
# Let's mock a network or transport layer by sampling `threshold` random `kfrags`,
# one for each required Ursula.

kfrags = random.sample(kfrags,  # All kfrags from above
                       1)      # M - Threshold

# Bob collects the resulting `cfrags` from several Ursulas.
# Bob must gather at least `threshold` `cfrags` in order to open the capsule.

cfrags = list()  # Bob's cfrag collection
for kfrag in kfrags:
    cfrag = reencrypt(capsule=capsule, kfrag=kfrag)
    cfrags.append(cfrag)  # Bob collects a cfrag

print("len",len(cfrags))
assert len(cfrags) == 1
print("cfrags:",cfrags)
# Bob checks the capsule fragments
# --------------------------------
# If Bob received the capsule fragments in serialized form,
# he can verify that they are valid and really originate from Alice,
# using Alice's public keys.

suspicious_cfrags = [CapsuleFrag.from_bytes(bytes(cfrag)) for cfrag in cfrags]

# print(len(suspicious_cfrags))
cfrags = [cfrag.verify(capsule,
                       verifying_pk=alices_verifying_key,
                       delegating_pk=alices_public_key,
                       receiving_pk=bobs_public_key,
                       )
          for cfrag in suspicious_cfrags]

# Bob opens the capsule
# ------------------------------------
# Finally, Bob decrypts the re-encrypted ciphertext using his key.

bob_cleartext = decrypt_reencrypted(receiving_sk=bobs_secret_key,
                                    delegating_pk=alices_public_key,
                                    capsule=bob_capsule,
                                    verified_cfrags=cfrags,
                                    ciphertext=ciphertext)

print("cfrags",cfrags)
print("kfrags",kfrags)
print("bob clear text:", bob_cleartext)
assert bob_cleartext == plaintext

bob_cleartext = decrypt_reencrypted(receiving_sk=bobs_secret_key,
                                    delegating_pk=alices_public_key,
                                    capsule=bob_capsule,
                                    verified_cfrags=cfrags,
                                    ciphertext=ciphertext)
print(bob_cleartext)
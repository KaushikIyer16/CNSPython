
from Crypto.Cipher import Blowfish

INPUT_SIZE = 8

def pad_string(str):

	new_str = str
	pad_chars = INPUT_SIZE - (len(str) % INPUT_SIZE)

	if pad_chars != 0:
		for x in range(pad_chars):
			new_str += " "
		

	return new_str

#plaintext = "Meet Kaushik and Mahesh at 7pm at Cool Corner."

def cryptBlowfish(publicKey, plaintext):
        crypt_obj = Blowfish.new(publicKey, Blowfish.MODE_ECB)
        return crypt_obj.encrypt(pad_string(plaintext))
        
def decryptBlowfish(ciphertext, publickey):
        #print "Plaintext: " + plaintext
        crypt_obj1 = Blowfish.new(publickey, Blowfish.MODE_ECB)
        #print "Blowfish Cyphertext: ",ciphertext
        return crypt_obj1.decrypt(ciphertext)

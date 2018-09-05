from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode

hash = "SHA-256"

def newkeys(keysize=1024):
    random_generator = Random.new().read
    key = RSA.generate(keysize, random_generator)
    private, public = key, key.publickey()
    return public, private

def importKey(externKey):
    return RSA.importKey(externKey)

def getpublickey(priv_key):
    return priv_key.publickey()

def encrypt(message, pub_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(message)

def decrypt(ciphertext, priv_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(ciphertext)

def sign(message, priv_key, hashAlg="SHA-256"):
    global hash
    hash = hashAlg
    signer = PKCS1_v1_5.new(priv_key)
    if (hash == "SHA-512"):
        digest = SHA512.new()
    elif (hash == "SHA-384"):
        digest = SHA384.new()
    elif (hash == "SHA-256"):
        digest = SHA256.new()
    elif (hash == "SHA-1"):
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.sign(digest)

def verify(message, signature, pub_key):
    signer = PKCS1_v1_5.new(pub_key)
    if (hash == "SHA-512"):
        digest = SHA512.new()
    elif (hash == "SHA-384"):
        digest = SHA384.new()
    elif (hash == "SHA-256"):
        digest = SHA256.new()
    elif (hash == "SHA-1"):
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.verify(digest, signature)


class RSA_Algo:
	def __init__(self,length, accuracy):
		self.p=self.miller_rabin_prime_gen(round(length/2)+1,accuracy)
		self.q=self.miller_rabin_prime_gen(round(length/2)+1,accuracy)
		self.n=self.p*self.q
		phi=(self.p-1)*(self.q-1)#n-(p+q-1)
		self.e=randgen.getrandbits(16)
		while(self.e<0 or self.e>phi or self.euclidean_gcd(self.e,phi)!=1):# and extended_euclidean(e,phi)<0):
			self.e=randgen.getrandbits(16)

		self.d=self.extended_euclidean(self.e,phi)[1]
		if self.d<0:
			self.d=self.d+phi #e*d mod phi = 1 <=> e*(d+phi) mod phi = 1
		print(length,"bit RSA key generated.")


	def miller_rabin_is_prime(self,n,k):
		if (n<3 or n&1!=1):
			return False
		r=0
		d=n-1
		while d & 1!=1:
			r=r+1
			d=d>>1  #d=d//2
		for i in range(k):
			a=randgen.randint(2,n-2)
			x=self.mod_pow_rtl(a,d,n)
			if x==1 or x==n-1:
				continue
			for j in range(1,r):
				x=self.mod_pow_rtl(x,2,n)
				if x==1:
					return False
				elif x==n-1:
					break
			if(x!=n-1):
				return False
		return True

	def mod_pow_rtl(self,b,e,m):
		result = 1
		b=b%m
		while e>0:
			if(e & 1==1):
				result=(result*b)%m
			e=e>>1
			b=(b*b)%m
		return result

	def miller_rabin_prime_gen(self,length,accuracy):
		randnum=randgen.getrandbits(length)
		while(self.miller_rabin_is_prime(randnum,accuracy)!=True):
			randnum=randgen.getrandbits(length)
		return randnum

	def euclidean_gcd(self,a,b):
		while b!=0:
			t=b
			b=a%b
			a=t
		return a

	def extended_euclidean_b(self,a,n):
		t=0
		newt=1024
		r=n
		newr=a
		while newr!=0:
			quotient = r//newr
			t=newt
			newt=t-quotient*newt
			r=newr
			newr=r-quotient*newr
		if r>1:
			print ("Not invertable.")
		if t<0:
			t= t+n
		return t

	def extended_euclidean(self,a,b):
		if (b==0):
			return [a,1,0]
		[d1,s1,t1] = self.extended_euclidean(b,a%b)
		d=d1
		s=t1
		t= s1-(a//b)*t1
		return [d,s,t]

	def chinese_remainder(self,p,q,d,c):
		dp=d%(p-1)
		dq=d%(q-1)
		qinv=self.extended_euclidean(q,p)[1]
		m1=self.mod_pow_rtl(c,dp,p)
		m2=self.mod_pow_rtl(c,dq,q)
		h=(qinv*(m1-m2))%p
		m=m2+(h*q)
		return m

	def encrypt_rsa(self,text,e,n):
		textinints=[]
		for c in text:
			textinints.append(ord(c))
		cipherblock=[]
		for i in textinints:
			cipherblock.append(self.mod_pow_rtl(i,e,n))

		return cipherblock

	def decrypt_rsa(self,cipherblock):
		decodedblock=[]
		for c in cipherblock:
			decodedblock.append(self.chinese_remainder(self.p,self.q,self.d,c))
		decodedtext=[]
		for d in decodedblock:
			decodedtext.append(chr(d))
		decodedtext=''.join(decodedtext)
		return decodedtext

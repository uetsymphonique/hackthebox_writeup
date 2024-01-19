def decrypt(enc_msg):
    pass


dictionary = dict()
for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_-+={}[]|;:<>,.?/'~` \n":
    dictionary[hex((ord(char) * 123 + 18) % 256)[2:].rjust(2, '0')] = char

print(dictionary)

with open('msg.enc', 'r') as msg_file:
    dec_msg = ''
    msg = msg_file.readline()
    for i in range(0, len(msg), 2):
        if msg[i:i + 2] in dictionary:
            dec_msg += dictionary[msg[i:i + 2]]
        else:
            dec_msg += '#'
    print(dec_msg)

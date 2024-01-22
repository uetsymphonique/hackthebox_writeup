def encrypt(key, data: bytes) -> bytes:
    ret = b''
    for i in range(len(data)):
        ret += bytes([data[i] ^ key[i % len(key)]])
    return ret


with open('output.txt', 'r') as input_file:
    enc_flag = bytes.fromhex(input_file.readline().split(': ')[1])
    start_of_flag = bytes("HTB{".encode())
    key = [start_of_flag[i] ^ enc_flag[i] for i in range(4)]
    print(encrypt(key, enc_flag).decode())
    # Output: HTB{rep34t3d_x0r_n0t_s0_s3cur3}


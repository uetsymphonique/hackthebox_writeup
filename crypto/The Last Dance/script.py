message = b"Our counter agencies have intercepted your messages and a lot "
message += b"of your agent's identities have been exposed. In a matter of "
message += b"days all of them will be captured"

with open('crypto_the_last_dance/out.txt', 'r') as inp_file:
    iv = bytes.fromhex(inp_file.readline())
    enc_msg = bytes.fromhex(inp_file.readline())
    enc_flag = bytes.fromhex(inp_file.readline())

    print(''.join(
        [chr(message[i] ^ enc_msg[i] ^ enc_flag[i]) for i in range(min(len(message), len(enc_msg), len(enc_flag)))]))
    # output: HTB{und3r57AnD1n9_57R3aM_C1PH3R5_15_51mPl3_a5_7Ha7}

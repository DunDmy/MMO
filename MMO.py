import sys

# This funtion produces a list of blocks
def get_blocks(block_size, plaint_text):
    # check if plaint text size is divisible by a block size
    if len(plaint_text) % block_size != 0:
        num_of_zeros = block_size - (len(plaint_text) % block_size)
        new_plaint_text = '0'* num_of_zeros + plaint_text
        return create_blocks(block_size, new_plaint_text, len(new_plaint_text))
    else:
        return create_blocks(block_size, plaint_text, len(plaint_text))


# This function creates a block
def create_blocks(block_size, plaint_text, plaint_size):
    blocks = []
    block = ''
    counter = 1
    #print(plaint_size)
    for i in range (0, plaint_size):
        # create a block
        block += plaint_text[i]
        if(counter == block_size):
            # append to the blcok and reset
            blocks.append(block)
            block = ''
            counter = 0
        counter += 1
    return blocks
    

# if the last bit in the string is 1, then g returns the same string
# if the last bit is 0, then g makes the last two bits 1s
def run_G_function(string_bits):
  
    if string_bits[len(string_bits) - 1] == '1':
        #print("G :" + string_bits)
        return string_bits
    else:
        string_bits_list = list(string_bits)
        string_bits_list[len(string_bits) - 1] = '1'
        string_bits_list[len(string_bits) - 2] = '1'
        string_bits_g = "".join(string_bits_list)
        #print("G :" + string_bits_g)
        return string_bits_g


# this function takes plaintext and converts into bits
def get_bits_from_plain(text_value):
    if check_default(text_value):
        return text_value
    else:
        bin_text = ''.join(format(ord(x), 'b') for x in text_value).zfill(128)
        return bin_text


# this function checks if values are from homework7 or module7 notes
def check_default(hw):
    if hw == '011100010111011100' or hw == '100100110111011':
        return True


# this function takes bin returnd dec
def get_dec(bin_val):
    dec_num = int(bin_val,2)
    return dec_num


# calculating xow of two strings of binary number a and b
def get_xor(left_text, right_text):
 
    xor_result = ""
    for i in range(0, len(left_text)):
        if left_text[i] == right_text[i]:
            xor_result = xor_result + "0"
        else:
            xor_result = xor_result + "1"

    return xor_result


def MMO_hash(plaintext, hash_text_file):

    hash_value = ''

    # H_0 these can be public values
    # in this case H_0 is defined as some arbitrary value
    H_0 = '11110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001110100110010111100111110111'
    block_size = len(H_0)

    # convert text to bits
    text_bits = get_bits_from_plain(plaintext)
  
    # condition used to update to homework parms
    if check_default(text_bits):
        if text_bits == '011100010111011100':
            H_0 = '010110'
            block_size = len(H_0)
        elif text_bits == '100100110111011':
            H_0 = '10001'
            block_size = len(H_0)

    list_of_blocks = get_blocks(block_size, text_bits)

    list_of_blocks.insert(0, H_0)

    H_l = len(list_of_blocks)
    block_l = len(list_of_blocks[0])

    # generate hash
    for i in range(1, H_l):
        g = get_dec(run_G_function(list_of_blocks[i - 1])) 
        x_i = get_dec(list_of_blocks[i])
        list_of_blocks[i] = get_xor(bin((g * x_i) % pow(2, block_l))[2:].zfill(block_l), list_of_blocks[i])
        hash_value = list_of_blocks[i]

    hash_text = hex(int(hash_value, 2))[2:]

    cipher_writer = open(hash_text_file, "a")
    cipher_writer.writelines(hash_text)
    cipher_writer.close()

    return 0


def main(argv):
    plain_text_file = argv[1]
    hash_text_file = argv[2]

    with open(plain_text_file, 'r') as reader:
            # handle a new line
            lines = (line.rstrip() for line in reader) 
            lines = list(line for line in lines if line)
            # read line
            for line in lines:
                MMO_hash(str(line), hash_text_file)


if __name__ == "__main__":
    main(sys.argv)

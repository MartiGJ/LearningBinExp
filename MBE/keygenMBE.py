import sys
def tohex(val):
  return hex((val + (1 << 32)) % (1 << 32))

def sign_extend(value):
    sign_bit = 1 << (8 - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

username = sys.argv[1].encode("ascii")

base =( username[3] ^ 0x1337) + 0x5eeded
print(hex(base))
for b in username:
    b_sign = sign_extend(b)
    serial = b_sign ^ base
    serial_mul = serial * 0x88233b2b
    serial_upper = serial_mul>>32
    new_var = serial - serial_upper
    new_var = new_var >> 1
    new_var += serial_upper
    new_var = new_var >> 10
    new_var = new_var * 0x539
    temp_var = serial-new_var
    base+= temp_var

print(base)

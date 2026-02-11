AutoTick = 0
InstructionsPerSecond = 5000
RPR = 0 # RAM Pointer Register m
SPR = 0 # Stack Pointer Register
FSPR = 0 # Function Stack Pointer Register
PCR = 0 # Program Counter Register
CMPregisterA = 0
CMPregisterB = 0
index = 0
FreeRegs = []*16
R = [0] * 16
RAM = [0] * 0x10000
flags = [0] * 12
PrgStackRoof = 0xffff
PrgStackFloor = 0xf0f0
FuncStackRoof = 0xf0ef
FunStackFloor = 0xeff0
VarRoof = 0xeeff
VarFloor = 0xe000
Pvar = 0xe000
PrgStack = [0] * 3855
FuncStack = [0] * 255
labels = {}
functions = {}
VarList = {}
VarNum = len(VarList)
CharList = ""
CharRef = {
    "a":0x01,
    "b":0x02,
    "c":0x03,
    "d":0x04,
    "e":0x05,
    "f":0x06,
    "g":0x07,
    "h":0x08,
    "i":0x09,
    "j":0x0a,
    "k":0x0b,
    "l":0x0c,
    "m":0x0d,
    "n":0x0e,
    "o":0x0f,
    "p":0x10,
    "q":0x11,
    "r":0x12,
    "s":0x13,
    "t":0x14,
    "u":0x15,
    "v":0x16,
    "w":0x17,
    "x":0x18,
    "y":0x19,
    "z":0x1a,
    "A":0x1b,
    "B":0x1c,
    "C":0x1d,
    "D":0x1e,
    "E":0x1f,
    "F":0x20,
    "G":0x21,
    "H":0x22,
    "I":0x23,
    "J":0x24,
    "K":0x25,
    "L":0x26,
    "M":0x27,
    "N":0x28,
    "O":0x29,
    "P":0x2a,
    "Q":0x2b,
    "R":0x2c,
    "S":0x2d,
    "T":0x2e,
    "U":0x2f,
    "V":0x30,
    "W":0x31,
    "X":0x32,
    "Y":0x33,
    "Z":0x34,
    "1":0x35,
    "2":0x36,
    "3":0x37,
    "4":0x38,
    "5":0x39,
    "6":0x3a,
    "7":0x3b,
    "8":0x3c,
    "9":0x3d,
    "0":0x3e,
    "|":0x3f,
    "_":0x40,
    "-":0x41,
    "+":0x42,
    "=":0x43,
    "nl":0x44,
    " ":0x45,
    "!":0x46,
    "?":0x47
}
ValRef = {
    0x01:"a",
    0x02:"b",
    0x03:"c",
    0x04:"d",
    0x05:"e",
    0x06:"f",
    0x07:"g",
    0x08:"h",
    0x09:"i",
    0x0a:"j",
    0x0b:"k",
    0x0c:"l",
    0x0d:"m",
    0x0e:"n",
    0x0f:"o",
    0x10:"p",
    0x11:"q",
    0x12:"r",
    0x13:"s",
    0x14:"t",
    0x15:"u",
    0x16:"v",
    0x17:"w",
    0x18:"x",
    0x19:"y",
    0x1a:"z",
    0x1b:"A",
    0x1c:"B",
    0x1d:"C",
    0x1e:"D",
    0x1f:"E",
    0x20:"F",
    0x21:"G",
    0x22:"H",
    0x23:"I",
    0x24:"J",
    0x25:"K",
    0x26:"L",
    0x27:"M",
    0x28:"N",
    0x29:"O",
    0x2a:"P",
    0x2b:"Q",
    0x2c:"R",
    0x2d:"S",
    0x2e:"T",
    0x2f:"U",
    0x30:"V",
    0x31:"W",
    0x32:"X",
    0x33:"Y",
    0x34:"Z",
    0x35:"1",
    0x36:"2",
    0x37:"3",
    0x38:"4",
    0x39:"5",
    0x3a:"6",
    0x3b:"7",
    0x3c:"8",
    0x3d:"9",
    0x3e:"0",
    0x3f:"|",
    0x40:"_",
    0x41:"-",
    0x42:"+",
    0x43:"=",
    0x44:"nl",
    0x45:" ",
    0x46:"!",
    0x47:"?"
}
OpcodeVal = {
    "mov":0x01, 
    "ldi":0x02,
    "add":0x03,
    "sub":0x04,
    "and":0x05,
    "or" :0x06,
    "not":0x07,
    "xor":0x08,
    "addi":0x09,
    "subi":0x0a,
    "andi":0x0b,
    "ori":0x0c,
    "xori":0x0d,
    "label":0x0e,
    "func":0x0f,
    "mul":0x10,
    "div":0x11,
    "mod":0x12,
    "cal":0x13,
    "ret":0x14,
    "cmp":0x15,     #! set Bit Flags in address 0xEF00
    "jnz":0x16,     #! Bit 15 
    "jez":0x17,     #! Bit 14
    "jgz":0x18,     #! Bit 13
    "jlz":0x19,     #! Bit 12
    "jlez":0x1a,    #! Bit 11
    "jgez":0x1b,    #! Bit 10
    "jme":0x1c,     #! Bit 7
    "jne":0x1d,     #! Bit 6
    "jmg":0x1e,     #! Bit 5
    "jml":0x1f,     #! Bit 4
    "jle":0x20,     #! Bit 3
    "jge":0x21,     #! Bit 2
    "jmp":0x22,     #! Bit not needed (Always jumps)
    "lir":0x23,     # Load into RAM
    "ata":0x24,     # Copy one value in an address to another
    "lor":0x25,     # Load out of RAM
    "disp":0x26,    # Display
    "disp1":0x27,   # Display next 7 bits
    "disp2":0x28,   # Display first 7 bits
    "rec":0x29,     # Receive character
    "ren":0x2a,     # Receive number
    "push":0x2b,    # Push into stack
    "pop":0x2c,     # Pop from stack
    "inter":0x2d,    # Interrupt
    "nop":0x2e,
    "hlt":0x2f,
    "var":0x30,
    "stv":0x31,
    "ldv":0x32,
    "sta":0x33,
    "stb":0x34,
    "stab":0x35,
    "cmi":0x36
}
OpRef = {
    0x01:"mov",  # done
    0x02:"ldi",  # done
    0x03:"add",  # done
    0x04:"sub",  # done
    0x05:"and",  # done
    0x06:"or" ,  # done
    0x07:"not",  # done
    0x08:"xor",  # done
    0x09:"addi", # done
    0x0a:"subi", # done
    0x0b:"andi", # done
    0x0c:"ori",  # done
    0x0d:"xori", # done
    0x0e:"label",# done
    0x0f:"func", # done
    0x10:"mul",  # done
    0x11:"div",  # done
    0x12:"mod",  # done
    0x13:"cal",  # done
    0x14:"ret",  # done
    0x15:"cmp",  # done
    0x16:"jnz",  # done
    0x17:"jez",  # done
    0x18:"jgz",  # done
    0x19:"jlz",  # done
    0x1a:"jlez", # done
    0x1b:"jgez", # done
    0x1c:"jme",  # done
    0x1d:"jne",  # done
    0x1e:"jmg",  # done
    0x1f:"jml",  # done
    0x20:"jle",  # done
    0x21:"jge",  # done
    0x22:"jmp",  # done
    0x23:"lir",  # done
    0x24:"ata",  # done
    0x25:"lor",  # done
    0x26:"disp", # done
    0x27:"disp1",# done
    0x28:"disp2",# done
    0x29:"rec",  # done
    0x2a:"ren",
    0x2b:"push", # done
    0x2c:"pop",  # done
    0x2d:"inter",
    0x2e:"nop",  # done
    0x2f:"hlt",  # done
    0x30:"var",  # done
    0x31:"stv",  # done
    0x32:"ldv",  # done
    0x33:"sta",  # done
    0x34:"stb",  # done
    0x35:"stab", # done
    0x36:"cmi"   # done
}
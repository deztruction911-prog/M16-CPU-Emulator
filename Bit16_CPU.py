from os import system, name
from getpass import getpass
from time import sleep
from asCompiler import tokenise, compile, TokenReference, tokens, token, variables, comparisons
from M16Variables import AutoTick, InstructionsPerSecond, RPR, SPR, FSPR, PCR, index, R, RAM, PrgStackRoof, PrgStackFloor, FuncStackRoof, FunStackFloor, VarRoof, VarFloor, Pvar, PrgStack, FuncStack, labels, functions, VarList, VarNum, CharList, CharRef, ValRef, OpcodeVal, OpRef, flags, CMPregisterA, CMPregisterB, FreeRegs

# Extra functions
def RAM_percent():
	percentage = 100 - (RAM.count(0) / 0xffff) * 100
	print("RAM used: {0:.1f}%".format(percentage))
def pad(text):
	return f"{text:<80}"
def clrs():
	system('cls')
def checkimm(val):
	val = (val + 32768) % 65536 - 32768
	return val
def unwrap(val):
	return val & 0xFFFF
def UpdatePrgStack():
	global RAM
	for i in range(len(PrgStack)):
		RAM[i+PrgStackFloor] = PrgStack[i]
def PushVal(val):
	global SPR, PrgStack
	while PrgStack[SPR] != 0:
		SPR += 1
		if SPR == len(PrgStack):
			exit("Stack Overflow")
	PrgStack[SPR] = val
	SPR += 1
	return None
def PopVal():
	global SPR, PrgStack
	SPR -= 1
	if SPR < 0:
		exit("Stack Underflow!")
	PoppedVal = PrgStack[SPR]
	PrgStack[SPR] = 0
	return PoppedVal
def FuncPush(val):
	global FSPR, FuncStack
	while FuncStack[FSPR] != 0:
		FSPR += 1
		if FSPR == len(FuncStack):
			exit("Stack Overflow")
	FuncStack[FSPR] = val
	FSPR += 1
	return None
def FuncPop():
	global FSPR, FuncStack
	FSPR -= 1
	if FSPR < 0:
		exit("Stack Underflow!")
	PoppedVal = FuncStack[FSPR]
	FuncStack[FSPR] = 0
	return PoppedVal

def PTR(program): # Program To RAM
	global RAM, index
	# Retrieve opcode
	for i in range(len(program)):
		opcode = program[i][0]
		try:
			operandA = program[i][1]
			operandB = program[i][2]
			operandC = program[i][3]
			operandD = program[i][4]
		except IndexError or TypeError:
			pass

		if opcode in ["nop", "hlt", "rec", "ret"]:
			RAM[index] = OpcodeVal[opcode]
			index += 1
		elif opcode in ["jnz", "jez", "jgz", "jlz", "jlez", "jgez", "jme", "jne", "jml", "jmg", "jmle", "jmge", "jmp"]:
			RAM[index] = OpcodeVal[opcode]
			index += 1
			RAM[index] = labels[operandA]
			index += 1
		elif opcode in ["add", "sub", "and", "or", "xor", "addi", "subi", "andi", "ori", "xori", "mul", "mod","div"]:
			if opcode == "not":
				RAM[index] = OpcodeVal["not"]
				index += 1
				RAM[index] = operandA
				index += 1
				RAM[index] = operandB
				index += 1
				continue
			RAM[index] = OpcodeVal[opcode]
			index += 1
			RAM[index] = operandA
			index += 1
			RAM[index] = operandB
			index += 1
			RAM[index] = operandC
			index += 1
		elif opcode in ["mov", "ldi", "lor", "lir", "ata", "push", "pop"]:
			if opcode == ["push", "pop"]:
				RAM[index] = OpcodeVal[opcode]
				index += 1
				RAM[index] = operandA
				index += 1
				continue
			RAM[index] = OpcodeVal[opcode]
			index += 1
			RAM[index] = operandA
			index += 1
			RAM[index] = operandB
			index += 1
		elif opcode == "cal":
			RAM[index] = OpcodeVal[opcode]
			index += 1
			RAM[index] = functions[operandA]
			index += 1
		elif opcode in ["stv", "ldv"]:
			RAM[index] = OpcodeVal[opcode]
			index += 1
			RAM[index] = VarList[operandA]
			index += 1
			RAM[index] = operandB
			index += 1
		elif opcode in ["disp1", "disp2", "disp"]:
			RAM[index] = OpcodeVal[opcode]
			index += 1
			RAM[index] = operandA
			index += 1
		elif opcode in ["sta", "stb", "stab"]:
			if opcode == "stab":
				RAM[index] = OpcodeVal[opcode]
				index += 1
				RAM[index] = CharRef[operandA]
				index += 1
				RAM[index] = CharRef[operandB]
				index += 1
				RAM[index] = operandC
				index += 1
				RAM[index] = operandD
				index += 1
				continue
			RAM[index] = OpcodeVal[opcode]
			index += 1
			RAM[index] = CharRef[operandA]
			index += 1
			RAM[index] = operandB
			index += 1


# Main opcodes and functions
def mov(Rx, Ry):
	global R
	R[Ry] = R[Rx]
	R[Ry] = checkimm(R[Ry])

def ldi(imm, Rx):
	global R
	imm = checkimm(imm)
	R[Rx] = imm

def add(Rx, Ry, Rz):
	global R
	R[Rz] = R[Rx] + R[Ry]
	R[Rz] = checkimm(R[Rz])

def sub(Rx, Ry, Rz):
	global R
	R[Rz] = R[Rx] - R[Ry]
	R[Rz] = checkimm(R[Rz])

def AND(Rx, Ry, Rz):
	global R
	R[Rz] = R[Rx] & R[Ry]
	R[Rz] = checkimm(R[Rz])

def OR(Rx, Ry, Rz):
	global R
	R[Rz] = R[Rx] | R[Ry]
	R[Rz] = checkimm(R[Rz])

def NOT(Rx, Ry):
	R[Ry] = ~R[Rx]
	R[Ry] = checkimm(R[Ry])

def xor(Rx, Ry, Rz):
	global R
	R[Rz] = R[Rx] ^ R[Ry]
	R[Rz] = checkimm(R[Rz])

def addi(imm, Rx, Ry):
	imm = checkimm(imm)
	R[Ry] = R[Rx] + imm
	R[Ry] = checkimm(R[Ry])

def subi(imm, Rx, Ry):
	imm = checkimm(imm)
	R[Ry] = R[Rx] - imm
	R[Ry] = checkimm(R[Ry])

def ori(imm, Rx, Ry):
	imm = checkimm(imm)
	R[Ry] = R[Rx] | imm
	R[Ry] = checkimm(R[Ry])

def andi(imm, Rx, Ry):
	imm = checkimm(imm)
	R[Ry] = R[Rx] & imm
	R[Ry] = checkimm(R[Ry])

def xori(imm, Rx, Ry):
	imm = checkimm(imm)
	R[Ry] = R[Rx] ^ imm
	R[Ry] = checkimm(R[Ry])

def mul(Rx, Ry, Rz):
	R[Rz] = R[Rx] * R[Ry]
	R[Rz] = checkimm(R[Rz])

def div(Rx, Ry, Rz):
	R[Rz] = R[Rx] // R[Ry]
	R[Rz] = checkimm(R[Rz])

def mod(Rx, Ry, Rz):
	R[Rz] = R[Rx] % R[Ry]
	R[Rz] = checkimm(R[Rz])

def cmp(Rx, Ry):
	global RAM
	addr = 0xef00
	RAM[addr] = 0
	if R[Rx] != 0:
		RAM[addr] += 0b0100000000000000
	if R[Rx] == 0:
		RAM[addr] += 0b0010000000000000
	if R[Rx] > 0:
		RAM[addr] += 0b0001000000000000
	if R[Rx] < 0:
		RAM[addr] += 0b0000100000000000
	if R[Rx] <= 0:
		RAM[addr] += 0b0000010000000000
	if R[Rx] >= 0:
		RAM[addr] += 0b0000001000000000
	if R[Rx] == R[Ry]:
		RAM[addr] += 0b0000000001000000
	if R[Rx] != R[Ry]:
		RAM[addr] += 0b0000000000100000
	if R[Rx] > R[Ry]:
		RAM[addr] += 0b0000000000010000
	if R[Rx] < R[Ry]:
		RAM[addr] += 0b0000000000001000
	if R[Rx] <= R[Ry]:
		RAM[addr] += 0b0000000000000100
	if R[Rx] >= R[Ry]:
		RAM[addr] += 0b0000000000000010

def cmi(Rx, imm):
	imm = checkimm(imm)
	addr = 0xef00
	RAM[addr] = 0
	if R[Rx] == imm:
		RAM[addr] += 0b0000000001000000
	if R[Rx] != imm:
		RAM[addr] += 0b0000000000100000
	if R[Rx] > imm:
		RAM[addr] += 0b0000000000010000
	if R[Rx] < imm:
		RAM[addr] += 0b0000000000001000
	if R[Rx] <= imm:
		RAM[addr] += 0b0000000000000100
	if R[Rx] >= imm:
		RAM[addr] += 0b0000000000000010

def jnz(label):
	global PCR
	condition = RAM[0xef00]
	if condition & 0b0100000000000000 == 0b0100000000000000:
		PCR = labels[label]

def jez(label):
	global PCR
	condition = RAM[0xef00]
	if condition & 0b0010000000000000 == 0b0010000000000000:
		PCR = labels[label]

def jgz(label):
	global PCR
	condition = RAM[0xef00]
	if condition & 0b0001000000000000 == 0b0001000000000000:
		PCR = labels[label]

def jlz(label):
	global PCR
	condition = RAM[0xef00]
	if condition & 0b0000100000000000 == 0b0000100000000000:
		PCR = labels[label]

def jlez(label):
	global PCR
	condition = RAM[0xef00]
	if condition & 0b0000010000000000 == 0b0000010000000000:
		PCR = labels[label]

def jgez(label):
	global PCR
	condition = RAM[0xef00]
	if condition & 0b0000001000000000 == 0b0000001000000000:
		PCR = labels[label]

def jme(label):
	global PCR
	condition = RAM[0xef00]
	if condition & 0b0000000001000000 == 0b0000000001000000:
		PCR = labels[label]

def jne(label):
	global PCR
	condition = RAM[0xef00]
	if condition & 0b0000000000100000 == 0b0000000000100000:
		PCR = labels[label]

def jmg(label):
	global PCR
	condition = RAM[0xef00]
	if condition & 0b0000000000010000 == 0b0000000000010000:
		PCR = labels[label]

def jml(label):
	global PCR
	condition = RAM[0xef00]
	if condition & 0b0000000000001000 == 0b0000000000001000:
		PCR = labels[label]

def jle(label):
	global PCR
	condition = RAM[0xef00]
	if condition & 0b0000000000000100 == 0b0000000000000100:
		PCR = labels[label]

def jge(label):
	global PCR
	condition = RAM[0xef00]
	if condition & 0b0000000000000010 == 0b0000000000000010:
		PCR = labels[label]

def jmp(label):
	global PCR
	PCR = labels[label]

def push(Rx):
	global PrgStack, RAM
	PushVal(R[Rx])
	UpdatePrgStack()

def pop(Rx):
	global PrgStack, RAM
	R[Rx] = PopVal()
	UpdatePrgStack()

def rec():
	global RAM
	try:
		user_input = input("Enter char: ")
	except EOFError:
		return None
	if user_input == '':
		char = "nl"
	else:
		char = user_input[0]
	CurrentAdr = 0xefe0
	while CurrentAdr < 0xefef and RAM[CurrentAdr] != 0:
		CurrentAdr += 1
	if CurrentAdr == 0xefef:
		for i in range(0xefe0, 0xefef):
			RAM[i] = 0
		CurrentAdr = 0xefe0
	if char in CharRef:
		RAM[CurrentAdr] = CharRef[char]

def disp1(addr):
	global CharList
	if RAM[addr] == 0:
		return None
	if addr > 0xef00 and addr < 0xeff0:
		char = RAM[addr]
		if char == CharRef["nl"]:
			CharList += "\n"
		char &= 0b1111111
		CharList += ValRef[char]

def disp2(addr):
	global CharList, RAM
	if RAM[addr] == 0:
		return None
	if addr > 0xef00 and addr < 0xeff0:
		char = RAM[addr]
		if CharRef["nl"]:
			CharList += "\n"
		char &= 0b11111110000000
		char = char >> 7
		CharList += ValRef[char]

def disp(addr):
	global CharList
	if RAM[addr] == 0:
		return None
	if addr > 0xef00 and addr < 0xeff0: 
		NextDisp = 1
		while NextDisp != 0:
			word = RAM[addr]
			charL = word & 0b1111111
			charH = (word & 0b11111110000000) >> 7
			NextDisp = (word & 0b100000000000000) >> 14
			addr += 1
			if charH == CharRef["nl"]: CharList += "\n"
			elif charH != 0: CharList += ValRef[charH]
			if charL == CharRef["nl"]: CharList += "\n"
			elif charL != 0: CharList += ValRef[charL]

def lir(Rx, Ry):
	global RAM
	if unwrap(R[Ry]) >= 0x0000 and unwrap(R[Ry]) <= 0xffff:
		RAM[unwrap(R[Ry])] = unwrap(R[Rx])
	else:
		return None

def lor(Rx, Ry):
	global RAM
	if unwrap(R[Ry]) >= 0x0000 and unwrap(R[Ry]) <= 0xffff:
		R[Rx] = checkimm(RAM[unwrap(R[Ry])])
	else:
		return None

def ata(addrA, addrB):
	addrA &= 0xffff
	addrB &= 0xffff
	RAM[addrB] = RAM[addrA]

def cal(FuncName):
	global RAM, FuncStack, PCR
	if FuncName in functions:
		clocktick = PCR
		PCR = functions[FuncName]
		FuncPush(clocktick)

def ret():
	global RAM, FuncStack, PCR
	PCR = FuncPop()

def var(VarName, VarValue):
	global RAM, Pvar
	VarList[VarName] = Pvar
	RAM[Pvar] = VarValue
	Pvar += 1
	if Pvar > VarRoof:
		Pvar = VarFloor

def ldv(VarName, Rx):
	global R
	try:
		pointer = VarList[VarName]
	except KeyError:
		return None
	R[Rx] = RAM[pointer]

def stv(VarName, Rx):
	global RAM
	try:
		pointer = VarList[VarName]
	except KeyError:
		return None
	RAM[pointer] = R[Rx]

def sta(char, addr):
	if char in CharRef and addr > 0xef00 and addr < 0xefe0:
		RAM[addr] = CharRef[char]

def stb(char, addr):
	if char in CharRef and addr > 0xef00 and addr < 0xefe0:
		RAM[addr] = CharRef[char] << 7

def stab(charB, charA, PrNext, addr):
	if charA in CharRef and charB in CharRef and addr > 0xef00 and addr < 0xefe0:
		RAM[addr] = (PrNext<<14) + (CharRef[charB]<<7) + CharRef[charA]

def nop():
	pass

def hlt():
	exit("Program halted")

program = [
	("label ta;"),
	("x = 90;"),
	("label tb;")
]

for i in range(len(program)):
	if program[i][0] == "label":
		LabelName = program[i][1]
		labels[LabelName] = i
for i in range(len(program)):
	if program[i][0] == "func":
		FuncName = program[i][1]
		functions[FuncName] = i
for i in range(len(program)):
	if program[i][0] == "var":
		var(program[i][1], program[i][2])

clrs()
PTR(program) # Call only once upon compilation
RunCode = 1
while RunCode == True:
	# Program end
	if PCR == len(program) + 1:
		print("Program finished successfully")
		exit()

	# Retrieve opcodes and operands
	# Set operands to --- when not available
	try:
		opcode = program[PCR][0]
	except IndexError:
		opcode = "---"

	try:
		operandA = program[PCR][1]
	except IndexError:
		operandA = "---"

	try:
		operandB = program[PCR][2]
	except IndexError:
		operandB = "---"

	try:
		operandC = program[PCR][3]
	except IndexError:
		operandC = "---"

	try:
		operandD = program[PCR][4]
	except IndexError:
		operandD = "---"

	# CPU states
	print("\033[H", end="")
	print(pad(f"Program Counter (Register 16): {PCR}"))
	print(pad(f"RAM pointer (Register 17): {RPR}"))
	print(pad(f"Stack Pointer: {SPR}"))
	print(pad(f"Function Stack Pointer: {FSPR}"))

	for i in range(0, 16, 2):
		reg_line = f"R{i}: {R[i]} | R{i+1}: {R[i+1]}"
		print(pad(reg_line))
	
	print(pad(""))
	print(pad(f"Opcode: {opcode}"))
	print(pad(f"opA: {operandA}"))
	print(pad(f"opB: {operandB}"))
	print(pad(f"opC: {operandC}"))
	print(pad(f"opD: {operandD}"))

	print(pad(""))

	num = 0b0100000000000000
	if opcode == "cmp":
		CMPregisterA = operandA
		CMPregisterB = operandB
	flags[0] = f"R{CMPregisterA} ! 0: " + f"{bool(((RAM[0xef00]) & num) >> 14)}"[0]
	num = num >> 1
	flags[1] = f"R{CMPregisterA} = 0: " + f"{bool(((RAM[0xef00]) & num) >> 13)}"[0]
	num = num >> 1
	flags[2] = f"R{CMPregisterA} > 0: " + f"{bool(((RAM[0xef00]) & num) >> 12)}"[0]
	num = num >> 1
	flags[3] = f"R{CMPregisterA} < 0: " + f"{bool(((RAM[0xef00]) & num) >> 11)}"[0]
	num = num >> 1
	flags[4] = f"R{CMPregisterA} <= 0:" + f"{bool(((RAM[0xef00]) & num) >> 10)}"[0]
	num = num >> 1
	flags[5] = f"R{CMPregisterA} >= 0:" + f"{bool(((RAM[0xef00]) & num) >> 9)}"[0]
	num = num >> 3
	flags[6] = f"R{CMPregisterA} = R{CMPregisterB}: " + f"{bool(((RAM[0xef00]) & num) >> 6)}"[0]
	num = num >> 1
	flags[7] = f"R{CMPregisterA} != R{CMPregisterB}: " + f"{bool(((RAM[0xef00]) & num) >> 5)}"[0]
	num = num >> 1
	flags[8] = f"R{CMPregisterA} > R{CMPregisterB}: " + f"{bool(((RAM[0xef00]) & num) >> 4)}"[0]
	num = num >> 1
	flags[9] = f"R{CMPregisterA} < R{CMPregisterB}: " + f"{bool(((RAM[0xef00]) & num) >> 3)}"[0]
	num = num >> 1
	flags[10] = f"R{CMPregisterA} <= R{CMPregisterB}: " + f"{bool(((RAM[0xef00]) & num) >> 2)}"[0]
	num = num >> 1
	flags[11] = f"R{CMPregisterA} >= R{CMPregisterB}: " + f"{bool(((RAM[0xef00]) & num) >> 1)}"[0]

	print("Last comparison result: ")
	for i in range(0, 12, 2):
		print(pad(f"{flags[i]} | {flags[i+1]}"))
	print(pad(""))
	print(pad(f"Variables | Pointer | Value"))

	for blank, variable in enumerate(VarList):
		print(pad(f"{variable} | {hex(VarList[variable])} | {RAM[VarList[variable]]}"))

	print(pad(""))
	print(pad(""))

	if AutoTick == False:
		getpass("Press enter to step")

	# Opcode/operand execution
	if opcode in ["rec", "ret", "nop", "hlt"]:
		string = opcode + "()"
		exec(string)
	elif opcode in ["jnz", "jez", "jgz", "jlz", "jlez", "jgez", "jme", "jne", "jml", "jmg", "jmle", "jmge", "jmp", "push", "pop", "disp1", "disp2", "disp", "cal"]:
		string = opcode + "(operandA)"
		exec(string)
	elif opcode in ["mov", "ldi", "not", "cmp", "cmi", "lir","lor", "ldv", "stv", "sta", "stb", "ata"]:
		string = "pass"
		if opcode == "not": NOT(operandA, operandB)
		else: string = opcode + "(operandA, operandB)"
		exec(string)
	elif opcode in ["add", "sub", "and", "or", "xor", "addi", "subi", "andi", "ori", "xori", "mul", "mod","div"]:
		string = "pass"
		if opcode == "and": AND(operandA, operandB, operandC)
		elif opcode == "or": OR(operandA, operandB, operandC)
		else: string = opcode + "(operandA, operandB, operandC)"
		exec(string)
	elif opcode in ["stab"]:
		string = opcode + "(operandA, operandB, operandC, operandD)"
		exec(string)
	elif opcode not in ["---", "label", "func", "var", "rec", "ret", "nop", "hlt", "jnz", "jez", "jgz", "jlz", "jlez", "jgez", "jme", "jne", "jml", "jmg", "jmle", "jmge", "jmp", "push", "pop", "disp1", "disp2", "disp", "cal", "mov", "ldi", "not", "cmp", "cmi", "lir","lor", "ldv", "stv", "sta", "stb", "add", "sub", "and", "or", "xor", "addi", "subi", "andi", "ori", "xori", "mul", "mod", "div", "stab"]:
		exit("Opcode not recognised: '{0}'".format(opcode))

	print(pad(""))
	print(pad(CharList))
	PCR += 1
	if AutoTick == True:
		sleep(1/InstructionsPerSecond)
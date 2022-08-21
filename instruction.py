from borsh_construct import *
InstructionEnum = Enum(
    "InitProgram",
    "RegisterUser" / CStruct("user_name" / Vec(U8)),
    "RewardXP" / CStruct("total_xp" / U64, "user_name" / Vec(U8)),
    "BlankInstruction",

    enum_name = "InstructionEnum"
)

def build_instruction(instruction):
    return InstructionEnum.build(instruction)

    
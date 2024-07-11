import idc
import ida_idaapi
import ida_kernwin
import idautils
import ida_name
import ida_bytes
import ida_ida
import ida_funcs
import ida_typeinf
import ida_segment
import ida_nalt
import ida_hexrays
import json
import itertools
import idaapi
import logging
import struct
import numpy as np
import llvmlite.binding as llvm
from llvmlite import ir

from contextlib import suppress

i8ptr = ir.IntType(8).as_pointer()
ptrsize = 64 if ida_idaapi.get_inf_structure().is_64bit() else 32
ptext = {}

def struct_info(tif, type_name):
    info = None
    udt_data = ida_typeinf.udt_type_data_t()
    tif.get_udt_details(udt_data)
    
    if type_name not in binaryinfo["struct"]:
        binaryinfo["struct"][type_name] = {}

        for idx in range(udt_data.size()):
            udt_member = udt_data.at(idx)

            if udt_member.type.is_array():
                child_tif = udt_member.type.get_ptrarr_object()
                if child_tif.is_func():
                    sub_type = "func"
                elif child_tif.is_ptr():
                    sub_type = "ptr"
                elif child_tif.is_udt():
                    sub_type = "struct"
                    info = struct_info(child_tif, udt_member.name)
                elif tif.is_float():
                    sub_type = "float"
                elif tif.is_double():
                    sub_type = "double"
                else:
                    sub_type = f"int{child_tif.get_size()*8}"

                count = udt_member.type.get_array_nelems()

                if info != None:
                    for index in range(count):
                        for offset in info:
                            binaryinfo["struct"][type_name][udt_member.offset // 8 + index * (child_tif.get_size()) + offset] = info[offset]
                else:
                    for index in range(count):
                        binaryinfo["struct"][type_name][udt_member.offset // 8 + index * (child_tif.get_size())] = f"{sub_type} {udt_member.name}"

            elif udt_member.type.is_func():
                sub_type = "func"
            elif udt_member.type.is_ptr():
                sub_type = "ptr"
            elif udt_member.type.is_udt():
                sub_type = "struct"
                info = struct_info(udt_member.type, udt_member.name)
            elif tif.is_float():
                sub_type = "float"
            elif tif.is_double():
                sub_type = "double"
            else:
                sub_type = f"int{udt_member.type.get_size()*8}"
    
            if info != None:
                for offset in info:
                    binaryinfo["struct"][type_name][udt_member.offset // 8 + offset] = info[offset]
            else:
                binaryinfo["struct"][type_name][udt_member.offset // 8] = f"{sub_type} {udt_member.name}"

    return binaryinfo["struct"][type_name]

def lift_tif(tif: ida_typeinf.tinfo_t, width = -1) -> ir.Type:
    """
    Lifts the given IDA type to corresponding LLVM type.
    If IDA type is an array/struct/tif, type lifting is performed recursively.

    :param tif: the type to lift, in IDA
    :type tif: ida_typeinf.tinfo_t
    :raises NotImplementedError: variadic structs
    :return: lifted LLVM type
    :rtype: ir.Type
    """
    if tif.is_func():
        ida_rettype = tif.get_rettype()                           
        ida_args = (tif.get_nth_arg(i) for i in range(tif.get_nargs()))
        is_vararg = tif.is_vararg_cc()                               
        llvm_rettype = lift_tif(ida_rettype)                            
        llvm_args = (lift_tif(arg) for arg in ida_args)
        return ir.FunctionType(i8ptr if isinstance(llvm_rettype, ir.VoidType) else llvm_rettype, llvm_args, var_arg = is_vararg) 

    elif tif.is_ptr():
        child_tif = tif.get_ptrarr_object()
        if child_tif.is_void():
            return ir.IntType(8).as_pointer()
        return lift_tif(child_tif).as_pointer()

    elif tif.is_array():
        child_tif = tif.get_ptrarr_object()
        element = lift_tif(child_tif)
        count = tif.get_array_nelems()
        if count == 0:
            # an array with an indeterminate number of elements = type pointer
            tif.convert_array_to_ptr()
            return lift_tif(tif)      
        return ir.ArrayType(element, count)

    elif tif.is_void():
        return ir.VoidType()

    elif tif.is_udt():
        udt_data = ida_typeinf.udt_type_data_t()
        tif.get_udt_details(udt_data)
        type_name = tif.get_type_name()
        context = ir.context.global_context
        
        type_name = "struct" if type_name == None else type_name

        if type_name not in context.identified_types:
            struct_t = context.get_identified_type(type_name)
            elementTypes = []
            for idx in range(udt_data.size()):
                udt_member = udt_data.at(idx)
                if udt_member.type.get_type_name() in context.identified_types:
                    elementTypes.append(context.identified_types[udt_member.type.get_type_name()])
                else:
                    element = lift_tif(udt_member.type)
                    elementTypes.append(element)

            struct_t.set_body(*elementTypes)

        struct_info(tif, type_name)
        return context.get_identified_type(type_name)

    elif tif.is_bool():
        return ir.IntType(1)

    elif tif.is_char():
        return ir.IntType(8)

    elif tif.is_float():
        return ir.FloatType()

    elif tif.is_double():
        return ir.DoubleType()

    elif tif.is_decl_int() or tif.is_decl_uint() or tif.is_uint() or tif.is_int():
        return ir.IntType(tif.get_size()*8)
        
    elif tif.is_decl_int16() or tif.is_decl_uint16() or tif.is_uint16() or tif.is_int16():
        return ir.IntType(tif.get_size()*8)
        
    elif tif.is_decl_int32() or tif.is_decl_uint32() or tif.is_uint32() or tif.is_int32():
        return ir.IntType(tif.get_size()*8)
        
    elif tif.is_decl_int64() or tif.is_decl_uint64() or tif.is_uint64() or tif.is_int64():
        return ir.IntType(tif.get_size()*8)
        
    elif tif.is_decl_int128() or tif.is_decl_uint128() or tif.is_uint128() or tif.is_int128():
        return ir.IntType(tif.get_size()*8)

    elif tif.is_ext_arithmetic() or tif.is_arithmetic():
        return ir.IntType(tif.get_size()*8)
        
    else:
        if width != -1:
            return ir.ArrayType(ir.IntType(8), width)
        else:
            return ir.IntType(ptrsize)

def initialize():
    """
    This function serves as a initial function with following steps.
    1. Decompile all functions.
    2. Collect all strings.
    3. Create GlobalVariabel for all IDA data item.

    ptext: dict to save decompile results {ea:decompile}
    str_dict: dict to save all strings
    """
    # decompile all functions
    for func in idautils.Functions():
        binaryinfo["function"][hex(func)] = ida_name.get_name(func)
        try:
            pfunc = ida_hexrays.decompile(func)
            if pfunc == None:
                continue
        except:
            continue

        count = {}
        for lvar in pfunc.lvars: 
            if hex(func) not in binaryinfo["vartype"]:
                binaryinfo["vartype"][hex(func)] = {}
    
            if lvar.is_arg_var:
                varname = f"arg"
            elif lvar.is_reg_var():
                varname = f"reg{lvar.get_reg1()}"
            else:
                varname = f"stack{lvar.get_stkoff()}"

            if varname not in count:
                count[varname] = 1
            else:
                count[varname] += 1

            varname = varname + "_" + str(count[varname])

            arg_t = lift_tif(lvar.tif)
            if isinstance(arg_t, ir.IdentifiedStructType):
                binaryinfo["vartype"][hex(func)][varname] = arg_t.name
            elif isinstance(arg_t, ir.PointerType) and isinstance(arg_t.pointee, ir.IdentifiedStructType):
                binaryinfo["vartype"][hex(func)][varname] = arg_t.pointee.name + " *"

if __name__ == "__main__":
    """
    This script run in IDApython.
    output: The text IR file to be saved.
    """
    idc.auto_wait()
    output = idc.ARGV[1]
    #########################################################################
    binaryinfo = {}
    binaryinfo["struct"] = {}
    binaryinfo["vartype"] = {}
    binaryinfo["function"] = {}
    #########################################################################
    initialize()
    json.dump(binaryinfo, open(f"{output}.label", "w"), indent=1)
    idc.qexit(0)
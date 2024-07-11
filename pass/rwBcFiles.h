#pragma once
#include "common.h"
llvm::Module* MyParseIRFile(llvm::StringRef filename);		
bool doWriteBackLL(llvm::Module* M, llvm::StringRef filename);
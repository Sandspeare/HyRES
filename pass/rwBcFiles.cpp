/*****************************************************************************
Filename: rwBcFiles.cpp
Date    : 2020-02-10 11:25:35
Description: Read and Write Intermedia Representation file
*****************************************************************************/
#include "rwBcFiles.h"
#include "llvm-c-14/llvm-c/Core.h"
/// \Read Intermedia Representation file
Module* MyParseIRFile(StringRef filename)
{
	SMDiagnostic Err;
	std::unique_ptr<Module> mod = nullptr;
		//blue 2023/12/6
	//llvm::LLVMContext globalContext; 
	LLVMContextRef globalContextref = LLVMGetGlobalContext();
	LLVMContext& globalContext = *(LLVMContext*)globalContextref;
	mod = llvm::parseIRFile(filename, Err, globalContext);
	if (!mod)
	{
		Err.print("Open Module file error", errs());
		return NULL;
	}
	Module *M = mod.get();
	if (!M)
	{
		errs() << ": error loading file '" << filename << "'\n";
		return NULL;
	}
	mod.release();
	return M;
}

/// \Write Intermedia Representation file
bool doWriteBackLL(Module* M, StringRef filename)
{
	std::error_code ErrorInfo;
	//std::unique_ptr<tool_output_file> out(new tool_output_file(filename, ErrorInfo, llvm::sys::fs::F_None));
	//blue 2023/12/6
	std::unique_ptr<llvm::ToolOutputFile> out(new llvm::ToolOutputFile(filename, ErrorInfo, llvm::sys::fs::OF_None));

	if (ErrorInfo)
	{
		errs() << ErrorInfo.message() << "\n";
		return false;
	}
	M->print(out->os(), NULL);
	out->keep();
	return true;
}


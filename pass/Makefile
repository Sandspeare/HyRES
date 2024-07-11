CC = gcc
CFLAGS = -Wall -Wextra -fpermissive -g 
INCLUDES = /usr/lib/llvm-14/include
#LIBS = LLVMCodeGen LLVMIRReader LLVMBitReader LLVMBitWriter LLVMipo LLVMMC LLVMAsmParser LLVMTransformUtils LLVMAnalysis LLVMCore LLVMSupport
#LIBS = LLVMExtensions
LIBS = LLVMTableGen LLVMLTO LLVMSparcInfo LLVMDebugInfoCodeView LLVMMCDisassembler LLVMCFIVerify LLVMBitReader LLVMMipsAsmParser LLVMHexagonAsmParser LLVMPowerPCAsmParser LLVMLanaiDisassembler LLVMM68kDisassembler LLVMDWP LLVM-14.0.0 LLVMM68kDesc LLVMVEDisassembler LLVMAArch64Desc LLVMAMDGPUDisassembler LLVMHexagonInfo LLVMInstCombine LLVMAsmPrinter LLVMMSP430Desc LLVMRISCVInfo LLVMLanaiCodeGen LLVMAVRAsmParser LLVMVEAsmParser LLVMExegesisMips LLVMCore LLVMARMDesc LLVMWebAssemblyInfo LLVMPasses LLVMDlltoolDriver LLVMAMDGPUUtils LLVMExegesisPowerPC LLVMFrontendOpenACC LLVMRISCVDesc LLVMSymbolize LLVMXCoreInfo LLVMVEDesc LLVMJITLink LLVMTableGenGlobalISel LLVMRuntimeDyld LLVMHexagonCodeGen LLVMipo LLVMXCoreDisassembler LLVMMipsDesc LLVMExegesis LLVMMCA LLVMNVPTXInfo LLVMM68kAsmParser LLVMX86TargetMCA LLVMLanaiInfo LLVMARMInfo LLVMMSP430AsmParser LLVMX86Info LLVMAVRDisassembler LLVMAArch64CodeGen LLVMRemarks LLVMNVPTXCodeGen LLVMARMUtils LLVMSparcAsmParser LLVMAArch64Info LLVMXCoreCodeGen LLVMDemangle LLVMLinker LLVMScalarOpts LLVMWebAssemblyDisassembler LLVMMSP430CodeGen LLVMARMDisassembler LLVMM68kInfo LLVMInterfaceStub LLVMAArch64AsmParser LLVMMCJIT LLVMAArch64Utils LLVMHexagonDesc LLVMBPFDesc LLVMWebAssemblyUtils LLVMPowerPCCodeGen LLVMAMDGPUCodeGen LLVMFrontendOpenMP LLVMHexagonDisassembler LLVMDebugInfoPDB LLVMAMDGPUInfo LLVMWebAssemblyCodeGen LLVMWebAssemblyDesc LLVMFileCheck LLVMMCParser LLVMExegesisX86 LLVMAMDGPUTargetMCA LLVMMSP430Disassembler LLVMBitstreamReader LLVMMC LLVMObjectYAML LLVMCFGuard LLVMBitWriter LLVMM68kCodeGen LLVMInstrumentation LLVMAnalysis LLVMSystemZDisassembler LLVMExegesisAArch64 LLVMRISCVDisassembler LLVMAVRCodeGen LLVMCodeGen LLVMX86Disassembler LLVMWindowsManifest LLVMBPFInfo LLVMCoverage LLVMSystemZAsmParser LLVMWebAssemblyAsmParser LLVMNVPTXDesc LLVMAMDGPUDesc LLVMOrcShared LLVMSupport LLVMDebugInfoMSF LLVMDebugInfoGSYM LLVMSparcCodeGen LLVMTransformUtils LLVMBPFAsmParser LLVMDiff LLVM-14 LLVMVectorize LLVMOrcTargetProcess LLVMBinaryFormat LLVMDebugInfoDWARF LLVMVEInfo LLVMRISCVCodeGen LLVMSparcDisassembler LLVMIRReader LLVMPowerPCDesc LLVMAVRDesc LLVMObject LLVMMIRParser LLVMARMAsmParser LLVMInterpreter LLVMDebuginfod LLVMGlobalISel LLVMSystemZCodeGen LLVMOrcJIT LLVMAMDGPUAsmParser LLVMSparcDesc LLVMMSP430Info LLVMAVRInfo LLVMAsmParser LLVMLineEditor LLVMARMCodeGen LLVMLanaiDesc LLVMPerfJITEvents LLVMMipsInfo LLVMLibDriver LLVMCoroutines LLVMTarget LLVMMipsCodeGen LLVMXRay LLVMSystemZInfo LLVMRISCVAsmParser LLVMBPFDisassembler LLVMPowerPCInfo LLVMTextAPI LLVMOption LLVMFuzzMutate LLVMPowerPCDisassembler LLVMExecutionEngine LLVMProfileData LLVMSystemZDesc LLVMObjCARCOpts LLVMX86Desc LLVMDWARFLinker LLVMAggressiveInstCombine LLVMX86AsmParser LLVMAArch64Disassembler LLVMMipsDisassembler LLVMSelectionDAG LLVMVECodeGen LLVMXCoreDesc LLVMBPFCodeGen LLVMX86CodeGen LLVMLanaiAsmParser
BIN_DIR = ./bin
LIBRARY_DIRS = /usr/lib/llvm-14/lib

ExtractStaticInfo.o: ExtractStaticInfo.cpp
	$(CC) $(CFLAGS) -I$(INCLUDES) -c ExtractStaticInfo.cpp -o $(BIN_DIR)/ExtractStaticInfo.o

common.o: common.cpp
	$(CC) $(CFLAGS) -I$(INCLUDES) -c common.cpp -o $(BIN_DIR)/common.o

rwBcFiles.o: rwBcFiles.cpp
	$(CC) $(CFLAGS) -I$(INCLUDES) -c rwBcFiles.cpp -o $(BIN_DIR)/rwBcFiles.o

main.o: main.cpp
	$(CC) $(CFLAGS) -I$(INCLUDES) -c main.cpp -o $(BIN_DIR)/main.o

output: ExtractStaticInfo.o common.o main.o rwBcFiles.o
	$(CC) $(CFLAGS) -I$(INCLUDES) -o $(BIN_DIR)/facts $(BIN_DIR)/rwBcFiles.o $(BIN_DIR)/ExtractStaticInfo.o $(BIN_DIR)/common.o $(BIN_DIR)/main.o -L$(LIBRARY_DIRS) $(addprefix -l,$(LIBS)) -pthread -lm -ldl -lrt -lncurses -lstdc++
clean:
	rm -f $(BIN_DIR)/facts $(BIN_DIR)/ExtractStaticInfo.o $(BIN_DIR)/rwBcFiles.o $(BIN_DIR)/common.o $(BIN_DIR)/main.o
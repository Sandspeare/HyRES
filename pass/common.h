#pragma once

#include "llvm/ADT/Statistic.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/InlineAsm.h"
#include "llvm/Pass.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Transforms/Scalar.h"
#include "llvm/IR/InstIterator.h"
#include "llvm/Support/Casting.h"
#include "llvm/IR/DataLayout.h"
#include "llvm/IR/Instruction.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/GlobalValue.h" 
#include "llvm/Transforms/Scalar.h"
#include "llvm/Support/Allocator.h"
#include "llvm/IR/IntrinsicInst.h"
#include "llvm/IR/Intrinsics.h"
#include "llvm/IR/InstIterator.h"
#include "llvm/Support/BranchProbability.h"
#include "llvm/Analysis/BranchProbabilityInfo.h"
#include "llvm/CodeGen/MachineBranchProbabilityInfo.h"
#include "llvm/Support/BlockFrequency.h"
#include "llvm/Analysis/BlockFrequencyInfo.h"
#include "llvm/Analysis//BlockFrequencyInfoImpl.h"
#include "llvm/CodeGen/MachineBlockFrequencyInfo.h"
#include "llvm/Transforms/Utils/ValueMapper.h"
#include "llvm/Transforms/Utils/Cloning.h"
#include "llvm/Bitcode/BitcodeReader.h"
#include "llvm/Bitcode/BitcodeWriter.h"
#include "llvm/Support/ToolOutputFile.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/SourceMgr.h"
#include "llvm/IRReader/IRReader.h"
#include "llvm/CodeGen/GlobalISel/LoadStoreOpt.h"

#include "rwBcFiles.h"
#include <string>
#include <fstream>
#include <iostream>
#define  AddedPointer "AddedPointer"

using namespace llvm;
using namespace std;

int IfIntInlist(int num, vector<int> SearchList);
int IfFuncInlist(Function* Func, vector<Function*> SearchList);
int IfTypeInlist(int Start, Type* Ty, vector<Type*> SearchList);
int IfBlockInlist(BasicBlock* ins, vector<BasicBlock*> SearchIns);
int IfInstInList(Instruction* Func, vector<Instruction*> SearchList);
int IfStrInList(string Func, vector<string> SearchList);
int** MallocGraph(int size);
int** CopyGraph(int size, int** sourceGraph);
int** MatrixPlus(int** MatrixA, int** MatrixB, int MatrixLength);
int** MatrixMulti(int** tempMatrixA, int** tempMatrixB, int MatrixLength);
void doNormalDelete(Module *mod);

vector<Function*> EraseFuncFromList(Function* Func, vector<Function*> FuncList);
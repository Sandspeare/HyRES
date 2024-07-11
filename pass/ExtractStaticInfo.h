#pragma once
#include "common.h"
class ExtractStaticInfo
{
public:
	string GetInstIndex(Instruction * ins);
	bool IR2MicroCode(vector<Instruction*> trace);
	string GetGroundTruth(vector<Instruction*> trace);
	Function* RemoveFuncInst(Function *Func, vector<int> traceindex, string Name);
	bool ExtractFacts(Module * mod, string SavePath);
	int CheckOffset(Instruction* inst);
	bool AnlysisFlow(Instruction * inst, vector<Instruction*>* trace, vector<int>* field);
	Function* ExtractStaticInfo::CreateFunCopy(Function* OldFun);
	void AnlysisDefineFlow(Instruction *inst, vector<Instruction*> *trace, vector<BasicBlock*> *blklist);
	Function * CreateFuncFromInst(Module* mod, Function * OldFun, vector<Instruction*> tracelist, vector<BasicBlock*> blklist);
	void BaseInformation(Module * mod);
	void GlobalInfo(Module * mod, string SavePath);
	void FunctionInfo(Module * mod, string SavePath);
	void Instructions(Module * mod, string SavePath);
protected:
	vector<Function*> FuncList;
	vector<BasicBlock*> BlkList;
	vector<Instruction*> InstList;

};

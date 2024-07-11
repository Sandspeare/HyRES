#include "ExtractStaticInfo.h"

/// Returns the string representation of a llvm::Value* or llvm::Type*  
template <typename T> static std::string llvm_to_string(T* value_or_type) {
	std::string str;
	llvm::raw_string_ostream stream(str);
	value_or_type->print(stream, true);
	stream.flush();
	return str;
}

void ExtractStaticInfo::BaseInformation(Module * mod)
{
	for (Function &Func : *mod)
	{
		FuncList.push_back(&Func);
		for (BasicBlock &B : Func)
		{
			BlkList.push_back(&B);
			for (Instruction &I : B)
			{
				InstList.push_back(&I);
			}
		}
	}
}

void ExtractStaticInfo::GlobalInfo(Module * mod, string SavePath)
{
	DataLayout tmpDataLayout(mod);
	ofstream global;
	llvm::LLVMContext context;
	llvm::IRBuilder<> builder(context);
	global.open(SavePath + "//global.facts");
	for (Module::global_iterator gi = mod->global_begin(); gi != mod->global_end(); gi++)
	{
		GlobalVariable* g_value = &*gi;
		if (g_value->isConstant())
		{
			global << string(g_value->getName()) << ";constant;" << llvm_to_string(g_value->getValueType()) << ";" << tmpDataLayout.getTypeStoreSize(g_value->getValueType()) << ";";
		}
		else
		{
			global << string(g_value->getName()) << ";global;" << llvm_to_string(g_value->getValueType()) << ";" << tmpDataLayout.getTypeStoreSize(g_value->getValueType()) << ";";
		}

		if (g_value->hasInitializer())
		{
			Constant* InitializieValue = g_value->getInitializer();
			global << llvm_to_string(InitializieValue);
		}
		else
		{
			global << "unknown";
		}

		global << "\n";
	}

	global.close();
}

void ExtractStaticInfo::FunctionInfo(Module * mod, string SavePath)
{
	ofstream predecessor;
	ofstream instruction;
	ofstream function;
	ofstream argument;
	ofstream block;
	ofstream operand;
	ofstream instype;

	predecessor.open(SavePath + "//predecessor.facts");
	instruction.open(SavePath + "//instruction.facts");
	function.open(SavePath + "//function.facts");
	argument.open(SavePath + "//argument.facts");
	block.open(SavePath + "//block.facts");
	operand.open(SavePath + "//operand.facts");
	instype.open(SavePath + "//instype.facts");


	int ii = 0;
	int bi = 0;
	int fi = 0;
	int ai = 0;

	for (Function &Func : *mod)
	{
		function << fi << ";" << string(Func.getName()) << ";";
		if (Func.isDeclaration())
		{
			function << "declare;" << llvm_to_string(Func.getReturnType()) << "\n";
		}
		else
		{
			function << "define;" << llvm_to_string(Func.getReturnType()) << "\n";
		}

		int aj = 0;
		for (Function::const_arg_iterator arg = Func.arg_begin(); arg != Func.arg_end(); ++arg)
		{
			argument << fi << ";" << aj << ";" << string(arg->getName()) << ";" << llvm_to_string(arg->getType()) << "\n";
			ai++;
			aj++;
		}
		
		for (BasicBlock &B : Func)
		{
			block << fi << ";" << bi << ";" << string(B.getName()) << "\n";

			for (llvm::pred_iterator it = pred_begin(&B), end = pred_end(&B); it != end; ++it)
			{
				BasicBlock* pred = *it;
				predecessor << fi << ";" << string(B.getName()) << ";" << string(pred->getName()) << "\n";
			}

			for (Instruction &I : B)
			{
				if (StoreInst* inst = dyn_cast<StoreInst>(&I))
				{
					instype << ii << ";" << llvm_to_string(inst->getOperand(0)->getType()) << "\n";
				}
				else
				{
					instype << ii << ";" << llvm_to_string(I.getType()) << "\n";
				}
				instruction << fi << ";" << bi << ";" << ii << ";";
				if (I.hasName())
				{
					instruction << string(I.getName()) << ";";
				}
				else
				{
					instruction << "-1;";
				}
				instruction << I.getOpcodeName() << "\n";

				for (int opi = 0; opi < I.getNumOperands(); opi++)
				{
					if (llvm::ConstantInt* opd = llvm::dyn_cast<llvm::ConstantInt>(I.getOperand(opi)))
					{
						operand << ii << ";" << opi << ";" << opd->getZExtValue() << "\n";
					}
					else if (llvm::ConstantFP* opd = llvm::dyn_cast<llvm::ConstantFP>(I.getOperand(opi)))
					{
						operand << ii << ";" << opi << ";" << "float" << "\n";
					}
					else if (!I.getOperand(opi)->hasName())
					{
						operand << ii << ";" << opi << ";" << "unk" << "\n";
					}
					else if (llvm::Instruction* opd = llvm::dyn_cast<llvm::Instruction>(I.getOperand(opi)))
					{
						operand << ii << ";" << opi << ";" << string(I.getOperand(opi)->getName()) << "\n";
					}
					else
					{
						operand << ii << ";" << opi << ";" << string(I.getOperand(opi)->getName()) << "\n";
					}
				}

				ii++;
			}
			bi++;
		}
		fi++;
	}

	predecessor.close();
	argument.close();
	function.close();
	instruction.close();
	block.close();
	operand.close();
}

/// \Generate function graph, finish packaging, pruning and cloning 
bool ExtractStaticInfo::ExtractFacts(Module * mod, string SavePath)
{
	FunctionInfo(mod, SavePath);
	GlobalInfo(mod, SavePath);
	return true;
}



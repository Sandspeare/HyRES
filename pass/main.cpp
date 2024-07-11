#include "common.h"
#include "ExtractStaticInfo.h"

int main(int argc, char* argv[])
{
	string InputBCFile = argv[1];
	string SavePath = argv[2];
	Module* mod = MyParseIRFile(InputBCFile);
	if (mod == NULL)
	{
		return -1;
	}

	ExtractStaticInfo doExtractStaticInfo;
	doExtractStaticInfo.ExtractFacts(mod, SavePath);

	return 1;

}
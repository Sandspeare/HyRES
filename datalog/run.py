import argparse
import sys
import os
import subprocess
import pathlib

def parseArgs():
    parser = argparse.ArgumentParser(description='Deterministic Reasoning')
    parser.add_argument('-f', action='store', dest='facts_dir', default="facts",
                        help='specify facts directory (default: facts)')
    parser.add_argument('-o', action='store', dest='output_dir', default="output",
                        help='specify output directory (default: output)')
    parser.add_argument('-j', action='store', dest='thread_count', default="4",
                        help='specify how many threads Soufflé may use (default: 4)')
    args = parser.parse_args(sys.argv[1:])
    return args

def set_functors_path():
    absPath = str(pathlib.Path(__file__).parent.absolute())
    os.environ['LD_LIBRARY_PATH'] = absPath+"/"+"logic/functors/"

def compile_functors():
    command = "./make.sh "
    subprocess.call(command, shell=True, cwd="logic/functors/")
    set_functors_path()

def CreateDirectory(name):
    if(not os.path.isdir("./"+name)):
        os.mkdir("./"+name)

def run(facts_dir, output_dir, thread_count):
    compile_functors()
    command = "souffle \"logic/main.dl\" "
    command += "-F \""+facts_dir+"\" -D \""+output_dir+"\" "
    command += "-L logic/functors "
    command += "-j "+thread_count
    subprocess.call(command, shell=True)
    print("Execution finished output written to output directory")

if __name__ == "__main__":
    args = parseArgs()
    
    CreateDirectory("facts")
    CreateDirectory("output")
    facts_dir = args.facts_dir
    output_dir = args.output_dir
    thread_count = args.thread_count
    run(facts_dir, output_dir, thread_count)

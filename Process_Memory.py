class Process_Memory:
    def __init__(self, process_ID):
        self.process_ID = process_ID

    def run(self):
        id_name = str(self.process_ID)
        path_to_process = "/proc/" + id_name + "/status"
        size_mem_name = "VmSize:"
        with open(path_to_process, "r") as ins:
            checker = 0
            for line in ins:
                if line.startswith(size_mem_name):
                    print(line[len(size_mem_name):])
                    checker = 1
            if not checker: 
                print("VmSize is not available!") 


proc = Process_Memory(1)
proc.run()
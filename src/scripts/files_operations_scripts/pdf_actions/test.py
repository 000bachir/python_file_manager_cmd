import psutil



def check_user_ram() : 
        memory = psutil.virtual_memory()
        print(f"Total RAM: {memory.total / (1024**3):.2f} GB")
        print(f"Available RAM: {memory.available / (1024**3):.2f} GB")
        print(f"Used RAM: {memory.used / (1024**3):.2f} GB")
        MIN_RAM_REQUIRED = 1 
        MIN_CPU_CORE = 2
        available_ram = memory.available / (1024 ** 3)
        cpu_cores = psutil.cpu_count() or 1
        try : 
            if available_ram < MIN_RAM_REQUIRED: 
                print(f"Not enough RAM , Required : {MIN_RAM_REQUIRED}")
            if cpu_cores < MIN_CPU_CORE : 
                print(f"Not enough cpu core available , Required {MIN_CPU_CORE}")
        except RuntimeError as e : 
            print(f"Not enough ressources available {e}")
        finally :  
            print("System meets the minimum requirenemnts\n")

check_user_ram()

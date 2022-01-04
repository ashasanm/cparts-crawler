def get_nvidia_gtx_gpu():
    name_scheme = {"prefix": "gtx",
                   "generation_max": 10,
                   "perf_tier_max": 8,
                   "revision": 0,
                   "suffix": "Ti", }
    gpus = []
    listing = True
    generation = 5
    while listing:
        if generation == (name_scheme["generation_max"]+6):
            listing = False

        perf_tier = 5
        while perf_tier <= name_scheme["perf_tier_max"]:
            if generation == 8:
                break
            elif generation == 16:
                if perf_tier > 6:
                    break

            suffix = 0
            series = "{} {}{}{}".format(name_scheme["prefix"], generation, perf_tier, name_scheme["revision"])
            gpus.append(series)
            suffix += 1 
            if suffix == 1:
                series = "{} {}{}{} {}".format(name_scheme["prefix"], generation, perf_tier, name_scheme["revision"], name_scheme["suffix"])
                gpus.append(series)
            perf_tier += 1
        generation += 1
        if generation > name_scheme["generation_max"]:
            generation = 16

    return gpus


def get_nvidia_rtx_gpu():
    name_scheme = {"prefix": "rtx",
                    "generation_min": 20,
                   "generation_max": 30,
                   "perf_tier_min": 6,
                   "perf_tier_max": 9,                   
                   "revision": 0,
                   "suffix": "Ti"}
    gpus = []
    listing = True
    generation = name_scheme["generation_min"]
    while listing:
        perf_tier = name_scheme["perf_tier_min"]

        while perf_tier <= name_scheme["perf_tier_max"]:
            
            if perf_tier == name_scheme["perf_tier_max"] and generation == name_scheme["generation_min"]:
                break
            
            if perf_tier == name_scheme["perf_tier_max"]:
                series = "{} {}{}{}".format(name_scheme["prefix"], generation, perf_tier, name_scheme["revision"])
                gpus.append(series)
            else:
                series = "{} {}{}{}".format(name_scheme["prefix"], generation, perf_tier, name_scheme["revision"])
                gpus.append(series)
                series = "{} {}{}{} {}".format(name_scheme["prefix"], generation, perf_tier, name_scheme["revision"], name_scheme["suffix"])
                gpus.append(series)
            perf_tier += 1

        generation += 10

        if generation > name_scheme["generation_max"]:
            listing = False

    return gpus


def get_amd_gpu():
    amd = [
        "rx 460","rx 470", "rx 480", 
        "rx 550", "rx 560", "rx 570", "rx 580",
        "rx 5500", "rx 5500 xt", "rx 5600", "rx 5600 xt", "rx 5700", "rx 5700 xt",
        "rx 6600", "rx 6600 xt", "rx 6700 xt", "rx 6800", "rx 6800 xt", "rx 6900 xt" 
        ]
        
    return amd
            



if __name__ == '__main__':
    gpu_lists = []
    nvidia_gtx = get_nvidia_gtx_gpu()
    nvidia_rtx = get_nvidia_rtx_gpu()

    

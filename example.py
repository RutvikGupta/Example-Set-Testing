class Example:
    def __init__(self, name: str):
        self.name = name
        self.pipeLoop = DEF_S_pipeLoop
        self.maxTime = DEF_S_maxTime
        self.minTime = DEF_S_minTime
        self.graceTime = DEF_S_graceTime
        self.defaultInput = DEF_S_defaultInput
        self.activeInput = DEF_S_activeInput
        self.defaultTarget = DEF_S_defaultTarget
        self.activeTarget = DEF_S_activeTarget
        self.loadEvent = standardLoadEvent
        self.loadExample = standardLoadExample
        self.numGroupNames = 0
        self.maxGroupNames = 0
        self.groupName = NULL

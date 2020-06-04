# #ifndef DEFAULTS_H
# #define DEFAULTS_H
#
# /* NETWORK FIELDS */
DEF_N_numTimeIntervals = 1
DEF_N_numTicksPerInterval = 1
DEF_N_backpropTicks = 1

DEF_N_numUpdates = 100
DEF_N_batchSize = 0  # /* This means full batch mode */
DEF_N_reportInterval = 10
DEF_N_criterion = 0.0
DEF_N_trainGroupCrit = 0.0
DEF_N_testGroupCrit = 0.5
DEF_N_groupCritRequired = False
DEF_N_minCritBatches = 1
DEF_N_pseudoExampleFreq = False

# DEF_N_algorithm           DOUGS_MOMENTUM
DEF_N_learningRate = 0.1
# ifdef ADVANCED
# define DEF_N_rateIncrement      0.1
# define DEF_N_rateDecrement      0.9
# endif /* ADVANCED */
DEF_N_momentum = 0.9
DEF_N_adaptiveGainRate = 0.001
DEF_N_weightDecay = 0.0
"""/* dcp */"""
DEF_N_weightEliminationW0 = 0.0
DEF_N_gainDecay = 0.0
DEF_N_outputCostStrength = 0.01
DEF_N_outputCostPeak = 0.5
DEF_N_targetRadius = 0.0
DEF_N_targetZeroScaling = 1.0
DEF_N_zeroErrorRadius = 0.0

DEF_N_gain = 1.0
DEF_N_ternaryShift = 5.0
DEF_N_clampStrength = 0.5
DEF_N_initOutput = 0.5
DEF_N_initOutputRange = 0.0
DEF_N_initInput = 0.0
DEF_N_initGain = 1.0
DEF_N_finalGain = 1.0
DEF_N_annealTime = 1.0

DEF_N_randMean = 0.0
DEF_N_randRange = 1.0
DEF_N_noiseRange = 0.1

DEF_N_autoPlot = True
DEF_N_plotCols = 10
DEF_N_unitCellSize = 14
DEF_N_unitCellSpacing = 2
# DEF_N_unitDisplayValue    UV_OUT_TARG
# DEF_N_unitDisplaySet      TRAIN_SET
# DEF_N_unitUpdates         ON_REPORT
DEF_N_unitTemp = 1.0
# DEF_N_unitPalette         BLUE_BLACK_RED
DEF_N_unitExampleProc = 0
DEF_N_boltzUnitExampleProc = 1

DEF_N_linkCellSize = 8
DEF_N_linkCellSpacing = 0
# DEF_N_linkDisplayValue    UV_LINK_WEIGHTS
# DEF_N_linkUpdates         ON_REPORT
DEF_N_linkTemp = 1.0
# DEF_N_linkPalette         BLUE_BLACK_RED

# DEF_N_writeExample        standardWriteExample

"""/* GROUP FIELDS */"""
DEF_G_standardReset = True  # /* RESET_ON_EXAMPLE for SRNs */
DEF_G_continuousReset = True  # /* for continuous networks */
DEF_G_trainGroupCrit = None
DEF_G_testGroupCrit = None

DEF_G_learningRate = None
DEF_G_momentum = None
DEF_G_weightDecay = None
# /* dcp */
DEF_G_weightEliminationW0 = None
DEF_G_gainDecay = None
DEF_G_outputCostScale = 1.0
DEF_G_outputCostPeak = None
DEF_G_targetRadius = None
DEF_G_targetZeroScaling = None
DEF_G_zeroErrorRadius = None
DEF_G_errorScale = 1.0

DEF_G_dtScale = 1.0
DEF_G_gain = None
DEF_G_ternaryShift = None
DEF_G_clampStrength = None
DEF_G_initOutput = None
DEF_G_initOutputRange = None
DEF_G_initInput = None

DEF_G_randMean = None
DEF_G_randRange = None
DEF_G_noiseRange = None
# DEF_G_noiseProc           = addGaussianNoise

DEF_G_showIncoming = True
DEF_G_showOutgoing = True
DEF_G_numColumns = 0
DEF_G_neighborhood = 4
DEF_G_periodicBoundary = False

"""/* UNIT FIELDS */"""
DEF_U_target = None
DEF_U_externalInput = None
DEF_U_dtScale = 1.0
DEF_U_activeTicks = 1

"""/* BLOCK FIELDS */"""
DEF_B_learningRate = None
DEF_B_momentum = None
DEF_B_weightDecay = None
"""/* dcp */"""
DEF_B_weightEliminationW0 = None
DEF_B_randMean = None
DEF_B_randRange = None
DEF_B_min = None
DEF_B_max = None

"""/* LINK FIELDS */"""
DEF_L_deriv = 0.0
DEF_L_lastWeightDelta = 0.0
DEF_L_lastValue = 1.0

"""/* EXAMPLE SET FIELDS */"""
DEF_S_mode = bool(1 << 0)
DEF_S_pipeLoop = True
DEF_S_maxTime = 1.0
DEF_S_minTime = 0.0
DEF_S_graceTime = 0.0
DEF_S_defaultInput = 0.0
DEF_S_activeInput = 1.0
DEF_S_defaultTarget = 0.0
DEF_S_activeTarget = 1.0
# DEF_S_loadEvent           =standardLoadEvent
# DEF_S_loadExample         =standardLoadExample
# DEF_S_loadNextExample     =standardLoadNextExample


"""/* EXAMPLE FIELDS */"""
DEF_E_frequency = 1.0

"""/* EVENT FIELDS */"""
DEF_V_maxTime = None
DEF_V_minTime = None
DEF_V_graceTime = None

"""/* GRAPH PARAMETERS */"""
DEF_GR_columns = 100
DEF_GR_values = 100
DEF_GR_lineWidth = 1.0

"""/* OTHER STUFF */"""
DEF_GUI = True  # /* Whether the Main Window opens by default. */
DEF_BATCH = False  # /* Whether its in Batch mode by default. */
DEF_CONSOLE = False  # /* Whether the Console opens by default. */
DEF_VERBOSITY = 1  # /* The initial verbosity level. */

"""/* Buffer Limits */"""
BUFFER_SIZE = 4096  # /* Size of the text Buffer. */
PAR_BUF_SIZE = 8192  # /* Buffer size for parallel weight transfers.
# Must be at least 3 */
MAX_TYPES = 32  # /* Max types modifying a single group */

"""/* Fast Sigmoid */"""
SIGMOID_RANGE = 16  # /* Sigmoid defined for up to +- this value */
SIGMOID_SUB = 1024  # /* Granularity of the table */

"""/* Magic Cookies */"""
BINARY_EXAMPLE_COOKIE = 0xaaaaaaaa  # /* 10101010... */
OLD_BINARY_WEIGHT_COOKIE = 0x55555555  # /* 01010101... */
BINARY_WEIGHT_COOKIE = 0x55555556

BIAS_NAME = "bias"  # /* The name of the bias group */
NUM_COLORS = 101  # /* Colors in blue-red colormap */
UPDATE_INTERVAL = 100  # /* Interval between screen updates,
# in milliseconds */
"""// dcp CHANGE"""
#   AUTO_NICE_VALUE  =10       #/* Long-running process renice value */
AUTO_NICE_VALUE = 0  # /* Long-running process renice value */
AUTO_NICE_DELAY = 10  # /* Minutes before auto-renicing */

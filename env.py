import math
import qutils

ACCOUNT = "1"
BUILD = "1"

N = 75 # number of experiments in one run
SHOTS = 8192
BACKEND_ID = "ibmqx2" # ibmq_qasm_simulator ibmqx2 ibmq_rome
SKIP_RUN = True

# prepare parameter
theta_start = 0 # inclusive
theta_end = 2 * math.pi # not inclusive

 # to keep same step, but differ values
step = (theta_end - theta_start) / N
runs_count = 1
run_index = 0 # stopped on acc 3, index 5
theta_offset = run_index * step / runs_count

THETA, THETA_VALUES = qutils.prepareParameter('θ', theta_start, theta_end, N, theta_offset)

CONTEXT_COMMENT = str(N) + " experiments, " + \
                  str(SHOTS) + " shots, " + \
                  "range [" + str(theta_start) + ", " + str(theta_end) + "), " + \
                  "offset " + str(theta_offset)

CURRENT_DEVICE = qutils.backend(ACCOUNT, BACKEND_ID)

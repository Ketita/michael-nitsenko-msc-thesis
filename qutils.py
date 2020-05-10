import utils
from qiskit import IBMQ
from qiskit.compiler import transpile, assemble
from qiskit.tools.monitor import job_monitor
from qiskit.circuit import Parameter

def prepareParameter(name, start, end, splits, offset):
    # calculate parameter
    values = []
    step = (end - start) / splits
    for i in range(splits):
        value = i * step + offset
        values.append(value)
    
    return Parameter(name), values

def backend(account, backend_id):
    token = utils.accounts()[account]["token"]
    try: IBMQ.disable_account()
    except: pass
    provider = IBMQ.enable_account(token)
    return provider.get_backend(backend_id)

# transpile
def optimize(circuit, device):
    transpiled_qc = transpile(circuit, backend=device)
    return transpiled_qc

# assemble
def build(circuit, device, shots):
    return assemble(circuit, backend=device, shots=shots)

# run
def run(qobj, device, parameters, comment = "", monitor = False):
    job = device.run(qobj)
    path = utils.record(job, device, parameters, comment)
    
    if monitor:
        print(path)
        job_monitor(job)
        _ = job.result()
        
    return path

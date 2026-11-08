from bbpssw import bbpssw_protocol_alice
from netqasm.sdk import EPRSocket, Qubit
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
import numpy as np
from scipy.linalg import sqrtm


def main(app_config=None):

    # Create a socket for classical communication
    socket = Socket("alice", "bob")

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("bob")

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket],
    )

    # Create Alice's context, initialize EPR pairs inside it and call Alice's BBPSSW method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:
        # Create ERP pair
        epr1 = epr_socket.create()[0]
        epr2 = epr_socket.create()[0]
        alice.flush()

        original_dm = 0.5 * np.array([
            [1, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 0, 0, 1],
        ])

        original_dm_Z = 0.5 * np.array([
            [1, 0, 0, -1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [-1, 0, 0, 1],
        ])
        original_dm_I = (1 / 4) * np.array([
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ])

        original_dm_2 = 0.5 * np.array([
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
        ])

        original_dm_2_Z = 0.5 * np.array([
            [0, 0, 0, 0],
            [0, 1, -1, 0],
            [0, -1, 1, 0],
            [0, 0, 0, 0],
        ])

        original_fidelity1 = get_fidelity(get_qubit_state(epr1, False), original_dm)
        original_fidelity2 = get_fidelity(get_qubit_state(epr2, False), original_dm)
        print(f'OriginalFidelity1:{original_fidelity1}')
        print(f'OriginalFidelity2:{original_fidelity2}')
        socket.send('Original Fidelity measured')

        success = bbpssw_protocol_alice(epr1, epr2, alice, socket)
        dm1 = get_qubit_state(epr1, False)

        fidelity = get_fidelity(dm1, original_dm)
        fidelityI = get_fidelity(dm1, original_dm_I)
        fidelity2 = get_fidelity(dm1, original_dm_2)
        fidelityZ = get_fidelity(dm1, original_dm_Z)
        fidelity2Z = get_fidelity(dm1, original_dm_2_Z)
        socket.send("Fidelity measured")
        res = epr1.measure()
        alice.flush()
        print(f"Alice:measurement {res}")
        print(f"Success:{success}")
        print(f"Fidelity:{fidelity}")
        print(f"FidelityI:{fidelityI}")
        print(f"Fidelity2:{fidelity2}")
        print(f"FidelityZ:{fidelityZ}")
        print(f"Fidelity2Z:{fidelity2Z}")

        print(f"Matrix {dm1}")




def get_fidelity(density1, density2):
    sqrt_density2 = sqrtm(density2)
    product = np.dot(np.dot(sqrt_density2, density1), sqrt_density2)
    sqrt_prod = sqrtm(product)
    return np.round(np.real((np.trace(sqrt_prod))**2), 7)

if __name__ == "__main__":
    main()

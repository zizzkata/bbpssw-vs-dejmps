from dejmps import dejmps_protocol_bob
from netqasm.sdk import EPRSocket, Qubit
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state

def main(app_config=None):

    # Create a socket for classical communication
    socket = Socket("bob", "alice")

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("alice")

    # Initialize Alice's NetQASM connection
    bob = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket],
    )

    # Create Bob's context, initialize EPR pairs inside it and call Bob's DEJMPS method. Finally, print out whether or not Bob successfully created an EPR Pair with Alice.
    with bob:
        epr1 = epr_socket.recv()[0]
        epr2 = epr_socket.recv()[0]
        original_fidelity_finished = socket.recv()
        success = dejmps_protocol_bob(epr1, epr2, bob, socket)
        fidelity_finished = socket.recv()
        res = epr1.measure()
        bob.flush()
        print(f"Bob:measurement {res}")

if __name__ == "__main__":
    main()

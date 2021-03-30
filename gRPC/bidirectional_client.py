import grpc
import gRPC.proto.grpc_pb2_grpc as pb2_grpc
import gRPC.proto.grpc_pb2 as pb2


def make_message(message):
    return pb2.Message(
        message=message
    )


def generate_messages():
    messages = [
        make_message("First message"),
        make_message("Second message"),
        make_message("Third message"),
        make_message("Fourth message"),
        make_message("Fifth message"),
    ]
    for msg in messages:
        print("Hello Server Sending you the %s" % msg.message)
        yield msg


def send_message(stub):
    responses = stub.bidirectional(generate_messages())
    for response in responses:
        print("Hello from the server received your %s" % response.message)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = pb2_grpc.GRPCServiceStub(channel)
        send_message(stub)


if __name__ == '__main__':
    run()
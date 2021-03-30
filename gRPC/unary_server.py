from concurrent import futures

import grpc

import gRPC.proto.grpc_pb2_grpc as pb2_grpc
from gRPC.proto.grpc_pb2 import Message
from gRPC.proto.grpc_pb2_grpc import GRPCServiceServicer


class UnaryServerService(GRPCServiceServicer):

    def unary(self, request, context):
        return Message(message='Server, %s!' % request.message)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_GRPCServiceServicer_to_server(UnaryServerService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

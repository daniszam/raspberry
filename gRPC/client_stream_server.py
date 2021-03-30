from concurrent import futures

import grpc

import gRPC.proto.grpc_pb2 as pb2
import gRPC.proto.grpc_pb2_grpc as pb2_grpc


class ClientStreamService(pb2_grpc.GRPCServiceServicer):

    def request_stream(self, request_iterator, context):
        return pb2.Message(message='Response')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_GRPCServiceServicer_to_server(ClientStreamService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

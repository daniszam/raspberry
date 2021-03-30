from concurrent import futures

import grpc
import gRPC.proto.grpc_pb2_grpc as pb2_grpc


class BidirectionalService(pb2_grpc.GRPCServiceServicer):

    def bidirectional(self, request_iterator, context):
        for message in request_iterator:
            yield message


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_GRPCServiceServicer_to_server(BidirectionalService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
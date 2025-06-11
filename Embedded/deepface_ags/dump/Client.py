from dsocket import Client

client = Client()
while True:
    fname = input()
    if fname:
        client.send_data(fname)
        fname = None
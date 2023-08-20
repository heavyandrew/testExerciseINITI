import argparse
from api import Server

def main():
    parser = argparse.ArgumentParser(description='Insert port, conf_path, cam_num, sub_instance_list_path')
    parser.add_argument(
        '--port',
        type=str,
        help='Port for instance'
    )
    parser.add_argument(
        '--data_path',
        type=str,
        help='Path to conf file'
    )

    input = parser.parse_args()

    app = Server(input.port, input.data_path)
    app.run()

#python .\server\main.py --port 80 --data_path "data.csv"

if __name__ == "__main__":
    main()
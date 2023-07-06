import subprocess as sp
import argparse
import json
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(description='AZSH - Simple azure run command wrapper')

    parser.add_argument('--resource-group', '-g', help='The resource group the VM is located in', required=True, default=None)
    parser.add_argument('--name', '-n', help='The name of the VM', required=True, default=None)
    parser.add_argument('--subscription', '-s', help='The subscription the resource group and VM are located in', default=None)

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    base = ["az", "vm", "run-command", "invoke", "-g", args.resource_group, "-n", args.name, "--command-id", "RunShellScript"]
    if args.subscription:
        base = base + ["--subscription", args.subscription]

    try:
        while True:
            cmd = input(f"{args.name} > ")
            if cmd == "exit":
                exit()
            params = base + ["--scripts", cmd]
            ret = sp.run(params, shell=True, capture_output=True, text=True)
            ret_data = json.loads(ret.stdout)
            output = ret_data['value'][0]['message']
            start_stdout = output.find("[stdout]") + 9
            end_stdout = output.find("\n[stderr]")
            stdout = output[start_stdout:end_stdout]
            stderr = output[end_stdout+9:-1]
            print(stderr, file=sys.stderr)
            print(stdout)
    except KeyboardInterrupt:
        exit()


if __name__ == "__main__":
    main()    

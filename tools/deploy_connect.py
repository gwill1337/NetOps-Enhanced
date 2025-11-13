from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.task import Task, Result
from nornir.plugins.inventory import simple

def connect_device(task: Task) -> Result:

    # TODO:
    # if task.host.platform == "cisco_ios":
    #     config_mode_command = "configure terminal"
    # elif task.host.platform == "juniper":
    #     config_mode_command = "configure"
    # elif task.host.platform == "paloalto_panos":
    #     config_mode_command = "configure"

    # test connection
    result = task.run(
        task=netmiko_send_command,
        command_string="show version"
    )

    return Result(host=task.host, result=result.result)

if __name__ == "__main__":
    nr = InitNornir(config_file="config.yaml")
    results = nr.run(task=connect_device)

    for host, res in results.items():
        print(f"{host}:\n{res[0].result}\n{'-'*40}")

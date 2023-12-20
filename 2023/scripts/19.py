import copy
import math
from collections import defaultdict

from aoc_utils import read_input


def parse_part(part_str: str) -> dict:
    part_str_without_brackets = part_str.strip("{}")
    part_elements = [
        element.split("=")
        for element in part_str_without_brackets.split(",")
        if element
    ]
    return {key: int(value) for key, value in part_elements}


def parse_workflow(workflow_str: str) -> tuple[str, list]:
    workflow_str_name, workflow_str_content = workflow_str.strip("}").split("{")

    workflow_content = [
        workflow.split(":") for workflow in workflow_str_content.split(",")
    ]
    workflow_content = [
        workflow if len(workflow) == 2 else [None, workflow[0]]
        for workflow in workflow_content
    ]

    return workflow_str_name, workflow_content


raw_input_workflows, raw_input_parts = read_input(raw_input=True).split("\n\n")

# parse the parts and workflows
input_parts = [
    part for part in [parse_part(part) for part in raw_input_parts.split("\n")] if part
]
input_workflows = {
    name: content
    for name, content in [
        parse_workflow(workflow) for workflow in raw_input_workflows.split("\n")
    ]
}


def put_part_in_workflows(part: dict, workflows: dict) -> bool:
    workflow = workflows["in"]
    while True:
        for condition_output in workflow:
            condition, output = condition_output
            if not condition:
                if output == "A":
                    return True
                elif output == "R":
                    return False
                else:
                    workflow = workflows[output]
                    break
            elif "<" in condition:
                parameter_name, condition_value_str = condition.split("<")
                condition_value = int(condition_value_str)
                parameter_value = part[parameter_name]

                if parameter_value < condition_value:
                    if output == "A":
                        return True
                    elif output == "R":
                        return False
                    workflow = workflows[output]
                    break

            elif ">" in condition:
                parameter_name, condition_value_str = condition.split(">")
                condition_value = int(condition_value_str)
                parameter_value = part[parameter_name]

                if parameter_value > condition_value:
                    if output == "A":
                        return True
                    elif output == "R":
                        return False
                    workflow = workflows[output]
                    break


def get_workflows_graph(workflows: dict, workflow_name: str, graph: dict):
    workflow = workflows[workflow_name]
    for condition_output in workflow:
        condition, output = condition_output

        condition_str = condition if condition is not None else str(condition)

        if output == "A":
            graph[condition_str] = True if output == "A" else False
        elif output != "R":
            graph[condition_str] = {}
            get_workflows_graph(workflows, output, graph[condition_str])
            if not graph[condition_str]:
                graph.pop(condition_str)


print(
    "P1",
    sum(
        [
            sum(list(part.values()))
            for part in input_parts
            if put_part_in_workflows(part, input_workflows)
        ]
    ),
)

workflows_graph = {}
get_workflows_graph(input_workflows, "in", workflows_graph)


def get_paths(d):
    q = [(d, [])]
    while q:
        n, p = q.pop(0)

        td = copy.deepcopy(d)
        for sp in p:
            td = td[sp]
        if td == True:
            yield p

        if isinstance(n, dict):
            for k, v in n.items():
                q.append((v, p + [k]))


valid_paths = list(get_paths(workflows_graph))

total_possibilities = []
for path in valid_paths:
    valid_ranges = {key: [1, 4000] for key in "xmas"}
    for cond in path:
        if cond == "None":
            pass
        elif "<" in cond:
            cond_param, cond_value_str = cond.split("<")
            cond_value = int(cond_value_str)
            valid_ranges[cond_param][1] = min(
                valid_ranges[cond_param][1], cond_value - 1
            )

        elif ">" in cond:
            cond_param, cond_value_str = cond.split(">")
            cond_value = int(cond_value_str)
            valid_ranges[cond_param][0] = max(
                valid_ranges[cond_param][0], cond_value + 1
            )

    total_possibilities.append(valid_ranges)

print(total_possibilities)

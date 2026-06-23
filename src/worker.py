import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from src.workflows.parent.hello_world import SayHelloWorkflow
    from src.workflows.child.hello_world_child import ComposeGreetingWorkflow
    from src.activities.activities import greet
    from src.utils.constants import TASK_QUEUE, CLIENT


async def main():
    client = await Client.connect(CLIENT)
    worker = Worker(
        client=client,
        task_queue=TASK_QUEUE,
        workflows=[SayHelloWorkflow, ComposeGreetingWorkflow],
        activities=[greet],
    )
    print("Worker started.")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())

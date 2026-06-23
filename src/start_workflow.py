import asyncio
import uuid
from temporalio.client import Client
import sys

from src.utils.constants import TASK_QUEUE, CLIENT


async def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "Temporal"
    client = await Client.connect(CLIENT)
    result = await client.start_workflow(
        workflow="HelloWorldWorkflow",
        args=[name],
        id=f"say-hello-workflow-{uuid.uuid4()}",
        task_queue=TASK_QUEUE,
    )
    print("Workflow result:", result)


if __name__ == "__main__":
    asyncio.run(main())

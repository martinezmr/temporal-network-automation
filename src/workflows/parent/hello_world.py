from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from src.activities.activities import greet
    from src.models.models import ComposeGreetingInput
    from src.workflows.child.hello_world_child import ComposeGreetingWorkflow
    from src.utils.constants import TASK_QUEUE


@workflow.defn(name="HelloWorldWorkflow")
class SayHelloWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        result = await workflow.execute_child_workflow(
            workflow=ComposeGreetingWorkflow.run,
            args=[ComposeGreetingInput(greeting="What up", name=name)],
            id=f"compose-greeting-workflow-{workflow.info().workflow_id}",
            task_queue=TASK_QUEUE,
        )

        result += await workflow.execute_activity(
            activity=greet,
            args=[name],
            schedule_to_close_timeout=timedelta(seconds=10),
        )

        return f"Workflow completed for {name}! Result: {result}"

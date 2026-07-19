from temporalio import workflow
from src.utils.models.models import ComposeGreetingInput


@workflow.defn
class ComposeGreetingWorkflow:
    @workflow.run
    async def run(self, input: ComposeGreetingInput) -> str:
        return f"{input.greeting}, {input.name}!"

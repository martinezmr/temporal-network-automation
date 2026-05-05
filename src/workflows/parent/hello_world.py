from datetime import timedelta
from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from src.activities.activities import greet

@workflow.defn(name="HelloWorldWorkflow")
class SayHelloWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            activity=greet,
            args=[name],
            schedule_to_close_timeout=timedelta(seconds=10),
        )
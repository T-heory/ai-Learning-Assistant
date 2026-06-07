from llm.deepseek_client import DeepSeekClient
from agents.profile_agent import ProfileAgent
from agents.resource_agent import ResourceAgent
from agents.path_agent import PathPlannerAgent
from agents.tutor_agent import TutorAgent
from agents.evaluator_agent import EvaluatorAgent


class Orchestrator:
    def __init__(self, llm: DeepSeekClient):
        self.llm = llm
        self.agents = {
            "profile": ProfileAgent(llm),
            "resource": ResourceAgent(llm),
            "path": PathPlannerAgent(llm),
            "tutor": TutorAgent(llm),
            "evaluator": EvaluatorAgent(llm),
        }
        self.workflows = {
            "onboarding": [
                ("profile", "extract"),
                ("resource", "generate"),
                ("path", "plan"),
            ],
            "question": [
                ("tutor", "answer"),
            ],
            "evaluate": [
                ("evaluator", "assess"),
                ("path", "adjust"),
            ],
        }

    async def run_workflow(self, workflow_name: str, context: dict) -> dict:
        results = {}
        if workflow_name not in self.workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")

        for agent_name, action in self.workflows[workflow_name]:
            agent = self.agents.get(agent_name)
            if not agent:
                continue
            agent_input = {**context, **results}
            agent_result = await agent.process(agent_input)
            results[f"{agent_name}_{action}"] = agent_result
        return results

    async def run_agent(self, agent_name: str, input_data: dict) -> dict:
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Unknown agent: {agent_name}")
        return await agent.process(input_data)

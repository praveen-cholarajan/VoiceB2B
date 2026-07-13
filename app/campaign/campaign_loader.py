import json
from pathlib import Path


class CampaignLoader:

    def __init__(self, campaign_name: str):

        project_root = Path(__file__).resolve().parents[2]

        self.file_path = (
            project_root
            / "app"
            / "campaign"
            / f"{campaign_name}.json"
        )

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Campaign file not found:\n{self.file_path}"
            )

        with open(self.file_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    # =====================================================
    # Campaign
    # =====================================================

    def load(self):

        return self.data

    @property
    def name(self):

        return self.data.get("campaign_name", "")

    # =====================================================
    # Agent
    # =====================================================

    @property
    def agent(self):

        return self.data.get("agent", {})

    @property
    def agent_name(self):

        return self.agent.get("name", "Voice Agent")

    @property
    def company_name(self):

        return self.agent.get("company", "Vi Business")

    # =====================================================
    # States
    # =====================================================

    @property
    def states(self):

        return self.data.get("states", {})

    @property
    def start_state(self):

        return self.data.get("start_state", "GREETING")

    def get_state(self, state_name):

        if not state_name:
            return None

        return self.states.get(state_name)

    def has_state(self, state_name):

        return state_name in self.states

    def state_names(self):

        return list(self.states.keys())

    def get_next_state(self, state_name):

        state = self.get_state(state_name)

        if state is None:
            return None

        return state.get("next")

    def is_last_state(self, state_name):

        return self.get_next_state(state_name) is None

    def get_script(self, state_name):

        state = self.get_state(state_name)

        if state is None:
            return []

        return state.get("script", [])

    def get_goal(self, state_name):

        state = self.get_state(state_name)

        if state is None:
            return ""

        return state.get("goal", "")

    def get_collect_fields(self, state_name):

        state = self.get_state(state_name)

        if state is None:
            return []

        return state.get("collect", [])

    # =====================================================
    # Plans
    # =====================================================

    @property
    def plans(self):

        return self.data.get("plans", {})

    def get_plan(self, plan_name):

        return self.plans.get(plan_name)

    def get_all_plans(self):

        return self.plans

    # =====================================================
    # Documents
    # =====================================================

    @property
    def documents(self):

        return self.data.get("documents", {})

    def get_documents(self, business_type):

        docs = []

        docs.extend(
            self.documents.get(
                business_type,
                []
            )
        )

        docs.extend(
            self.documents.get(
                "common",
                []
            )
        )

        return docs

    # =====================================================
    # Objections
    # =====================================================

    @property
    def objections(self):

        return self.data.get("objections", {})

    def get_objection(self, objection):

        return self.objections.get(
            objection,
            []
        )

    # =====================================================
    # Helpers
    # =====================================================

    def __contains__(self, state_name):

        return self.has_state(state_name)

    def __len__(self):

        return len(self.states)

    def __repr__(self):

        return (
            f"CampaignLoader("
            f"name={self.name}, "
            f"states={len(self.states)})"
        )
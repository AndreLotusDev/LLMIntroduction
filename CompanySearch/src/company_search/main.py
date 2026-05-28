#!/usr/bin/env python
import sys
import warnings

from company_search.crew import CompanySearch

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew interactively, asking the user for a company name.
    """
    company_name = input("Enter the company name to research: ").strip()
    if not company_name:
        raise ValueError("Company name cannot be empty.")

    inputs = {
        'company_name': company_name,
    }

    try:
        result = CompanySearch().crew().kickoff(inputs=inputs)
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(result)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    inputs = {"company_name": sys.argv[3] if len(sys.argv) > 3 else "Tesla"}
    try:
        CompanySearch().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    try:
        CompanySearch().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    inputs = {"company_name": sys.argv[3] if len(sys.argv) > 3 else "Tesla"}
    try:
        CompanySearch().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "company_name": trigger_payload.get("company_name", ""),
    }

    try:
        result = CompanySearch().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")

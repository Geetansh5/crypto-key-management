from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

class Policy(BaseModel):
    id: int
    name: str
    description: str

# Mock database
mock_db: Dict[int, Policy] = {}
current_id = 1

@router.post("/policies", response_model=Policy)
async def create_policy(policy: Policy):
    global current_id
    policy.id = current_id
    mock_db[current_id] = policy
    current_id += 1
    return policy

@router.get("/policies", response_model=List[Policy])
async def list_policies():
    return list(mock_db.values())

@router.get("/policies/{policy_id}", response_model=Policy)
async def get_policy(policy_id: int):
    if policy_id not in mock_db:
        raise HTTPException(status_code=404, detail="Policy not found")
    return mock_db[policy_id]

@router.put("/policies/{policy_id}", response_model=Policy)
async def update_policy(policy_id: int, policy: Policy):
    if policy_id not in mock_db:
        raise HTTPException(status_code=404, detail="Policy not found")
    policy.id = policy_id
    mock_db[policy_id] = policy
    return policy

@router.delete("/policies/{policy_id}")
async def delete_policy(policy_id: int):
    if policy_id not in mock_db:
        raise HTTPException(status_code=404, detail="Policy not found")
    del mock_db[policy_id]
    return {"message": "Policy deleted successfully"}
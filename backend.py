import hashlib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import difflib
from main import agentic_analyzer
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Data Models ---
class PolicyVersion(BaseModel):
    policy: str
    version_id: str
    content: str  # The raw text of the policy

class ComparisonRequest(BaseModel):
    old_version: PolicyVersion
    new_version: PolicyVersion
class PolicyRequest(BaseModel):
    policy: str


# --- Core Logic Functions ---

def generate_policy_hash(text: str) -> str:
    """Creates a SHA-256 hash for blockchain storage."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def get_policy_diff(old_text: str, new_text: str) -> List[str]:
    """Detects added, removed, or changed clauses."""
    diff = difflib.ndiff(old_text.splitlines(), new_text.splitlines())
    # Filter to show only changes (+ or -)
    changes = [line for line in diff if line.startswith('+ ') or line.startswith('- ')]
    return changes

# --- API Endpoints ---

@app.post("/compare-policy")
async def compare_policy(data: ComparisonRequest):
    """
    Main endpoint for Member 4's logic: 
    Detects changes and generates hashes for blockchain entry.
    """
    try:
        # 1. Generate Hashes for Member 4's Blockchain layer
        old_hash = generate_policy_hash(data.old_version.content)
        new_hash = generate_policy_hash(data.new_version.content)
        
        # 2. Compute Differences
        differences = get_policy_diff(data.old_version.content, data.new_version.content)
        
        # 3. Determine if a "Consent Revocation" prompt is needed
        # (If significant clauses were removed or risky ones added)
        status = "changed" if differences else "identical"
        
        return {
            "status": status,
            "old_version_hash": old_hash,
            "new_version_hash": new_hash,
            "diff_count": len(differences),
            "changes": differences,
            "requires_reconsent": len(differences) > 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
class PolicyRequest(BaseModel):
    policy: str
@app.post("/analyze-policy")
async def analyze_policy(data: PolicyRequest):

    result = agentic_analyzer(data.policy)

    return result

@app.post("/analyze-policy")
async def analyze_policy(data: PolicyRequest):

    result = agentic_analyzer(data.policy)

    return result
    """Logic to simulate writing a 'Revoke' status to the blockchain."""
    # In a real demo, this would call Member 4's smart contract/local chain
    tx_hash = generate_policy_hash(f"{user_id}-{policy_id}-REVOKED")
    return {
        "message": "Consent revoked successfully",
        "audit_trail_hash": tx_hash 
}
    